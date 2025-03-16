from fastapi import FastAPI, HTTPException
from comps import ServiceType, TextDoc
from typing import Dict, List
import uvicorn
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = FastAPI()

# Initialize model and tokenizer
model_name = "Helsinki-NLP/opus-mt-en-de"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def translate(input: TextDoc) -> TextDoc:
    # Translate text using the model
    inputs = tokenizer(
        input.text, return_tensors="pt", padding=True, truncation=True, max_length=512
    )
    outputs = model.generate(**inputs, max_length=512)
    translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return TextDoc(text=translated_text, language="de")


def get_examples(text: str, language: str = "de") -> str:
    # Generate example sentences using the translation model
    examples = []
    base_sentences = [
        "This concept is important in software architecture.",
        "Many modern systems use this approach.",
        "We can implement this pattern in our project.",
    ]

    # Translate each base sentence
    for sentence in base_sentences:
        context_sentence = f"{text}. {sentence}"
        inputs = tokenizer(
            context_sentence,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        )
        outputs = model.generate(**inputs, max_length=512)
        translated = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        examples.append(f"EN: {sentence}\nDE: {translated}")

    return "\n\n".join(examples)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/translate")
async def translate_endpoint(request: Dict):
    try:
        text = request.get("text", "")
        source_lang = request.get("source_language", "en")
        target_lang = request.get("target_language", "de")

        doc = TextDoc(text=text, language=source_lang)
        result = translate(doc)
        return {"translated_text": result.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/examples")
async def examples_endpoint(request: Dict):
    try:
        text = request.get("text", "")
        language = request.get("language", "de")

        examples = get_examples(text, language)
        return {"examples": examples}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
