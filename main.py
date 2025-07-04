
from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Quiz Generation API",
    description="An API to generate quizzes from various sources.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Quiz Generation API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
