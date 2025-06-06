from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn, io, numpy as np
from tensorflow.keras.models import load_model
from PIL import Image, UnidentifiedImageError
from pdf2image import convert_from_bytes

app = FastAPI(title="Fraud Detection API")
model = load_model("models/fraud_detector.h5")

@app.post("/score/")
async def score_receipt(file: UploadFile = File(...)):
    data = await file.read()

    # 1. PDF → PIL.Image via pdf2image
    filename = file.filename.lower()
    if filename.endswith(".pdf") or file.content_type == "application/pdf":
        try:
            pages = convert_from_bytes(data, size=(224,224), fmt="PNG")
            pil_img = pages[0]
        except Exception as e:
            raise HTTPException(400, f"PDF conversion error: {e}")
    else:
        # 2. Image formats → PIL.Image
        try:
            pil_img = Image.open(io.BytesIO(data)).convert("RGB").resize((224,224))
        except UnidentifiedImageError:
            raise HTTPException(400, "Unsupported image format or corrupted file")

    # 3. Preprocess & predict
    x = np.array(pil_img) / 255.0
    x = np.expand_dims(x, 0)

    prob = float(model.predict(x)[0][0])
    score = int(prob * 100)

    return {"fraud_score": score, "probability": prob}

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
