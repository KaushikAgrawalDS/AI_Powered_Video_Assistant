# 🎥 AI Powered Video Assistant

An AI-powered application that transforms YouTube videos or local audio/video files into intelligent, searchable knowledge. The assistant transcribes audio, generates summaries, extracts action items, and answers user questions using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📺 Process YouTube videos
- 📁 Upload local audio/video files
- 🎙️ Automatic speech-to-text transcription using Whisper
- 📝 AI-generated meeting or video summaries
- ✅ Automatic extraction of action items
- 💬 Ask questions about the video using RAG
- 🔎 Semantic search using ChromaDB
- 🤖 Powered by Mistral AI and LangChain
- 🌐 Simple Streamlit web interface

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI & NLP
- OpenAI Whisper
- Mistral AI
- LangChain

### Vector Database
- ChromaDB

### Embeddings
- HuggingFace Sentence Transformers

### Audio Processing
- yt-dlp
- FFmpeg
- pydub

---

## 📂 Project Structure

```
AI_POWERED_VIDEO_ASSISTANT/
│
├── Core/
│   ├── rag_engine.py
│   ├── summarizer.py
│   ├── transcriber.py
│   ├── vectorestore.py
│   └── Actionables.py
│
├── Utils/
│
├── downloads/
├── vector_db/
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---


## 📖 How It Works

1. Enter a YouTube URL or provide a local media file.
2. Audio is extracted and converted into WAV format.
3. Whisper transcribes the audio into text.
4. The transcript is chunked and embedded.
5. ChromaDB stores the embeddings.
6. LangChain retrieves relevant context.
7. Mistral AI generates:
   - Summary
   - Action Items
   - Answers to user questions

---

