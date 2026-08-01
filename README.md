# 🎥 AI Powered Video Assistant

An AI-powered assistant that transforms YouTube videos or local audio/video files into an intelligent, searchable knowledge base. The application transcribes audio, translates Hinglish conversations into English, generates summaries, extracts action items, and enables context-aware question answering using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📺 Process YouTube videos
- 📁 Upload local audio/video files
- 🎙️ Speech-to-Text transcription using OpenAI Whisper(English)/Sarvam AI(Hinglish)
- 📝 AI-generated summaries
- ✅ Automatic extraction of action items
- 🤖 Interactive AI Chatbot
- 💬 Ask questions about the transcript in natural language
- 🧠 Context-aware conversation memory for follow-up questions
- 🔍 Retrieval-Augmented Generation (RAG) using LangChain + ChromaDB
- ⚡ Semantic search over transcripts
- 🤖 Powered by Mistral AI
- 🌐 Interactive Streamlit Web Interface
---

## 🏗️ Architecture

```
User Input
      │
      ▼
YouTube URL / Local File
      │
      ▼
Audio Extraction (yt-dlp / pydub)
      │
      ▼
Speech-to-Text (OpenAI Whisper/Sarvam AI)
      │
      ▼
Transcript
      │
      ├───────────────┐───────────────┐────────────────────┐
      ▼               ▼               ▼                    ▼
 Summary        Action Items         Key Decisions     Unresolved Questions
      │
      ▼
Chunking + Embeddings
      │
      ▼
ChromaDB Vector Store
      │
      ▼
Retriever (LangChain)
      │
      ▼
Mistral AI + LangChain
      │
      ▼
Context-Aware AI Chatbot
      │
      ▼
Intelligent Responses
```

---

## 🛠 Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI Models
- Mistral AI
- OpenAI Whisper
- Sarvam AI

### Frameworks
- LangChain

### Vector Database
- ChromaDB

### Embeddings
- Hugging Face Sentence Transformers

### Audio Processing
- yt-dlp
- FFmpeg
- pydub

### Other Libraries
- NumPy
- Pandas
- Python-dotenv

---

## 📂 Project Structure

```
AI_POWERED_VIDEO_ASSISTANT/
│
├── Core/
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── rag_engine.py
│   ├── vectorestore.py
│   └── Actionables.py
│
├── Utils/
│   ├── Audio_processing.py
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

##% Clone the repository

```bash
git clone https://github.com/KaushikAgrawalDS/AI_Powered_Video_Assistant.git
```


## 💡 How It Works

1. User enters a YouTube URL or uploads a local audio/video file.
2. Audio is extracted using **yt-dlp** or **pydub**.
3. OpenAI Whisper(English)/Sarvam AI(Hinglish)  converts speech into text.
4. The transcript is chunked into smaller sections.
5. Sentence Transformers generate embeddings.
6. ChromaDB stores the embeddings.
7. LangChain retrieves the most relevant transcript chunks.
8. Mistral AI generates:
   - Summary
   - Action Items
   - Key Decisions
   - Unresolved Questions
   - Context-aware chatbot responses
9. Chat history is preserved, enabling natural follow-up questions while grounding responses in the transcript.

---

## ✨ Key Capabilities

- Speech-to-Text Transcription
- Hinglish Translation
- AI Summarization
- Action Item, Key Decisions, Questions Detection
- Retrieval-Augmented Generation (RAG)
- AI Chatbot
- Conversational Memory
- Semantic Search
- Vector Database Integration

---

## 🚀 Future Improvements

- Multi-language support
- Speaker diarization
- PDF meeting reports
- Cloud deployment
- Meeting analytics dashboard
- Support for multiple LLM providers
- Authentication and user sessions

---

## 👨‍💻 Author

**Kaushik Agrawal**

GitHub: https://github.com/KaushikAgrawalDS

LinkedIn: *www.linkedin.com/in/kaushik-agrawal-03b64624b*

---

⭐ If you found this project useful, please consider giving it a star!
