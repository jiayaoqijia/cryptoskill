#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""X-Aggregate-Data：让 agent 读得到 X（Twitter）。不用 X API、不用登录、不用会员。

实时数据（读推、对话、搜索、账号、时间线、关注列表、翻译）在本机直接请求公开的 FxTwitter 接口；
X 中文区的统计（账号每日数据、排行、冠军、日报、大V动态、热帖、话题、谣言库）来自蓝不住 lanbuzhu.org 的开放接口。
只用 Python 标准库（3.8+），自动走系统代理 / HTTPS_PROXY。输出是 JSON。用法：python3 x.py -h
"""
import argparse
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

VERSION = "1.1.0"
FX = os.environ.get("XAD_FX", "https://api.fxtwitter.com").rstrip("/")
LBZ = os.environ.get("LANBUZHU_API", "https://lanbuzhu.org/api/open/v1").rstrip("/")
UA = "x-aggregate-data/%s (+https://github.com/qianyubtc/X-Aggregate-Data)" % VERSION
PAGE_GAP = 0.6  # 翻页之间歇一下，别把公开接口打爆
ARTICLE_MAX = 30000  # 长文正文最多给这么多字
NET_HINT = "连不上的话：国内网络要开代理（系统代理，或 HTTPS_PROXY=http://… 环境变量，不支持 socks）；Codex 等有沙箱的 agent 要允许联网"
PRETTY = False


class Fail(Exception):
    def __init__(self, msg, hint=None, code=1):
        super().__init__(msg)
        self.msg, self.hint, self.code = msg, hint, code


# ---------------- 网络 ----------------

def _proxy_for(url):
    p = urllib.request.getproxies()
    host = urllib.parse.urlsplit(url).hostname or ""
    try:
        if urllib.request.proxy_bypass(host):
            return None
    except Exception:
        pass
    return p.get("https") or p.get("http") or p.get("all")


def _curl(url, timeout):
    """urllib 证书校验失败时（python.org 装的 Python 没跑过 Install Certificates）退回 curl；curl 不读 macOS 系统代理，把代理显式传过去"""
    if not shutil.which("curl"):
        raise Fail("证书校验失败，系统里也没有 curl", "macOS 上运行 /Applications/Python 3.x/Install Certificates.command，或改用系统自带的 /usr/bin/python3", code=1)
    cmd = ["curl", "-sS", "--max-time", str(timeout), "-A", UA, "-H", "Accept: application/json", "-w", "\n%{http_code}"]
    px = _proxy_for(url)
    if px:
        cmd += ["--proxy", px]
    p = subprocess.run(cmd + [url], capture_output=True)
    if p.returncode != 0:
        raise Fail("请求失败：" + (p.stderr.decode("utf-8", "replace").strip() or "curl 出错"), NET_HINT)
    body, _, code = p.stdout.rpartition(b"\n")
    try:
        return int(code or 0), body.decode("utf-8", "replace")
    except ValueError:
        return 0, ""


def _retry_after(v):
    try:
        return max(1, min(30, int(v)))
    except (TypeError, ValueError):
        try:
            return max(1, min(30, int(parsedate_to_datetime(v).timestamp() - time.time())))
        except Exception:
            return 10


def get(url, timeout=25, retry=True):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if e.code == 429 and retry:
            time.sleep(_retry_after(e.headers.get("Retry-After")))
            return get(url, timeout, retry=False)
        try:
            return e.code, e.read().decode("utf-8", "replace")
        except Exception:
            return e.code, ""
    except urllib.error.URLError as e:
        if isinstance(e.reason, ssl.SSLError) or "CERTIFICATE" in str(e.reason).upper():
            return _curl(url, timeout)
        raise Fail("连不上 %s：%s" % (urllib.parse.urlsplit(url).netloc, e.reason), NET_HINT)
    except (TimeoutError, OSError) as e:
        raise Fail("请求超时或网络出错：%s" % e, NET_HINT)


def get_json(url):
    code, body = get(url)
    host = urllib.parse.urlsplit(url).netloc
    if not body.strip():
        return code, {}
    try:
        j = json.loads(body)
    except ValueError:
        if code == 200:  # 200 却不是 JSON：多半是代理 / 网关的拦截页、认证页
            raise Fail("%s 返回的不是数据（可能被代理或网关拦了）" % host, NET_HINT, code=5)
        return code, {}
    if not isinstance(j, dict):
        raise Fail("%s 返回的格式不对" % host, "稍后重试", code=5)
    return code, j


def _qs(params):
    q = {k: v for k, v in params.items() if v not in (None, "")}
    return ("?" + urllib.parse.urlencode(q)) if q else ""


def fx(path, **params):
    code, j = get_json(FX + path + _qs(params))
    inner = j.get("code") if isinstance(j.get("code"), int) else None
    if code == 404 or inner == 404:
        raise Fail("没找到（推文删了、账号不存在 / 改名了，或者是受保护账号）", code=4)
    if code in (401, 403) or inner in (401, 403):
        raise Fail("看不了（受保护账号或受限内容）", code=4)
    if code == 429 or inner == 429:
        raise Fail("请求太频繁，被限流了，过一两分钟再试", code=5)
    if code != 200 or (inner is not None and inner >= 400):
        raise Fail("数据源返回 %s%s" % (inner or code, "：" + str(j.get("message")) if j.get("message") else ""), "公开接口偶尔抽风，稍后重试", code=5)
    return j


def lbz(path, **params):
    code, j = get_json(LBZ + path + _qs(params))
    if code != 200:
        raise Fail(j.get("error") or "蓝不住返回 %s" % code, j.get("recommend") or j.get("check_url"), code=4 if code == 404 else 5)
    return j


# ---------------- 输入解析 ----------------

# X 和常见镜像的域名（前面要是开头、// 或子域名的点，免得 box.com 里的 x.com 也被认出来）
HOST = r"(?:^|//|\.)(?:x|twitter|fxtwitter|vxtwitter|fixupx|fixvx)\.com/"
RESERVED = {"home", "i", "search", "explore", "intent", "settings", "notifications", "messages", "compose", "hashtag",
            "share", "login", "logout", "signup", "tos", "privacy", "about", "jobs", "download", "account", "lists",
            "bookmarks", "communities", "premium", "following", "followers", "status"}
_FULLWIDTH = str.maketrans({"＠": "@", "／": "/", "：": ":", "？": "?", "＃": "#"})


def _norm(s):
    return (s or "").strip().translate(_FULLWIDTH)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def _expand_tco(s):
    """t.co 短链接：不跟随跳转，只读 Location"""
    url = s if s.startswith("http") else "https://" + s
    try:
        urllib.request.build_opener(_NoRedirect).open(urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA}), timeout=15)
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location")
        if loc:
            return loc
    except Exception:
        pass
    raise Fail("短链接展开失败：%s" % s, "给原始的推文或主页链接", code=2)


def tweet_id(s, _depth=0):
    s = _norm(s)
    if re.fullmatch(r"\d{5,25}", s):
        return s
    m = re.search(HOST + r"(?:[^/?#\s]+/)*status(?:es)?/(\d{1,25})(?!\d)", s)  # 链接里的 id 不限位数（最早的推 id 只有两位） or re.search(r"lanbuzhu\.org/piyao/(\d{5,25})(?!\d)", s)
    if m:
        return m.group(1)
    if _depth == 0 and re.search(r"(?:^|//)t\.co/\w+", s):
        return tweet_id(_expand_tco(re.search(r"(?:https?://)?t\.co/\w+", s).group(0)), 1)
    raise Fail("认不出推文：%s" % s, "给推文链接（x.com/账号/status/数字）或推文 id", code=2)


def handle(s, _depth=0):
    s = _norm(s)
    m = re.search(HOST + r"(?:#!/)?@?([A-Za-z0-9_]{1,15})(?=[/?#]|$)", s) or re.search(r"lanbuzhu\.org/(?:data/a|u)/@?([A-Za-z0-9_]{1,15})(?=[/?#]|$)", s)
    if m:
        h = m.group(1)
    elif _depth == 0 and re.search(r"(?:^|//)t\.co/\w+", s):
        return handle(_expand_tco(re.search(r"(?:https?://)?t\.co/\w+", s).group(0)), 1)
    else:
        h = s.lstrip("@").rstrip("/")
    if not re.fullmatch(r"[A-Za-z0-9_]{1,15}", h) or h.lower() in RESERVED:
        raise Fail("认不出账号：%s" % s, "给 @账号 或主页链接", code=2)
    return h


def lang_code(s):
    c = (s or "").strip().lower().replace("_", "-").split("-")[0]
    if not re.fullmatch(r"[a-z]{2,3}", c):
        raise Fail("语言写法不对：%s" % s, "用两三个字母的语言代码，比如 zh、en、ja", code=2)
    return c


# ---------------- 输出整理 ----------------

def iso(ts, fallback=None):
    try:
        return datetime.fromtimestamp(int(ts), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return fallback


def clean(d):
    return {k: v for k, v in d.items() if v not in (None, "", [], {})}


def _joined(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y").astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return s


def _lower(x):
    return (x or "").lower() if isinstance(x, str) else ""


def user_out(u, full=False):
    if not isinstance(u, dict):
        return None
    ver = u.get("verification") if isinstance(u.get("verification"), dict) else {}
    o = {
        "handle": u.get("screen_name"), "name": u.get("name"), "id": u.get("id"),
        "followers": u.get("followers"), "following": u.get("following"),
        "verified": bool(ver.get("verified")) or None, "verified_type": ver.get("type") if ver.get("verified") else None,
        "protected": u.get("protected") or None,
    }
    if full:
        site = u.get("website")
        o.update({
            "bio": u.get("description"), "location": u.get("location"), "website": site.get("url") if isinstance(site, dict) else site,
            "tweets": u.get("statuses"), "likes": u.get("likes"), "media_count": u.get("media_count"),
            "joined": _joined(u.get("joined")),
            "avatar": re.sub(r"_normal(\.\w+)$", r"_400x400\1", u.get("avatar_url") or "") or None, "banner": u.get("banner_url"),
            "url": "https://x.com/%s" % u.get("screen_name"),
        })
        ab = u.get("about_account") if isinstance(u.get("about_account"), dict) else {}
        if ab:
            uc = ab.get("username_changes") if isinstance(ab.get("username_changes"), dict) else {}
            o["about"] = clean({
                "based_in": ab.get("based_in"),  # X「关于此账号」里的所在地
                "based_in_accurate": ab.get("location_accurate"),  # false = X 提示所在地可能不准（比如用了 VPN）
                "signed_up_via": ab.get("source"), "signup_country_accurate": ab.get("created_country_accurate"),
                "username_changes": uc.get("count"), "last_username_change": uc.get("last_changed_at"),
            })
    return clean(o)


def media_out(t):
    out = []
    md = t.get("media") if isinstance(t.get("media"), dict) else {}
    for m in md.get("all") or []:
        if not isinstance(m, dict):
            continue
        x = {"type": m.get("type"), "url": m.get("url")}
        if m.get("type") in ("video", "gif"):
            x["thumb"] = m.get("thumbnail_url")
            if isinstance(m.get("duration"), (int, float)):
                x["seconds"] = round(m["duration"], 1)
        out.append(clean(x))
    return out


def article_text(a):
    """X 长文（Article）的正文：content.blocks 是 Draft.js 的段落"""
    lines = []
    content = a.get("content") if isinstance(a.get("content"), dict) else {}
    for b in content.get("blocks") or []:
        if not isinstance(b, dict) or b.get("type") == "atomic":
            continue
        tx = (b.get("text") or "").strip()
        if not tx:
            continue
        ty = b.get("type") or ""
        prefix = "## " if ty.startswith("header") else "- " if ty == "unordered-list-item" else "1. " if ty == "ordered-list-item" else "> " if ty == "blockquote" else ""
        lines.append(prefix + tx)
    return "\n".join(lines)


def tweet_out(t, depth=0, full_article=False, drop_quote_of=None):
    if not isinstance(t, dict):
        return None
    a = t.get("author") if isinstance(t.get("author"), dict) else {}
    rt = t.get("replying_to") if isinstance(t.get("replying_to"), dict) else None
    note = t.get("community_note")
    art = t.get("article") if isinstance(t.get("article"), dict) else None
    poll = t.get("poll") if isinstance(t.get("poll"), dict) else None
    rb = t.get("reposted_by") if isinstance(t.get("reposted_by"), dict) else None
    text = t.get("text")
    if text is None and isinstance(t.get("raw_text"), dict):
        text = t["raw_text"].get("text")
    o = {
        "id": t.get("id"), "url": t.get("url") or "https://x.com/%s/status/%s" % (a.get("screen_name"), t.get("id")),
        "created_at": iso(t.get("created_timestamp"), t.get("created_at")),
        "author": user_out(a),
        "text": text, "lang": t.get("lang"),
        "views": t.get("views"), "likes": t.get("likes"), "reposts": t.get("reposts"), "quotes": t.get("quotes"),
        "replies": t.get("replies"), "bookmarks": t.get("bookmarks"),
        "reply_to": clean({"handle": rt.get("screen_name"), "id": rt.get("status")}) if rt else None,
        "reposted_by": rb.get("screen_name") if rb else None,
        "media": media_out(t),
        "community_note": (note.get("text") if isinstance(note, dict) else note) or None,
        "poll": [clean({"label": c.get("label"), "votes": c.get("count"), "percent": c.get("percentage")}) for c in (poll.get("choices") or []) if isinstance(c, dict)] if poll else None,
        "sensitive": t.get("possibly_sensitive") or None,
    }
    if art:
        ao = {"title": art.get("title"), "preview": art.get("preview_text")}
        if full_article:
            body = article_text(art)
            ao["text"] = body[:ARTICLE_MAX]
            if len(body) > ARTICLE_MAX:
                ao["truncated"] = True
        else:
            ao["note"] = "这是长文，用 tweet 命令读这条推能拿到全文"
        o["article"] = clean(ao)
    q = t.get("quote") if isinstance(t.get("quote"), dict) else None
    if q and depth < 1 and q.get("id") != drop_quote_of:
        o["quoted"] = tweet_out(q, depth + 1)
    return clean(o)


_INVIS = re.compile("[\U000E0000-\U000E007F‪-‮⁦-⁩​‌‎‏⁠﻿]")


def scrub(v):
    """去掉看不见的字符（Unicode 标签字符、双向控制符、零宽字符）：它们能藏人眼看不见、模型却读得到的指令"""
    if isinstance(v, str):
        return _INVIS.sub("", v)
    if isinstance(v, list):
        return [scrub(x) for x in v]
    if isinstance(v, dict):
        return {k: scrub(x) for k, x in v.items()}
    return v


def emit(obj):
    sys.stdout.write(json.dumps(scrub(obj), ensure_ascii=False, indent=1 if PRETTY else None, separators=None if PRETTY else (",", ":")) + "\n")
    sys.stdout.flush()


# ---------------- 翻页 ----------------

def _key(it):
    rb = it.get("reposted_by") if isinstance(it.get("reposted_by"), dict) else {}
    return (it.get("id") or it.get("screen_name"), rb.get("screen_name"))


def paged(path, limit, key="results", keep=None, old=None, **params):
    """FxTwitter v2 的列表接口：results + cursor.bottom。返回 (列表, more)，more = 还有没拿的。
    keep(item) 为 False 的不要、也不计数；old(item) 为 True = 早于截止时间：跳过，连着 3 条都是旧的就停
    （时间线最上面可能是很久以前的置顶推，不能见旧就停）"""
    out, seen, cursor, pages, streak = [], set(), None, 0, 0
    if limit <= 0:
        return out, False
    while pages < 50:
        j = fx(path, cursor=cursor, **params)
        pages += 1
        items = j.get(key) or []
        fresh = 0
        for it in items:
            if not isinstance(it, dict):
                continue
            k = _key(it)
            if k in seen:
                continue
            seen.add(k)
            fresh += 1
            if keep and not keep(it):
                continue
            if old and old(it):
                streak += 1
                if streak >= 3:
                    return out, False
                continue
            streak = 0
            if len(out) >= limit:
                return out, True
            out.append(it)
        cur = j.get("cursor") if isinstance(j.get("cursor"), dict) else {}
        cursor = cur.get("bottom")
        if not cursor or not fresh:
            return out, False
        if len(out) >= limit:
            return out, True
        time.sleep(PAGE_GAP)
    return out, True


# ---------------- 命令：实时 X 数据 ----------------

def _profile(h):
    j = fx("/2/profile/%s" % h, about_account=1)
    return user_out(j.get("user"), full=True)


def cmd_tweet(a):
    tid = tweet_id(a.target)
    res = {}
    if a.replies or a.thread:
        j = fx("/2/conversation/%s" % tid)
        st = j.get("status") if isinstance(j.get("status"), dict) else None
        if not st:
            raise Fail("没找到这条推（删了，或作者是受保护账号）", code=4)
        res["tweet"] = tweet_out(st, full_article=True)
        root_author = _lower((st.get("author") or {}).get("screen_name"))
        if a.thread:
            res["thread"] = [tweet_out(t) for t in (j.get("thread") or []) if isinstance(t, dict) and t.get("id") != tid and _lower((t.get("author") or {}).get("screen_name")) == root_author]
        if a.replies:
            reps = [t for t in (j.get("replies") or []) if isinstance(t, dict) and t.get("id") != tid]
            first, more = len(reps), len(reps) > a.replies
            if len(reps) < a.replies:  # 第一页不够：按对话搜（按时间倒序），拿满 N 条再去重
                extra, more = paged("/2/search", a.replies, q="conversation_id:%s" % tid, feed="latest", count=40)
                have = {t.get("id") for t in reps}
                reps += [t for t in extra if t.get("id") not in have and t.get("id") != tid]
            rows = []
            for t in reps[: a.replies]:
                o = tweet_out(t)
                o["direct"] = (o.get("reply_to") or {}).get("id") == tid  # true = 直接回复这条推；false = 楼中楼（回复的是别人的回复，那条不一定在列表里）
                if _lower((t.get("author") or {}).get("screen_name")) == root_author:
                    o["by_author"] = True
                rows.append(o)
            res["replies"] = rows
            res["replies_info"] = {
                "on_x": st.get("replies"), "returned": len(rows), "more": bool(more or len(reps) > a.replies),
                "order": ("前 %d 条是 X 回复区的默认顺序（按相关度），后面的按时间倒序" % first) if len(rows) > first else "X 回复区的默认顺序（按相关度）",
                "note": "X 上显示的回复数含被隐藏 / 删掉 / 受保护账号的回复，拿不全是正常的",
            }
        if a.about and st.get("author"):
            res["author"] = _profile((st.get("author") or {}).get("screen_name"))
    else:
        j = fx("/2/status/%s" % tid, about_account=1 if a.about else None)
        st = j.get("status") if isinstance(j.get("status"), dict) else j.get("tweet") if isinstance(j.get("tweet"), dict) else None
        if not st:
            raise Fail("没找到这条推（删了，或作者是受保护账号）", code=4)
        res["tweet"] = tweet_out(st, full_article=True)
        if a.about:
            res["author"] = user_out(st.get("author"), full=True)
    if a.quotes:
        qs, more = paged("/2/status/%s/quotes" % tid, a.quotes, count=40)
        res["quotes"] = [tweet_out(t, drop_quote_of=tid) for t in qs]  # 引用里不再重复嵌一遍原推
        res["quotes_more"] = more
    if a.translate:
        res["translation"] = _translate(tid, lang_code(a.translate))
    emit(res)


def _translate(tid, lang):
    j = fx("/2/status/%s/%s" % (tid, lang))
    t = j.get("tweet") if isinstance(j.get("tweet"), dict) else j.get("status") if isinstance(j.get("status"), dict) else {}
    tr = t.get("translation") if isinstance(t.get("translation"), dict) else {}
    if not tr.get("text"):
        why = "原文就是这种语言（lang=%s）" % t.get("lang") if _lower(t.get("lang")) == lang else "X 没有给这条推的译文（可能不支持这种语言）"
        return {"to": lang, "text": None, "note": "没有译文：" + why}
    return clean({"to": lang, "from": tr.get("source_lang"), "text": tr.get("text")})


def cmd_translate(a):
    tid = tweet_id(a.target)
    emit({"id": tid, "translation": _translate(tid, lang_code(a.to))})


def cmd_user(a):
    emit({"user": _profile(handle(a.target))})


def cmd_tweets(a):
    h = handle(a.target)
    hl = h.lower()
    since = _when(a.since) if a.since else None

    def own(t):  # 本人发的（带回复的时间线会夹着别人的推当上下文，转推带的是原作者）
        return _lower((t.get("author") or {}).get("screen_name")) == hl and not t.get("reposted_by")

    def my_repost(t):
        rb = t.get("reposted_by")
        return isinstance(rb, dict) and _lower(rb.get("screen_name")) == hl

    keep = lambda t: own(t) or (a.reposts and my_repost(t))
    old = (lambda t: own(t) and (t.get("created_timestamp") or 0) < since) if since else None
    path = "/2/profile/%s/%s" % (h, "media" if a.media else "statuses")
    items, more = paged(path, a.limit, keep=keep, old=old, count=40, with_replies="true" if a.replies else None)
    emit({"handle": h, "count": len(items), "more": more, "tweets": [tweet_out(t) for t in items]})


def _when(s):
    """2026-10-01（UTC 零点）/ 24h / 7d → Unix 秒"""
    m = re.fullmatch(r"(\d+)\s*([hd])", (s or "").strip().lower())
    if m:
        return int(time.time()) - int(m.group(1)) * (3600 if m.group(2) == "h" else 86400)
    try:
        return int(datetime.strptime(s.strip(), "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
    except (ValueError, AttributeError):
        raise Fail("时间要写成 2026-10-01、24h 或 7d：%s" % s, code=2)


def cmd_search(a):
    # X 的 since:/until: 按日期过滤不太准（实测 until: 不生效），换成按 Unix 秒的 since_time: / until_time:
    q = a.query
    if a.min_likes:
        q += " min_faves:%d" % a.min_likes
    if a.since:
        q += " since_time:%d" % _when(a.since)
    if a.until:
        q += " until_time:%d" % _when(a.until)
    items, more = paged("/2/search", a.limit, q=q, feed="top" if a.top else "latest", count=40)
    rows = [tweet_out(t) for t in items]
    if a.sort:
        rows.sort(key=lambda r: r.get(a.sort) or 0, reverse=True)
    res = {"query": q, "feed": "top" if a.top else "latest", "count": len(rows), "more": more, "tweets": rows}
    if a.sort:
        res["sorted_by"] = a.sort
        if more:
            res["note"] = "只在拿到的这 %d 条里排序；more 为 true 说明还有没拿的，要更全就加大 --limit 或提高 --min-likes" % len(rows)
    emit(res)


def cmd_follows(a, which):
    h = handle(a.target)
    items, more = paged("/2/profile/%s/%s" % (h, which), a.limit, count=100)
    emit({"handle": h, which: [user_out(u, full=a.full) for u in items], "count": len(items), "more": more, "order": "X 给的顺序"})


# ---------------- 命令：蓝不住的 X 中文区数据 ----------------

def cmd_stats(a):
    emit(lbz("/account/%s" % handle(a.target)))


def cmd_rank(a):
    emit(lbz("/rank", by=a.by, when=a.when, track=a.track, limit=a.limit))


def cmd_champions(a):
    emit(lbz("/champions", when=a.when))


def cmd_daily(a):
    if a.day and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a.day):
        raise Fail("日期要写成 2026-10-08", code=2)
    emit(lbz("/daily" + ("/" + a.day if a.day else "")))


def cmd_feed(a):
    emit(lbz("/feed", type=a.type, handle=handle(a.handle) if a.handle else None, page=a.page if not a.handle else None))


def cmd_hot(a):
    emit(lbz("/hot", hours=a.hours, sort=a.sort, track=a.track, limit=a.limit))


def cmd_topics(a):
    emit(lbz("/topics"))


def cmd_rumors(a):
    emit(lbz("/rumors", sort=a.sort, limit=a.limit))


def cmd_rumor(a):
    emit(lbz("/rumor/%s" % tweet_id(a.target)))


# ---------------- 入口 ----------------

class Parser(argparse.ArgumentParser):
    """参数写错时也输出 JSON（和别的错误一样），退出码 2"""

    def error(self, message):
        sub = self.prog.split(" ", 1)[1] + " " if " " in self.prog else ""
        emit({"error": "参数不对：" + message, "hint": "看用法：python3 x.py %s-h" % sub})
        sys.exit(2)


def _utf8_stdio():
    """Windows 控制台 / 管道默认是系统代码页（GBK、cp1252），打印中文、emoji 会崩"""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


TRACKS = ["ai", "crypto", "finance", "media"]


def main(argv=None):
    global PRETTY
    _utf8_stdio()
    argv = list(sys.argv[1:] if argv is None else argv)
    PRETTY = "--pretty" in argv  # 放在哪都行
    argv = [x for x in argv if x != "--pretty"]
    p = Parser(prog="x.py", description="读 X（Twitter）的数据：推文、对话、搜索、账号、时间线、关注列表、翻译；以及蓝不住的 X 中文区统计。输出 JSON，加 --pretty 缩进。")
    p.add_argument("--version", action="version", version="x-aggregate-data " + VERSION)
    sub = p.add_subparsers(dest="cmd", metavar="命令", parser_class=Parser)

    s = sub.add_parser("tweet", help="读一条推（链接或 id），可带回复、作者的整串、引用、翻译")
    s.add_argument("target")
    s.add_argument("--replies", type=int, default=0, metavar="N", help="带上 N 条回复")
    s.add_argument("--thread", action="store_true", help="带上作者自己接在后面的推（thread，不含这条本身）")
    s.add_argument("--quotes", type=int, default=0, metavar="N", help="带上 N 条引用这条推的推")
    s.add_argument("--translate", metavar="LANG", help="顺便翻译成某种语言，比如 zh、en")
    s.add_argument("--about", action="store_true", help="带上作者的完整资料（所在地、改名次数等）")
    s.set_defaults(fn=cmd_tweet)

    s = sub.add_parser("translate", help="翻译一条推（X 自带的翻译）")
    s.add_argument("target")
    s.add_argument("--to", default="zh", help="目标语言，默认 zh")
    s.set_defaults(fn=cmd_translate)

    s = sub.add_parser("user", help="账号资料：粉丝、关注、发帖数、注册时间、简介、所在地、改名次数")
    s.add_argument("target")
    s.set_defaults(fn=cmd_user)

    s = sub.add_parser("tweets", help="账号最近的推（时间线），默认只要本人发的原创 / 引用")
    s.add_argument("target")
    s.add_argument("--limit", type=int, default=20, help="最多几条，默认 20")
    s.add_argument("--since", help="只要这之后的：2026-10-01（UTC 零点）/ 24h / 7d")
    s.add_argument("--replies", action="store_true", help="包括 TA 回复别人的")
    s.add_argument("--reposts", action="store_true", help="包括 TA 转推的")
    s.add_argument("--media", action="store_true", help="只看带图 / 视频的")
    s.set_defaults(fn=cmd_tweets)

    s = sub.add_parser("search", help="搜推文，支持 X 的搜索语法（from: min_faves: lang: filter: url: 等）")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=20, help="最多几条，默认 20")
    s.add_argument("--since", help="这之后的：2026-10-01（UTC 零点）/ 24h / 7d")
    s.add_argument("--until", help="这之前的：2026-10-08（UTC 零点，不含当天）/ 24h（24 小时前）")
    s.add_argument("--min-likes", type=int, metavar="N", help="至少 N 个赞（等于在查询里加 min_faves:N）")
    s.add_argument("--sort", choices=["likes", "views", "reposts", "replies", "bookmarks", "quotes"], help="拿到之后按这个数字从高到低排（先用 --limit 多拿一些）")
    s.add_argument("--top", action="store_true", help="用 X 的热门排序（默认按时间）；热门不等于点赞最多，可能混进时间范围外、不太相关的推")
    s.set_defaults(fn=cmd_search)

    for which, desc in (("following", "TA 关注的人"), ("followers", "关注 TA 的人")):
        s = sub.add_parser(which, help=desc + "（X 给的顺序）")
        s.add_argument("target")
        s.add_argument("--limit", type=int, default=50, help="最多几个，默认 50")
        s.add_argument("--full", action="store_true", help="带简介、注册时间等完整资料")
        s.set_defaults(fn=lambda a, w=which: cmd_follows(a, w))

    s = sub.add_parser("stats", help="【蓝不住】账号每日数据：今天 / 昨日 / 7 天 / 30 天的曝光、发帖、评论、涨粉，近 30 天走势、名次、夺冠、动态")
    s.add_argument("target")
    s.set_defaults(fn=cmd_stats)

    s = sub.add_parser("rank", help="【蓝不住】X 中文区账号排行")
    s.add_argument("--by", default="views", choices=["views", "posts", "replies", "gain", "fans", "avgv", "maxv"], help="views 推文曝光 / posts 发帖 / replies 评论 / gain 涨粉 / fans 粉丝 / avgv 帖均曝光 / maxv 最高单帖")
    s.add_argument("--when", default="yday", choices=["today", "yday", "7d", "30d"], help="默认 yday（昨天，数据最全）；7d / 30d 含还没结束的今天")
    s.add_argument("--track", choices=TRACKS, help="赛道")
    s.add_argument("--limit", type=int, default=20, help="1–50，默认 20")
    s.set_defaults(fn=cmd_rank)

    s = sub.add_parser("champions", help="【蓝不住】发帖 / 评论 / 涨粉 / 曝光四个冠军和前 5")
    s.add_argument("--when", default="yday", choices=["today", "yday", "7d"], help="默认 yday")
    s.set_defaults(fn=cmd_champions)

    s = sub.add_parser("daily", help="【蓝不住】X 中文区日报（默认最新一期）")
    s.add_argument("day", nargs="?", help="哪一期：YYYY-MM-DD")
    s.set_defaults(fn=cmd_daily)

    s = sub.add_parser("feed", help="【蓝不住】大V动态：删帖（带原文）、改名改简介换头像、粉丝异动、互相转发引用、爆款")
    s.add_argument("--type", default="key", choices=["key", "delete", "profile", "fans", "interact", "viral", "all"], help="key 要闻 / delete 删帖 / profile 资料 / fans 粉丝 / interact 互动 / viral 爆款 / all")
    s.add_argument("--handle", help="只看某个账号（最近 30 条）")
    s.add_argument("--page", type=int, default=1, help="翻页（1–10，看全部账号时用）")
    s.set_defaults(fn=cmd_feed)

    s = sub.add_parser("hot", help="【蓝不住】X 中文区热帖")
    s.add_argument("--hours", default="24", choices=["3", "6", "12", "24"])
    s.add_argument("--sort", default="heat", choices=["heat", "views"], help="heat 现在最热 / views 曝光最高")
    s.add_argument("--track", choices=TRACKS, help="赛道")
    s.add_argument("--limit", type=int, default=20, help="1–30")
    s.set_defaults(fn=cmd_hot)

    s = sub.add_parser("topics", help="【蓝不住】X 中文区正在火的话题")
    s.set_defaults(fn=cmd_topics)

    s = sub.add_parser("rumors", help="【蓝不住】谣言库（疑似谣言的推，仅供参考）")
    s.add_argument("--sort", default="heat", choices=["heat", "score", "new"])
    s.add_argument("--limit", type=int, default=20, help="1–20")
    s.set_defaults(fn=cmd_rumors)

    s = sub.add_parser("rumor", help="【蓝不住】某条推的谣言检测报告（有人检测过才有）")
    s.add_argument("target")
    s.set_defaults(fn=cmd_rumor)

    a = p.parse_args(argv)
    if not a.cmd:
        p.print_help()
        return 2
    for k in ("limit", "replies", "quotes"):
        if getattr(a, k, None) is not None:
            setattr(a, k, max(0, min(getattr(a, k), 500)))
    try:
        a.fn(a)
        return 0
    except Fail as e:
        emit(clean({"error": e.msg, "hint": e.hint}))
        return e.code
    except KeyboardInterrupt:
        return 130
    except Exception as e:  # 兜底：别把一大段堆栈丢给 agent
        emit({"error": "脚本出错：%s: %s" % (type(e).__name__, e), "hint": "可以到 https://github.com/qianyubtc/X-Aggregate-Data/issues 反馈"})
        return 1


if __name__ == "__main__":
    sys.exit(main())
