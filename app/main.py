from fastapi import FastAPI

from app.api.jwt_routes import router as jwt_router

app = FastAPI(
    title="JWT Validator API",
    description="API para validação de JWT conforme backend-challenge.",
    version="1.0.0",
)

app.include_router(jwt_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
