---
name: indonesian-tts
description: Indonesian VO, free Piper draft plus ElevenLabs final.
---

# Indonesian TTS

Two engines, different jobs. Piper for drafts and timing; ElevenLabs for the final take, because Piper sounds like a news reader and cannot carry tension.

## Piper (free, offline, 4s for a 25s script)

Setup lives at `~/tts`:

```bash
uv venv ~/tts/venv --python 3.12
uv pip install --python ~/tts/venv/bin/python piper-tts
curl -sL -o ~/tts/models/id.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx
curl -sL -o ~/tts/models/id.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx.json
```

Synthesize (always clear PYTHONPATH; the host leaks a 3.14 site-packages into 3.12 and breaks numpy):

```bash
env -u PYTHONPATH ~/tts/venv/bin/python -m piper -m ~/tts/models/id.onnx \
  -f out.wav --length-scale 0.80 -i script.txt
```

`--length-scale 0.80` lands a 370-character script at ~26s, matching ElevenLabs at speed 1.2.

## Traps that actually break Piper

Write the script the way it is spoken, never in chat shorthand:

- `gw` makes Piper say "gewe". Write `gue`.
- `tau` becomes `tahu`.
- `ke parkiran` gets slurred into "kepakiran"; test any two-word place or direction phrase with ASR before shipping.
- Numbers are fine but ASR may transcribe "sembilan" as "9"; do not chase that as an error.

## Verifying pronunciation without ears

Install once: `uv pip install --python ~/tts/venv/bin/python faster-whisper`. The bundled PyAV is incompatible (`TypeError: open() got an unexpected keyword argument 'metadata_errors'`), so decode with ffmpeg and pass a numpy array, never a path:

```python
raw = subprocess.run(["ffmpeg","-v","error","-i",p,"-f","s16le","-ac","1","-ar","16000","-"],
                     capture_output=True).stdout
m.transcribe(np.frombuffer(raw, np.int16).astype(np.float32)/32768.0, language="id")
```

Then diff the transcript against the script. Report the pronunciation errors, not a WER number: whisper-small inserts and drops words on expressive audio, so WER alone will make ElevenLabs look worse than it is.

Check the **final muxed MP4** as well, not just the rendered take:

```bash
ffmpeg -hide_banner -i out/final.mp4 -af "silencedetect=noise=-35dB:d=0.45" -f null -
```

`adelay=200|200,apad` with `-shortest` can leave a dead tail or clip the last syllable, so the MP3 can be perfect while the delivered file is not. Gaps longer than ~0.45 s that are not in the script are the tell.

## What does not work

- MeloTTS: no Indonesian model (EN/ES/FR/ZH/JP/KR only). Do not install it for Indonesian work.
- RNNoise: for cleaning microphone recordings. Synthetic TTS is already clean, so it adds nothing to this pipeline.

## Never stack speed on speed

Choppy, jump-cut narration is usually self-inflicted: generating at `speed: 1.28` and then running
`atempo=1.15` on top. Two compressions delete the breath between clauses and clip consonants.
Generate once at 1.1-1.15, apply atempo only above ~40 s of audio, and never above 1.06.

Prosody follows the punctuation you write. Short adjacent sentences ("HP gw bunyi. Dari pemesannya.
Jangan ngetok pintu.") read as machine-gun bursts; link them with commas and connectors ("Sebelum gw
turun dari motor, HP gw bunyi, pesan dari pemesannya, isinya cuma satu kalimat: jangan ngetok pintu")
so the voice carries one breath across three ideas. Lower `style` to ~0.12 and raise `stability` to
~0.52 for storytelling: high style inserts micro-pauses that sound like cuts.

## Verdict from the user

He heard both A/B clips and picked ElevenLabs. Do not propose Piper as a replacement again; use it only for silent drafts and timing.

## Default workflow for a video

Draft the whole VO in Piper to lock timing and shot lengths, then regenerate the final take in ElevenLabs with the same text. One paid call instead of five.
