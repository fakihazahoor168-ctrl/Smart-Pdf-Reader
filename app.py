import streamlit as st
from pdf_reader import extract_text_from_pdf
from ai_question_generator import generate_questions_ai
from ai_mcq_generator import generate_mcqs_ai
from pdf_summarizer import summarize_text
from text_to_speech import speak_text   # 🔊 TTS import

# -------------------- SESSION STATE INIT --------------------
if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Intelligent PDF Reader",
    layout="wide"
)

st.title("🧠 Intelligent PDF Reader & AI Assistant")
st.write(
    "Upload a PDF to **summarize content**, **generate questions**, or **generate MCQs** using AI."
)

# -------------------- PDF UPLOAD --------------------
uploaded_file = st.file_uploader("📄 Upload PDF", type="pdf")

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)

    if not text.strip():
        st.error("❌ No readable text found in this PDF.")
        st.stop()

    # Optional text display
    if st.checkbox("Show extracted text"):
        st.text_area("Extracted PDF Text", text, height=300)

    # -------------------- USER OPTIONS --------------------
    with st.form("ai_form"):
        st.subheader("⚙️ Select Task & Settings")

        task = st.selectbox(
            "Select task",
            ["Summarize PDF", "Generate Questions", "Generate MCQs"]
        )

        difficulty = st.selectbox(
            "Difficulty level",
            ["Easy", "Medium", "Hard"]
        )

        qtype = st.selectbox(
            "Question type (only for questions)",
            ["Short", "Long"]
        )

        num_questions = st.number_input(
            "Number of questions",
            min_value=1,
            max_value=50,
            value=5
        )

        num_mcqs = st.number_input(
            "Number of MCQs",
            min_value=1,
            max_value=50,
            value=5
        )

        submit_btn = st.form_submit_button("🚀 Run")

    # -------------------- PROCESSING --------------------
    if submit_btn:
        with st.spinner("⏳ Processing, please wait..."):

            # -------- SUMMARIZATION --------
            if task == "Summarize PDF":
                summary = summarize_text(text)

                if not summary:
                    st.warning("⚠️ Could not generate summary.")
                else:
                    st.session_state.summary_text = summary

            # -------- QUESTION GENERATION --------
            elif task == "Generate Questions":
                questions = generate_questions_ai(
                    text, num_questions, difficulty, qtype
                )

                if not questions:
                    st.warning("⚠️ Could not generate questions.")
                else:
                    st.subheader("📘 Generated Questions")
                    for i, q in enumerate(questions, 1):
                        st.write(f"**{i}.** {q}")

                    if len(questions) < num_questions:
                        st.info(
                            f"ℹ️ Generated {len(questions)} out of {num_questions} questions."
                        )

                    # ✅ Download Questions
                    questions_text = "\n".join([f"{i}. {q}" for i, q in enumerate(questions, 1)])
                    st.download_button(
                        label="💾 Download Questions",
                        data=questions_text,
                        file_name="questions.txt",
                        mime="text/plain"
                    )

            # -------- MCQ GENERATION --------
            elif task == "Generate MCQs":
                mcqs = generate_mcqs_ai(text, num_mcqs, difficulty)

                if not mcqs:
                    st.warning("⚠️ Could not generate MCQs.")
                else:
                    st.subheader("📝 Generated MCQs")
                    mcqs_text = ""
                    for i, mcq in enumerate(mcqs, 1):
                        st.write(f"**Q{i}. {mcq['question']}**")
                        mcqs_text += f"Q{i}. {mcq['question']}\n"
                        for j, opt in enumerate(mcq["options"], 65):
                            st.write(f"{chr(j)}. {opt}")
                            mcqs_text += f"{chr(j)}. {opt}\n"
                        st.write(f"✅ **Answer:** {mcq['answer']}")
                        mcqs_text += f"Answer: {mcq['answer']}\n\n"
                        st.divider()

                    if len(mcqs) < num_mcqs:
                        st.info(
                            f"ℹ️ Generated {len(mcqs)} out of {num_mcqs} MCQs."
                        )

                    # ✅ Download MCQs
                    st.download_button(
                        label="💾 Download MCQs",
                        data=mcqs_text,
                        file_name="mcqs.txt",
                        mime="text/plain"
                    )

    # -------------------- SHOW SUMMARY (PERSISTENT) --------------------
    if st.session_state.summary_text:
        st.subheader("📌 PDF Summary")
        st.text_area(
            "Summary",
            st.session_state.summary_text,
            height=300
        )

        # 🔊 Play Summary in Browser
        st.button("🔊 Play Summary", key="play_summary", on_click=lambda: speak_text(st.session_state.summary_text))

        # 💾 Download Summary
        st.download_button(
            label="💾 Download Summary",
            data=st.session_state.summary_text,
            file_name="summary.txt",
            mime="text/plain"
        )

else:
    st.info("⬆️ Please upload a PDF file to get started.")
