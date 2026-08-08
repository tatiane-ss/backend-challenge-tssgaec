from fastapi import FastAPI

app = FastAPI(
    title="JWT Validator API",
    description="API para validação de JWT conforme as regras do backend-challenge.",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
