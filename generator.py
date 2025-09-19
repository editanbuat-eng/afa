#!/usr/bin/env python3
import json
import random
import click
from pathlib import Path
from jinja2 import Template
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

@click.command()
@click.option('--template', '-t', required=True, help='Path ke prompts.json')
@click.option('--out', '-o', default='results.json', help='File output')
@click.option('--count', '-c', default=1, help='Jumlah prompt yang di-generate')
@click.option('--mode', '-m', default='text', type=click.Choice(['text','image','video']),
              help='Mode output: text, image, atau video')
def main(template, out, count, mode):
    tpl_path = Path(template)
    data = json.loads(tpl_path.read_text(encoding='utf-8'))
    templates = data.get('templates', [])
    results = []

    for i in range(count):
        chosen = random.choice(templates)
        raw = json.dumps(chosen)
        rendered = Template(raw).render()
        obj = json.loads(rendered)
        prompt = obj["description"]

        if mode == "text":
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            obj["gemini_output"] = response.text

        elif mode == "image":
            model = genai.GenerativeModel("gemini-pro-vision")
            response = model.generate_content(prompt)
            obj["gemini_output"] = response.candidates[0].content.parts[0].text

        elif mode == "video":
            from PIL import Image
            import ffmpeg

            frames_dir = Path("frames")
            frames_dir.mkdir(exist_ok=True)

            frame_path = frames_dir / f"frame_{i+1:03d}.png"
            img = Image.new("RGB", (512, 512), color=(i*40 % 255, 100, 150))
            img.save(frame_path)

            obj["frame"] = str(frame_path)
            obj["gemini_desc"] = f"Frame {i+1} for: {prompt}"

            results.append(obj)

            if i == count - 1:
                (
                    ffmpeg
                    .input(str(frames_dir / "frame_%03d.png"), framerate=30)
                    .output("output.mp4")
                    .run(overwrite_output=True)
                )
                print("🎬 Video generated: output.mp4")
            continue

        obj['instance_id'] = f"{chosen['id']}-{i+1}"
        results.append(obj)

    Path(out).write_text(json.dumps({'results': results}, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ Saved {len(results)} prompts to {out}")

if __name__ == '__main__':
    main()
