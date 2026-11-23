---
name: study-plan-coaching
description: "Use when Do asks to plan his study sessions."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [study, schedule, calendar, reminders, career, learning]
    related_skills: [google-calendar-ops, hermes-cron-automation, cv-tailoring-and-ats, job-listing-hunter]
---

# Study plan coaching for Do

## When to use

"besok jadwalin dong", "materi apa yang perlu gw pelajari", "ingetin gw belajar", "cek cekin materi pembelajaran".

## Non-negotiables

1. **Answer key NEVER lives in the same file as the exercises.** He reads the key first and then mistakes recognition for recall (his words: "gw cuma ke inget kalau liat kunci jawaban"). Ship three files: `LATIHAN.md` (questions only), `KUNCI.md` (answers, open last), `CONTEKAN.md` (syntax reference + a worked "decompose in plain language" example, allowed open anytime — memorising syntax is not the skill).
2. **Read his calendar before scheduling.** Exam and class times come from Google Calendar; honour the 90-minute commute and "sampe rumah jam 8 malam" on exam days, so evening sessions start 20:30, not 17:30. Interpreter: `~/.hermes/hermes-agent/venv/bin/python` (system python lacks googleapiclient); the `google_api.py` wrapper under-reports, so page `events().list()` directly. Calendar id is the email `your-email@example.com`; always pass `+07:00`.
3. **Reminders = one-shot cron jobs, never scanners.** One tiny `no_agent` echo script per session in `~/.hermes/scripts/` (`reminder_*.sh`); `bash -n` and actually run it to see the exact text before creating the job. Times: a few minutes before each block, plus one for leaving the house before an exam.
4. **Write the plan twice:** Google Calendar events (dedupe by summary first; `reminders.overrides` popup 10-15 min) and a markdown file under `~/.hermes/career/` he can open on the phone. **Re-read the calendar AFTER your own edits inside the same script, before the dedupe test** — a summary list captured before you repurpose tonight's slot still holds that event, so the legitimate new insert (the displaced session's new date) gets skipped as a duplicate and disappears without any error. Dedupe against live state, never against a snapshot taken earlier in the same run.
5. **Verify every resource link with `curl -s -o /dev/null -w '%{http_code}'`** before sending. A dead link is worse than no link.
6. **Light load on exam days.** Protect the exam-prep slot; move the third session to the weekend instead of stacking it.

## Priority order for his lane (AI implementation & automation, finance/accounting, employed under a system)

1. Pajak dasar — biggest gap, and almost every accounting posting touches it. Free source: `pajak.go.id/coretaxpedia`.
2. SQL refresh — he has studied it, so it returns fast. Practise on his own SQLite data.
3. Excel lanjut + Power Query — small gap, 3 weekends.
4. Power BI — campus basics exist; skip the course, demand one published dashboard.
5. Accurate — CAP/CADE procedures state a 75 pass mark and a 3-month retake window, **no expiry**; don't let him re-pay for an exam he already passed.
6. Power Automate, then n8n — corporate Indonesia runs Microsoft 365, so Power Automate first.
7. TOEFL — separate track (graduation requirement, not a job skill); he must ask BAAK/prodi which test and minimum score is accepted.

Rule governing all of it: every stage must end in an artifact someone else can open. The certificate only reinforces; the artifact is the requirement.

## Exam-prep kit (the night before an exam)

Trigger: "besok gw ujian, jadi gw mau bljr", or he answers a study reminder saying tomorrow is an exam.
Do NOT stack the load: repurpose that night's scheduled session into exam prep and MOVE the displaced
session (SQL / Excel) to the weekend or Sunday evening — calendar and reminder both, and keep exactly
one session per night.

1. Take the exam facts from the calendar, never from memory: subject, room, start time. Then build the kit
   at `~/.hermes/career/<course>_uts/` with the same three-file split as the SQL sandbox — `CONTEKAN.md`
   (concept map + formulas + the structure of a full-mark answer + the classic traps; open anytime),
   `LATIHAN.md` (questions only, 6-8 items, 3-4 of them carrying most of the marks), `KUNCI.md`
   (worked steps, not just final numbers).
2. **Compute every key value in one script, then assert the strings appear in `KUNCI.md`.** That assert
   pass is what catches a hand-typed key drifting from the formula (a rounded `1.133.000` where the formula
   gives `1.133.333`). Never ship a key you did not recompute.
3. Include one case question, not only calculations: a three-candidate comparison table he must compute
   unit economics for and then defend a pick WITH its main risk. That mirrors how the marks are actually
   distributed in a business-course UTS.
4. Scope honesty: no official syllabus is available, so state in the delivery message which framework the
   kit is built from and offer to rewrite it if the lecturer's emphasis differs. Unlabelled content reads as
   "this is the lecturer's material" and he will not trust it.
5. Ship the 25-minute fallback every time: name the exact sections to read and the 3 exercises to do. He
   starts late more often than not.
6. Exam-day reminders: a morning review one (re-read the cheat sheet, redo 3 exercises from memory) and a
   leave-for-campus one fired ~10 minutes before he must walk out (90-minute commute, target arriving
   20-30 minutes early). Carry any other deadline that falls that day as the last line of the morning
   reminder instead of creating another job.

## Materials already built

`~/.hermes/career/sql_sandbox/` — `buat_db.py` generates `accounting_practice.db` (SQLite) plus `csv/` with a fixed seed (42): 103 faktur penjualan, 49 pembelian, 116 pembayaran, 6 months. 10 SQL exercises and 5 Power Query/Excel tasks; all 10 answer queries verified running. Re-running the builder reproduces identical numbers, so his answers stay comparable to the key.
`~/.hermes/career/skill_plan_2026-10-14.md` — full tiered learning plan with the posting evidence behind each item.
`~/.hermes/career/BESOK_15-Okt-2026.md` — worked example of a dated day plan.
`~/.hermes/career/bdd05_uts/` — worked example of the exam-prep kit (Digital Business Valuation): CONTEKAN with the three valuation approaches + unit economics + DCF skeleton + dilution + traps, 8 exercises, key recomputed and asserted. Clone this shape and swap the subject matter for the next exam night.

## Coaching stance

Volunteer the next tiny step and offer to check his answer, because a static key cannot tell him which part of his logic is inverted — that is the gap he needs closed. Do not pile on work when he is tired or has an exam; a 30-minute fallback version belongs in every plan.

## Closing the day ("kata kata hari ini dong")

He asks for this before sleeping, usually right after a heavy planning turn. It is a short reflective
message, not a report of what the assistant did and not a pep talk.

Build it from the day's CONCRETE facts — what he actually decided, admitted, or finished — because
vague encouragement is the thing he distrusts. Shape that landed: open on the one real admission or
decision of the day (he chose the employed lane over working solo; he admitted he only "remembers"
SQL when the answer key is in front of him), reframe it as a specific, fixable gap instead of a
character flaw, then end on the one small next-day step that is already scheduled for him. Prose
paragraphs, Indonesian santai (gw/lu), no "-" bullets.

Never: a task checklist, a recap of tool work, hype about progress toward Rp100 juta, or a closing
question ("mau gw ...?").
