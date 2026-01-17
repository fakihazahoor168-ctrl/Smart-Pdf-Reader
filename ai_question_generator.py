from transformers import pipeline

# Load model once
qg_pipeline = pipeline(
    "text2text-generation",
    model="valhalla/t5-base-qg-hl"
)

def generate_questions_ai(text, num, difficulty, qtype):
    questions = []

    # Sentence split
    sentences = [s.strip() for s in text.split(".") if len(s.split()) >= 6]

    # -------------------------------
    # Difficulty Logic (Easy / Hard)
    # -------------------------------
    if difficulty == "Easy":
        # Simple + factual
        filtered = [s for s in sentences if len(s.split()) <= 12]
        temperature = 0.3

    else:  # Hard
        # Complex + analytical
        filtered = [s for s in sentences if len(s.split()) > 12]
        temperature = 0.9

    if not filtered:
        filtered = sentences

    # -------------------------------
    # Question Type Logic (Short / Long)
    # -------------------------------
    if qtype == "Short":
        max_len = 40          # model output length
        max_words = 10        # post filter
    else:  # Long
        max_len = 90
        max_words = 30

    # -------------------------------
    # Question Generation
    # -------------------------------
    for sent in filtered:
        if len(questions) >= num:
            break

        prompt = f"generate question: {sent}"

        out = qg_pipeline(
            prompt,
            max_length=max_len,
            do_sample=True,
            temperature=temperature
        )

        q = out[0]["generated_text"].strip()

        # -------------------------------
        # Post Filters
        # -------------------------------
        if qtype == "Short" and len(q.split()) > max_words:
            continue

        if qtype == "Long" and len(q.split()) < 12:
            continue

        if q and q not in questions:
            questions.append(q)

    return questions
