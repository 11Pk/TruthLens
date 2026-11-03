from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to TruthLens Backend",
        "status": "Backend is running"
    }