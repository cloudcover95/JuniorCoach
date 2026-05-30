import subprocess
print("🚀 JuniorCoach starting...")
subprocess.Popen(["uvicorn", "backend.main:app", "--reload", "--port", "8000"])
print("Open frontend/index.html")