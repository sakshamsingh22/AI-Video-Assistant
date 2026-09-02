# 🎥 AI Video Assistant

An AI-powered video intelligence application that transforms long-form video and audio content into concise, structured, searchable, and actionable information.

The AI Video Assistant allows users to upload video content, extract audio, generate transcripts, summarize the content, identify key decisions and action items, extract important questions, and interact with the video through a Retrieval-Augmented Generation (RAG) based question-answering system.

---

## ✨ Features

### 🎬 Video & Audio Processing

- Upload and process video content
- Extract audio from video input
- Process audio for transcription
- Convert long-form video content into machine-readable text

### 🎙️ Automatic Transcription

- Convert spoken content into text
- Generate transcripts from video/audio
- Use transcripts as the foundation for AI analysis
- Make long video content searchable and easier to understand

### 📝 AI-Powered Summarization

- Generate concise summaries of long videos
- Automatically generate relevant titles
- Convert lengthy discussions into structured information
- Quickly understand the main topics of a video

### 🔍 Intelligent Information Extraction

The system extracts important information from the transcript, including:

- Key decisions
- Action items
- Important questions
- Relevant discussion points
- Other useful information from the conversation

### 💬 Ask Questions About the Video

Users can ask natural-language questions about the uploaded video.

The RAG pipeline retrieves relevant information from the transcript and uses it as context for generating answers.

Example questions:

- What were the main decisions discussed?
- What action items were assigned?
- What was the main topic of the meeting?
- What problems were discussed?
- What were the important questions raised?

### 🖥️ Interactive Web Interface

The application provides an interactive Streamlit interface for:

- Uploading videos
- Processing video content
- Viewing transcripts
- Reading summaries
- Viewing extracted insights
- Asking questions about the video

---

# 🧠 How It Works

The application follows an AI-powered processing pipeline:

```text
                         ┌─────────────────────┐
                         │     Video Input     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Audio Processing   │
                         │  / Audio Extraction │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Transcription    │
                         │    Speech → Text    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Transcript     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
             ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
             │ Summarizer  │ │  Extractor  │ │ RAG Engine  │
             └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
                    │               │               │
                    ▼               ▼               ▼
                Summary       Decisions /       User Query
                + Title       Actions /             │
                                  Questions         ▼
                                              Relevant Context
                                                     │
                                                     ▼
                                              AI Generated Answer
