#!/usr/bin/env python3
"""Record a headless Chromium page to a JPEG frame sequence via CDP screencast.

Usage:
  python3 cdp_screencast.py --url file:///abs/index.html --out frames --duration 9 \
      --width 1200 --height 675 [--port 9333] [--quality 92] [--settle 1.2]

Frames land as <out>/f0000.jpg ... ; encode them with the ffmpeg line in SKILL.md.
Requires: chromium on PATH, python websockets.
"""
import argparse, asyncio, base64, json, os, subprocess, time, urllib.request

import websockets


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--out", default="frames")
    p.add_argument("--duration", type=float, default=8.0)
    p.add_argument("--width", type=int, default=1200)
    p.add_argument("--height", type=int, default=675)
    p.add_argument("--port", type=int, default=9333)
    p.add_argument("--quality", type=int, default=92)
    p.add_argument("--settle", type=float, default=1.2, help="seconds to wait after navigate")
    p.add_argument("--browser", default="chromium")
    return p.parse_args()


async def find_target(port, tries=50):
    for _ in range(tries):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=1))
            for t in tabs:
                if t.get("type") == "page":
                    return t["webSocketDebuggerUrl"]
        except Exception:
            pass
        await asyncio.sleep(0.2)
    return None


async def run(a):
    os.makedirs(a.out, exist_ok=True)
    for f in os.listdir(a.out):
        os.remove(os.path.join(a.out, f))

    proc = subprocess.Popen(
        [a.browser, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
         f"--window-size={a.width},{a.height}", f"--remote-debugging-port={a.port}", a.url],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws_url = await find_target(a.port)
        if not ws_url:
            raise SystemExit("no devtools target (is chromium on PATH?)")

        n = 0
        async with websockets.connect(ws_url, max_size=20_000_000) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Page.navigate", "params": {"url": a.url}}))
            await asyncio.sleep(a.settle)
            await ws.send(json.dumps({"id": 3, "method": "Page.startScreencast", "params": {
                "format": "jpeg", "quality": a.quality,
                "maxWidth": a.width, "maxHeight": a.height, "everyNthFrame": 1}}))
            t0 = time.time()
            while time.time() - t0 < a.duration:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=2)
                except asyncio.TimeoutError:
                    continue
                msg = json.loads(raw)
                if msg.get("method") == "Page.screencastFrame":
                    p = msg["params"]
                    with open(os.path.join(a.out, f"f{n:04d}.jpg"), "wb") as fh:
                        fh.write(base64.b64decode(p["data"]))
                    n += 1
                    await ws.send(json.dumps({"id": 100 + n, "method": "Page.screencastFrameAck",
                                              "params": {"sessionId": p["sessionId"]}}))
            await ws.send(json.dumps({"id": 999, "method": "Page.stopScreencast"}))
        elapsed = max(time.time() - t0, 0.001)
        print(f"frames: {n}  span: {elapsed:.2f}s  fps: {n / elapsed:.2f}")
        even_h = a.height + a.height % 2
        print("encode with: ffmpeg -y -framerate "
              f"{n / elapsed:.2f} -i {a.out}/f%04d.jpg -vf pad={a.width}:{even_h}:0:0:black "
              "-c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart out.mp4")
    finally:
        proc.kill()


if __name__ == "__main__":
    asyncio.run(run(args()))
