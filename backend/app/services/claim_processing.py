import spacy

from google.genai import types

from app.core.gemini import client, MODEL
from app.schemas.claim_schemas import ClaimProcessingResult


# Sentence splitter
nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")


def process_claims(question: str, answer: str):

    # Step 1: Sentence splitting
    doc = nlp(answer)

    sentences = [
        sent.text.strip()
        for sent in doc.sents
        if sent.text.strip()
    ]

    # Step 2: Prepare prompt for fact selection +resolving pronouns + atomic claim extraction
    prompt = f"""
    You are a factual claim extraction system for TruthLens.

    USER QUESTION:
    {question}

    GENERATED ANSWER:
    {answer}

    SENTENCES:
    {sentences}

    Perform the following operations:

    1. Identify factual and independently verifiable statements.
    2. Ignore opinions, greetings and subjective statements.
    3. Resolve pronouns using the question and surrounding context.
    4. Decompose sentences containing multiple facts into
       independent atomic claims.
    5. Preserve names, dates, numbers, negations,
       conditions and uncertainty.
    6. Do not introduce information absent from the input.
    7. If a reference cannot be resolved confidently,
       preserve the original wording rather than guessing.
    8. Keep the original source sentence unchanged.

    Return all relevant factual claims.
    """

    # Step 3: Gemini structured output
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ClaimProcessingResult,
            temperature=0
        )
    )

    # Step 4: Validate and return
    if response.parsed is not None:
        return ClaimProcessingResult.model_validate(response.parsed)

    return ClaimProcessingResult.model_validate_json(response.text)