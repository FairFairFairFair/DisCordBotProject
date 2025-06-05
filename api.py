from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

# Define the request body model
class RequestBody(BaseModel):
    prompt: str

# Use raw string to avoid Unicode errors
model_name = r"C:\Users\user\Desktop\Discord-Mybot\models\fine-tuned-deepseek-r1-1.5b"
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model, tokenizer = None, None

@app.post("/generate")
async def generate_text(body: RequestBody):
    print(f"Received prompt: {body.prompt}")  # ใช้ body.prompt แทน
    inputs = tokenizer(body.prompt, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=100)
    return {"response": tokenizer.decode(outputs[0], skip_special_tokens=True)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
