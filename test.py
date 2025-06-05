import requests

# ส่ง prompt ผ่าน query parameter
response = requests.post("http://localhost:8000/generate", params={"prompt": "สวัสดี"})
print(response.json())
