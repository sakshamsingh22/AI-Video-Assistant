"""Audio acquisition, validation and chunking utilities."""
from pathlib import Path
from urllib.parse import urlparse
import os
import tempfile

import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = Path(os.getenv("AUDIO_DOWNLOAD_DIR", "downloads"))
MAX_LOCAL_FILE_BYTES = 500 * 1024 * 1024
ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".mp4", ".mov", ".mkv", ".webm", ".ogg", ".flac"}


def is_supported_remote_url(source: str) -> bool:
    parsed = urlparse(source)
    return parsed.scheme == "https" and parsed.hostname in {
        "youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"
    }


def download_youtube_audio(url: str) -> str:
    if not is_supported_remote_url(url):
        raise ValueError("Provide a valid HTTPS YouTube URL.")
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    with yt_dlp.YoutubeDL({
        "format": "bestaudio/best",
        "outtmpl": str(DOWNLOAD_DIR / "%(id)s.%(ext)s"),
        "noplaylist": True,
        "max_filesize": MAX_LOCAL_FILE_BYTES,
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav", "preferredquality": "192"}],
        "quiet": True,
    }) as ydl:
        info = ydl.extract_info(url, download=True)
        wav_path = Path(ydl.prepare_filename(info)).with_suffix(".wav")
    if not wav_path.is_file():
        raise RuntimeError("Audio download completed but the WAV output was not found.")
    return str(wav_path)


def convert_to_wav(input_path: str) -> str:
    path = Path(input_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Media file does not exist: {path}")
    if path.suffix.lower() not in ALLOWED_AUDIO_EXTENSIONS:
        raise ValueError(f"Unsupported media extension: {path.suffix or '(none)'}")
    if path.stat().st_size > MAX_LOCAL_FILE_BYTES:
        raise ValueError("Media file exceeds the 500 MB size limit.")
    audio = AudioSegment.from_file(str(path)).set_channels(1).set_frame_rate(16000)
    fd, output_path = tempfile.mkstemp(prefix="video-assistant-", suffix=".wav")
    os.close(fd)
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list[str]:
    if not isinstance(chunk_minutes, int) or not 1 <= chunk_minutes <= 30:
        raise ValueError("chunk_minutes must be between 1 and 30.")
    path = Path(wav_path)
    if not path.is_file():
        raise FileNotFoundError(f"Audio file does not exist: {path}")
    audio = AudioSegment.from_wav(str(path))
    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []
    for index, start in enumerate(range(0, len(audio), chunk_ms)):
        fd, chunk_path = tempfile.mkstemp(prefix=f"video-chunk-{index}-", suffix=".wav")
        os.close(fd)
        audio[start:start + chunk_ms].export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks


def process_input(source: str) -> list[str]:
    if not isinstance(source, str) or not source.strip():
        raise ValueError("Provide a YouTube URL or local media file path.")
    source = source.strip()
    wav_path = download_youtube_audio(source) if source.startswith(("http://", "https://")) else convert_to_wav(source)
    return chunk_audio(wav_path)
