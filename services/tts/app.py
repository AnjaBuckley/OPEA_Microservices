from fastapi import FastAPI, HTTPException
from comps import ServiceType, TextDoc
from typing import Dict
import uvicorn
import os
import base64
import io
from gtts import gTTS

app = FastAPI()


def synthesize_speech(input: TextDoc) -> Dict:
    try:
        # Create a bytes buffer for the audio
        audio_buffer = io.BytesIO()

        # Generate speech using gTTS
        tts = gTTS(text=input.text, lang=input.language)
        tts.write_to_fp(audio_buffer)

        # Get the audio data and convert to base64
        audio_buffer.seek(0)
        audio_base64 = base64.b64encode(audio_buffer.read()).decode("utf-8")

        return {
            "audio_data": audio_base64,
            "format": "mp3",  # gTTS generates MP3 files
            "sample_rate": 24000,  # Standard sample rate for gTTS
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Speech synthesis failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/synthesize")
async def synthesize_endpoint(request: Dict):
    try:
        text = request.get("text", "")
        language = request.get("language", "de")

        doc = TextDoc(text=text, language=language)
        result = synthesize_speech(doc)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7002)
