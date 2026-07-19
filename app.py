import streamlit as st
from src.config import OPENAI_API_KEY
from src.database import setup_and_populate_db
from src.generator import compile_quiz_data


@st.cache_resource
def prepare_knowledge_base():
    setup_and_populate_db()


prepare_knowledge_base()

st.set_page_config(page_title="Sports Quiz Agent", page_icon="🏆", layout="centered")

st.title("🏆 AI-Powered Sports Quiz Generator")
st.write("Generate factually grounded sports quiz questions for social media posts.")

st.markdown(
    """
    <style>
    .stAppDeployButton,
    .stAppToolbar .stAppDeployButton,
    .stAppToolbar button[title="Deploy"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "quiz_output" not in st.session_state:
    st.session_state.quiz_output = None
    st.session_state.quiz_context = None
    st.session_state.quiz_error = None
    st.session_state.request_count = 0

st.sidebar.header("Quiz Settings")
sport_choice = st.sidebar.selectbox("Select Sport", ["Cricket", "Football", "Tennis", "Badminton", "Basketball"])
difficulty = st.sidebar.select_slider("Select Difficulty", options=["Easy", "Medium", "Hard"])

if not OPENAI_API_KEY:
    st.sidebar.info("No OpenAI API key detected. A grounded fallback quiz will be created from local and live context.")


def generate_quiz():
    with st.spinner("Generating quiz with RAG references..."):
        try:
            request_number = st.session_state.request_count + 1
            st.session_state.request_count = request_number
            result = compile_quiz_data(
                sport_choice,
                difficulty,
                request_id=request_number,
            )

            if len(result) == 3:
                quiz_text, context_used, error_message = result
            else:
                quiz_text, context_used = result
                error_message = None

            st.session_state.quiz_output = quiz_text
            st.session_state.quiz_context = context_used
            st.session_state.quiz_error = error_message
            st.session_state.last_sport = sport_choice
            st.session_state.last_difficulty = difficulty
            st.success("Quiz generated successfully!")
        except Exception as e:
            st.error(f"Could not generate quiz: {e}")


left_col, right_col = st.sidebar.columns(2)
if left_col.button("Generate Quiz"):
    generate_quiz()

if right_col.button("Regenerate Quiz"):
    generate_quiz()

if st.session_state.quiz_output:
    st.subheader(f"Sport: {st.session_state.last_sport} | Difficulty: {st.session_state.last_difficulty}")
    st.text_area("Generated Quiz", value=st.session_state.quiz_output, height=360)

    with st.expander("🔎 Ground Truth Context Used"):
        st.code(st.session_state.quiz_context, language="markdown")
