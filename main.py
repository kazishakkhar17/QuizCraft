import streamlit as st
import pdfplumber
import requests
import json

# ------------------- CONFIG ------------------- #
GROQ_API_KEY = "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"  # Replace with your valid key
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# ------------------- STEP 1: PDF to Text ------------------- #
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# ------------------- STEP 2: Generate MCQs ------------------- #
def generate_mcqs(text, num_questions=25):
    prompt = f"""
You are a professional academic assistant. Read the passage below and generate {num_questions} multiple choice questions.

Guidelines:
- Use only information from the text.
- Ensure questions are clear and unambiguous.
- Mix theoretical and factual questions.
- Each question must include:
    - "question": a string
    - "options": exactly 4 options
    - "correct_option": index of the correct answer (0 to 3)

Return only a JSON list of dictionaries with no explanation.

Text:
\"\"\"{text[:3000]}\"\"\"
"""

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a medical quiz generator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(GROQ_API_URL, headers=HEADERS, json=data)

    if response.status_code != 200:
        st.error(f"API call failed with status {response.status_code}: {response.text}")
        return []

    response_json = response.json()

    if "choices" not in response_json:
        st.error("API response missing 'choices' key or returned error.")
        if "error" in response_json:
            st.error(f"API error message: {response_json['error'].get('message', 'No message')}")
        return []

    content = response_json["choices"][0]["message"]["content"]

    def extract_json_from_text(text):
        try:
            start = text.index('[')
            end = text.rindex(']') + 1
            json_str = text[start:end]
            return json.loads(json_str)
        except Exception:
            return None

    try:
        mcqs = json.loads(content)
    except json.JSONDecodeError:
        mcqs = extract_json_from_text(content)

    if mcqs is None:
        st.error("Failed to parse MCQs from model response.")
        st.json(response_json)
        return []
    else:
        return mcqs

# ------------------- STEP 3: Quiz UI ------------------- #
def run_quiz():
    mcqs = st.session_state.mcqs
    n = len(mcqs)

    if "answers" not in st.session_state or len(st.session_state.answers) != n:
        st.session_state.answers = [None] * n
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    st.subheader("📋 Take the Quiz!")

    # Show all questions with radio buttons and save answers as indices
    for i, q in enumerate(mcqs):
        st.markdown(f"**Q{i+1}. {q['question']}**")

        current_idx = st.session_state.answers[i] if st.session_state.answers[i] is not None else 0

        selected_option = st.radio(
            "Select answer:",
            options=q['options'],
            key=f"q_{i}",
            index=current_idx
        )
        selected_index = q['options'].index(selected_option)
        st.session_state.answers[i] = selected_index

        st.write("---")

    if st.button("Submit Quiz"):
        st.session_state.submitted = True

    if st.session_state.submitted:
        score = 0
        for i, q in enumerate(mcqs):
            correct_index = q['correct_option']
            user_index = st.session_state.answers[i]
            correct_answer = q['options'][correct_index]
            user_answer = q['options'][user_index]

            st.markdown(f"**Question {i+1}:** {q['question']}")
            st.markdown(f"- Your response: {user_answer}")
            st.markdown(f"- Correct answer: {correct_answer}")

            if user_index == correct_index:
                st.success("Result: ✅ Correct!")
                score += 1
            else:
                st.error("Result: ❌ Wrong.")
            st.write("---")

        st.markdown(f"### 🧠 Final Score: {score} / {len(mcqs)}")

# ------------------- MAIN APP ------------------- #
def main():
    st.title("🧠 QuizCraft")

    uploaded_file = st.file_uploader("Upload a PDF and Let the magic begin!", type=["pdf"])

    if uploaded_file:
        st.info("⏳ Analyzing your PDF...")
        text = extract_text_from_pdf(uploaded_file)

        st.code(text[:1000])  # <-- Show a snippet for debugging input quality

        if len(text.strip()) < 100:
            st.warning("The PDF doesn't contain enough text.")
            return

        if st.button("🔍 Start Your Test"):
            st.info("🧠 Generating questions...Powered By Shakkhar")
            mcqs = generate_mcqs(text)
            if mcqs:
                st.session_state.mcqs = mcqs
                st.session_state.submitted = False
                st.session_state.answers = [None] * len(mcqs)
            else:
                st.error("Failed to generate questions. Try again.")

    if "mcqs" in st.session_state and st.session_state.mcqs:
        run_quiz()

if __name__ == "__main__":
    main()
