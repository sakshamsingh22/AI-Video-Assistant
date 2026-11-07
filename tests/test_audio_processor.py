import pytest

from utils.audio_processor import is_supported_remote_url, chunk_audio


@pytest.mark.parametrize("url", [
    "https://www.youtube.com/watch?v=abc123",
    "https://youtu.be/abc123",
    "https://m.youtube.com/watch?v=abc123",
])
def test_accepts_supported_youtube_urls(url):
    assert is_supported_remote_url(url)


@pytest.mark.parametrize("url", [
    "http://www.youtube.com/watch?v=abc123",
    "https://youtube.com.evil.example/watch?v=abc123",
    "https://example.com/video",
    "file:///tmp/video.mp4",
])
def test_rejects_non_youtube_or_non_https_urls(url):
    assert not is_supported_remote_url(url)


def test_chunk_audio_rejects_invalid_duration():
    with pytest.raises(ValueError, match="between 1 and 30"):
        chunk_audio("missing.wav", 0)


def test_chunk_audio_requires_existing_file():
    with pytest.raises(FileNotFoundError):
        chunk_audio("missing.wav", 1)
