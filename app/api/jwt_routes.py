from fastapi import APIRouter

from app.schemas.jwt_schemas import (
    JWTValidationRequest,
    JWTValidationResponse,
)
from app.services.jwt_validation_service import validate_jwt

router = APIRouter(
    prefix="/api/v1/jwt",
    tags=["JWT"],
)


@router.post(
    "/validate",
    response_model=JWTValidationResponse,
    status_code=200,
)
def validate_jwt_endpoint(
    request: JWTValidationRequest,
) -> JWTValidationResponse:
    is_valid = validate_jwt(request.token)

    return JWTValidationResponse(valid=is_valid)
