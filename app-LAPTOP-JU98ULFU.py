import streamlit as st

from src.database import setup_and_populate_db
from src.generator import compile_quiz_data


@st.cache_resource
def prepare_knowledge_base():
    setup_and_populate_db()


prepare_knowledge_base()

st.set_page_config(page_title="Sports Quiz Agent", page_icon="🏆", layout="centered")
st.title("🏆 AI-Powered Sports Quiz Generator")
st.write("Generate grounded sports quiz questions using local historical facts and live web context.")

st.sidebar.header("Quiz Settings")
sport_choice = st.sidebar.selectbox("Select Sport", ["Cricket", "Football", "Badminton", "Tennis"])
difficulty = st.sidebar.select_slider("Select Difficulty", options=["Easy", "Medium", "Hard"])

if "quiz_output" not in st.session_state:
    st.session_state.quiz_output = None
    st.session_state.quiz_context = None

if st.sidebar.button("Generate Fresh Quiz", use_container_width=True):
    with st.spinner("Fetching historical facts and live context..."):
        try:
            quiz_text, context_used = compile_quiz_data(sport_choice, difficulty)
            st.session_state.quiz_output = quiz_text
            st.session_state.quiz_context = context_used
            st.success("Quiz created successfully!")
        except Exception as exc:
            st.error(f"Failed to generate quiz: {exc}")

if st.session_state.quiz_output:
    st.subheader(f"Current Quiz: {sport_choice} ({difficulty})")
    st.text_area(
        "Generated Quiz Output",
        value=st.session_state.quiz_output,
        height=350,
    )

    with st.expander("🔍 Inspect Ground Truth (RAG Context Used)"):
        st.code(st.session_state.quiz_context, language="markdown")
