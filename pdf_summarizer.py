from transformers import pipeline

# Load summarization model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize_text(text, max_length=150, min_length=60):
    """
    Summarize long text by chunking
    """
    summaries = []

    # Split into manageable chunks
    chunk_size = 800
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    for chunk in chunks:
        if len(chunk.strip()) < 100:
            continue

        summary = summarizer(
            chunk,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]["summary_text"]

        summaries.append(summary)

    return " ".join(summaries)
