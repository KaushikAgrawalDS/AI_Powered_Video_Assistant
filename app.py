import os
import tempfile
 
import streamlit as st
from dotenv import load_dotenv
 
from Utils.Audio_processing import process_input
from Core.transcriber import transcribe_all
from Core.summarizer import summarize, generate_title
from Core.Actionables import extarct_action_items, extarct_key_decisions, extract_questions
from Core.rag_engine import build_rag_chain, ask_question
 
load_dotenv()
 
st.set_page_config(page_title="AI Video Assistant", page_icon="🎬", layout="wide")
 
 
# ----------------------------------------------------------------------
# Core pipeline (same logic as the CLI script, just reused here)
# ----------------------------------------------------------------------
def run_pipeline(source: str, language: str = "english"):
    chunks = process_input(source)
    transcript = transcribe_all(chunks, language=language)
 
    title = generate_title(transcript)
    summary = summarize(transcript)
    action_items = extarct_action_items(transcript)
    questions = extract_questions(transcript)
    decisions = extarct_key_decisions(transcript)
    rag_chain = build_rag_chain(transcript)
 
    return {
        "title": title,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_question": questions,
        "rag_chain": rag_chain,
    }
 
 
# ----------------------------------------------------------------------
# Session state init
# ----------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
 
# ----------------------------------------------------------------------
# Sidebar — input selection
# ----------------------------------------------------------------------
st.sidebar.title("🎬 AI Video Assistant")
st.sidebar.markdown("Analyze a meeting/video from a **YouTube link** or a **local file**.")
 
source_type = st.sidebar.radio(
    "Choose input source",
    options=["YouTube Link", "Local File"],
    horizontal=False,
)
 
youtube_url = None
uploaded_file = None
 
if source_type == "YouTube Link":
    youtube_url = st.sidebar.text_input(
        "Paste YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
    )
else:
    uploaded_file = st.sidebar.file_uploader(
        "Select a local audio/video file",
        type=["mp4", "mp3", "wav", "m4a", "mov", "mkv", "avi"],
    )
 
language = st.sidebar.selectbox("Language", options=["english", "hinglish"], index=0)
 
run_clicked = st.sidebar.button("🚀 Run Analysis", use_container_width=True)
 
st.sidebar.divider()
if st.sidebar.button("🔄 Reset", use_container_width=True):
    st.session_state.result = None
    st.session_state.chat_history = []
    st.rerun()
 
# ----------------------------------------------------------------------
# Run pipeline
# ----------------------------------------------------------------------
if run_clicked:
    source = None
    tmp_path = None
 
    if source_type == "YouTube Link":
        if not youtube_url or not youtube_url.strip():
            st.sidebar.error("Please paste a YouTube URL first.")
        else:
            source = youtube_url.strip()
    else:
        if uploaded_file is None:
            st.sidebar.error("Please select a local file first.")
        else:
            # Persist the uploaded file to disk so process_input (which
            # expects a path) can read it.
            suffix = os.path.splitext(uploaded_file.name)[1]
            tmp_dir = tempfile.mkdtemp()
            tmp_path = os.path.join(tmp_dir, uploaded_file.name)
            with open(tmp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            source = tmp_path
 
    if source:
        with st.spinner("Processing video — this can take a few minutes..."):
            try:
                st.session_state.result = run_pipeline(source, language=language)
                st.session_state.chat_history = []
                st.success("Analysis complete!")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass
 
# ----------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------
result = st.session_state.result
 
if result is None:
    st.title("🎬 AI Video Assistant")
    st.info("Choose a YouTube link or local file in the sidebar, then click **Run Analysis**.")
else:
    st.title(result.get("title") or "Analysis Results")
 
    tab_summary, tab_actions, tab_decisions, tab_questions, tab_chat = st.tabs(
        ["📝 Summary", "✅ Action Items", "📌 Key Decisions", "❓ Open Questions", "💬 Chat"]
    )
 
    with tab_summary:
        st.markdown(result["summary"])
 
    with tab_actions:
        st.markdown(result["action_items"])
 
    with tab_decisions:
        st.markdown(result["key_decisions"])
 
    with tab_questions:
        st.markdown(result["open_question"])
 
    with tab_chat:
        st.caption("Ask questions about the video/meeting content.")
 
        for role, msg in st.session_state.chat_history:
            with st.chat_message(role):
                st.markdown(msg)
 
        question = st.chat_input("Ask something about this video...")
        if question:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        answer = ask_question(
                            rag_chain=result["rag_chain"],
                            questions=question,
                            chat_history=st.session_state.chat_history,  # pass history BEFORE this turn
                        )
                    except Exception as e:
                        answer = f"Error answering question: {e}"
                    st.markdown(answer)

            st.session_state.chat_history.append(("user", question))
            st.session_state.chat_history.append(("assistant", answer))
