from pydantic import BaseModel


class IBANValidationRequestV1(BaseModel):
    """model, used for a POST request's json body"""

    number: str


class IBANValidationResponseV1(BaseModel):
    """model of a GET response"""

    is_valid: bool


class IBANValidationFailureResponseV1(BaseModel):
    """model of a POST response, in case of validation failure"""

    details: str
