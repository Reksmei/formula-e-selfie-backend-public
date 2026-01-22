import os
import uuid
import base64
import io
import qrcode
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from google.cloud import storage

#Configuration
PROJECT_ID = "formula-e-selfie"
LOCATION = "global"
BUCKET_NAME = "created-images"
MODEL_ID = "gemini-3-pro-image-preview"

#Initializing Client
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)

storage_client = storage.Client(project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)

app = FastAPI()

#CORS 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def upload_to_gcs(image_data: bytes, content_type: str = "image/png") -> str:
    """
    Uploads images image bytes tou Cloud Storage with unique name and returns public URL.
    """
    filename = f"{uuid.uuid4()}.png"
    blob = bucket.blob(filename)

    blob.upload_from_string(image_data, content_type = content_type)
    return f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

@app.post("/generate")
async def generate_image(
    prompt: str = Form(...),
    image: Optional[UploadFile] = File(None),
    reference_image: Optional[UploadFile] = File(None)
):
    """
    Endpoint to generate or edit an image using Gemini 3 Pro Image/Nano Banana Pro. 

    -prompt: The text instruction (containing Formula E theme prompt)
    -image: (optional) The base image to edit
    -reference_image: (optional) A reference image to help ground the model in reality (branding, etc).
    """
    try:
        contents = [prompt]

        if image:
          image_bytes = await image.read()
          image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=image.content_type or "image/jpeg"
        )
        contents.append(image_part)

        if reference_image:
          ref_bytes = await reference_image.read()
          ref_part = types.Part.from_bytes(
            data=ref_bytes,
            mime_type=reference_image.content_type or "image/jpeg"
        )
          contents.append(ref_part)

        google_search_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    #API Call to Gemini on Vertex AI 
        response = client.models.generate_content(
        model=MODEL_ID,
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="4:3"
            ),
        )
    )

    #Extract Generated Image
        generated_image_bytes = None

        if response.candidates and response.candidates[0].content.parts:
          for part in response.candidates[0].content.parts:
            if part.inline_data:
                generated_image_bytes = part.inline_data.data
                break

        if not generated_image_bytes:
          error_text = response.text if response.text else "No image generated."
          raise HTTPException(status_code=500, detail=f"Nano Banana Pro did not return an image: {error_text}")

    #Upload generated image to GCS
        image_url = upload_to_gcs(generated_image_bytes)

        # Generate QR Code
        print("Generating QR code...")
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(image_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = io.BytesIO()
        img.save(buf)
        buf.seek(0)
        
        qr_code_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        print("QR code generated successfully.")

        return {
        "status": "success",
        "image_url": image_url,
        "qr_code_base64": qr_code_base64
        }
  
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=500, detail=str(e))

#For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)