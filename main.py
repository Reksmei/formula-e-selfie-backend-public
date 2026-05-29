import os
import uuid
import base64
import io
import qrcode
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import app_utils
import uvicorn

load_dotenv()

app = FastAPI()

#CORS 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def main_generate_image(prompt: str, image: Optional[UploadFile] = File(None), reference_image: Optional[UploadFile] = File(None)):
    return await app_utils.generate_image(prompt,image,reference_image)


#For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
      raise HTTPException(status_code=500, detail=str(e))

#For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
