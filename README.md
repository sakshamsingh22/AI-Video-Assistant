# AI Video Assistant

Turn long-form video and audio into transcripts, summaries, decisions, action items and transcript-grounded Q&A.

## Features

- YouTube audio acquisition and local media ingestion
- Audio normalization and chunked transcription
- English transcription with local Whisper
- Hinglish transcription/translation with Sarvam AI
- LLM-generated titles, summaries, decisions, action items and open questions
- Transcript Q&A using Chroma vector search and Mistral
- Streamlit interface and CLI entry point

## Architecture

```text
YouTube URL / local media
  -> utils/audio_processor.py (validate, download, normalize, chunk)
  -> core/transcriber.py (Whisper / Sarvam)
  -> core/summarizer.py + core/extractor.py
  -> core/vector_store.py + core/rag_engine.py
  -> Streamlit UI (app.py) or CLI (main.py)
```

## Requirements

- Python 3.10+
- FFmpeg installed and available on PATH
- Mistral API key for generation and RAG
- Sarvam API key only for Hinglish transcription

## Setup

```bash
git clone https://github.com/sakshamsingh22/AI-Video-Assistant.git
cd AI-Video-Assistant
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r Requirements.txt
cp .env.example .env
```

Add only the keys needed for the features you use:

```env
MISTRAL_API_KEY=your_mistral_key
SARVAM_API_KEY=your_sarvam_key
WHISPER_MODEL=small
```

Never commit API keys.

## Run

```bash
streamlit run app.py
```

CLI:

```bash
python main.py
```

Provide an HTTPS YouTube URL or a supported local media file. Local media is limited to 500 MB.

## Tests

```bash
pytest -q
python -m compileall -q .
```

Tests validate input handling without calling paid model APIs.

## Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `MISTRAL_API_KEY` | Summaries, extraction, RAG | None |
| `SARVAM_API_KEY` | Hinglish transcription | None |
| `SARVAM_STT_MODEL` | Sarvam model selection | `saaras:v2.5` |
| `WHISPER_MODEL` | Local English transcription | `small` |
| `AUDIO_DOWNLOAD_DIR` | YouTube download directory | `downloads` |

## Known limitations

- Whisper and embedding models may require substantial RAM and disk space.
- Long recordings take time because stages run sequentially.
- Generated summaries and action items should be reviewed before use as official records.
- The vector store is local. Multi-user deployment requires isolated per-session storage and retention controls.
- Process only media you have permission to access.
