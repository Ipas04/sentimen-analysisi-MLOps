from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import mlflow
import logging
from config import config

# Muat model yang sudah dilatih
model = joblib.load(config['model']['path'])

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Pengaturan logging
logging.basicConfig(filename=config['logging']['log_file'], level=config['logging']['level'])

# Input data model
class Review(BaseModel):
    review_text: str

@app.post(config['api']['base_url'])
def predict(review: Review):
    # Log parameter
    logging.info(f"Review received: {review.review_text}")

    # Prediksi sentimen
    sentiment = model.predict([review.review_text])[0]
    
    # Log metrik (contoh: sentimen)
    mlflow.log_metric("sentiment_score", sentiment)

    # Mengembalikan hasil prediksi
    return {"sentiment": sentiment}

# Jalankan server FastAPI pada host dan port yang ditentukan di config.yaml
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config['api']['host'], port=config['api']['port'])
