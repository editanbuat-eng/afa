# Veo3 Generator

Generator prompt & asset untuk **Veo 3** dengan integrasi Gemini API.

## Fitur
- Generate prompt teks (`--mode text`)
- Generate deskripsi/gambar (`--mode image`)
- Generate video konsisten (frame → video `.mp4`) (`--mode video`)

## Setup
1. Daftar API key di [Google AI Studio](https://aistudio.google.com/)
2. Simpan di file `.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Install deps:
   ```bash
   pip install -r requirements.txt
   ```

## Cara pakai
### Mode Teks
```bash
python src/generator.py --template prompts.json --out results.json --count 2 --mode text
```

### Mode Gambar
```bash
python src/generator.py --template prompts.json --out results.json --count 2 --mode image
```

### Mode Video
```bash
python src/generator.py --template prompts.json --count 5 --mode video
```
- Frame tersimpan di folder `frames/`
- Video jadi `output.mp4`

## Lisensi
MIT
