from fastapi import FastAPI
import uvicorn

from prediction_route import router as prediction_router
from config.logging_config import LogConfig

LogConfig().configure()

app = FastAPI(
    title="Defasagem Prediction API",
    version="1.0.0",
    description="API para prever risco de defasagem futura",
)

app.include_router(prediction_router)


@app.get("/")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
