from transformers import pipeline
import random

# 🔹 Load model ONCE
qg_pipeline = pipeline(
    "text2text-generation",
    model="valhalla/t5-base-qg-hl"
)

def generate_mcqs_ai(text, num, difficulty):
    mcqs = []

    # 🔹 Split text into sentences
    sentences = [s.strip() for s in text.split(".") if len(s.split()) >= 8]

    # -------------------------------------------------
    # 🔹 Difficulty-based INPUT + OUTPUT control
    # -------------------------------------------------
    if difficulty == "Easy":
        # Short sentences → factual MCQs
        filtered = [s for s in sentences if len(s.split()) <= 12]
        temperature = 0.3
        max_q_words = 10

    elif difficulty == "Medium":
        # Medium complexity sentences
        filtered = [s for s in sentences if 13 <= len(s.split()) <= 22]
        temperature = 0.6
        max_q_words = 15

    else:  # Hard
        # Long + analytical sentences
        filtered = [s for s in sentences if len(s.split()) > 22]
        temperature = 0.9
        max_q_words = 25

    # 🔹 Fallback if no sentence matches
    if not filtered:
        filtered = sentences

    # -------------------------------------------------
    # 🔹 Generate MCQs
    # -------------------------------------------------
    for sent in filtered:
        if len(mcqs) >= num:
            break

        prompt = f"generate question: {sent}"

        out = qg_pipeline(
            prompt,
            max_length=64,
            do_sample=True,
            temperature=temperature
        )

        question = out[0]["generated_text"].strip()
        if not question:
            continue

        # 🔹 POST-FILTER → fixes Easy/Hard confusion
        if len(question.split()) > max_q_words:
            continue

        # -------------------------------------------------
        # 🔹 Option generation logic
        # -------------------------------------------------
        words = [w.strip(",.()") for w in sent.split() if len(w) > 3]
        words = list(set(words))  # remove duplicates

        if len(words) < 4:
            continue

        correct_answer = random.choice(words)

        wrong_pool = [w for w in words if w != correct_answer]
        if len(wrong_pool) < 3:
            continue

        wrong_options = random.sample(wrong_pool, 3)

        options = wrong_options + [correct_answer]
        random.shuffle(options)

        mcqs.append({
            "question": question,
            "options": options,
            "answer": correct_answer
        })

    return mcqs
