# Challenge_1b/download_model.py
import os
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'all-MiniLM-L6-v2'
MODEL_PATH = './model'

def download_model():
    print(f"Downloading model: {MODEL_NAME} to {MODEL_PATH}")
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)
    model = SentenceTransformer(MODEL_NAME)
    model.save(MODEL_PATH)
    print(f"✅ Model downloaded and saved successfully to {MODEL_PATH}")

if __name__ == "__main__":
    download_model()