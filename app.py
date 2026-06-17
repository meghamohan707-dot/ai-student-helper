import streamlit as st
from openai import OpenAI

if "count" not in st.session_state:
    st.session_state.count = 0

MAX_FREE_USES = 5

# =========================
# 🔑 PUT YOUR API KEY HERE
# =========================

from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Student Helper", page_icon="📚")

st.title("📚 AI Student Helper App")
st.write("Paste your question or notes and get explanations, summaries, quizzes, and flashcards.")

# =========================
# INPUT
# =========================
user_input = st.text_area("Enter your text or question:")

mode = st.selectbox(
    "Choose mode:",
    ["Explain simply", "Summary", "Quiz", "Flashcards"]
)

# =========================
# PROMPT BUILDER
# =========================
def build_prompt(text, mode):
    return f"""
You are an expert tutor.

Student input: {text}

Mode: {mode}

Rules:
- Explain in simple language
- Use bullet points
- Make it easy to study
- Add examples if needed
"""
# =========================
# AI FUNCTION
# =========================
def get_ai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful and simple student tutor. Always explain clearly."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# =========================
# BUTTON ACTION
# =========================
if st.button("Generate"):
    if user_input.strip() == "":
        st.warning("Please enter a question or topic.")
    elif st.session_state.count >= MAX_FREE_USES:
        st.error("Free limit reached. Upgrade coming soon!")

    else:
        try:
            result = get_ai_response(build_prompt(user_input, mode))
            st.markdown(result)

            st.session_state.count += 1
            st.info(f"Free uses left: {MAX_FREE_USES - st.session_state.count}")

        except Exception as e:
            st.error("Something went wrong. Please try again.")
