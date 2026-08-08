from pydantic import BaseModel, ConfigDict, StrictStr


class JWTValidationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    token: StrictStr


class JWTValidationResponse(BaseModel):
    valid: bool
