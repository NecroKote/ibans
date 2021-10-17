import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ibans.services.iban import IBANService, CountryLookupError, IBANValidationError
from .schema import (
    IBANValidationRequestV1,
    IBANValidationResponseV1,
    IBANValidationFailureResponseV1,
)


router = APIRouter()
log = logging.getLogger("api.v1")


@router.get(
    "/iban/is_valid",
    response_model=IBANValidationResponseV1,
    tags=["iban"],
    summary="GET-based validator",
)
def get_iban_validator(
    number: str = Query(...),
    service: IBANService = Depends(IBANService),
):
    """provides simple True\False response to IBAN's validity request"""

    valid = service.is_valid_iban(number)
    return IBANValidationResponseV1(is_valid=valid)


@router.post(
    "/iban/validate",
    tags=["iban"],
    summary="POST-based validator",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={400: {"model": IBANValidationFailureResponseV1}},
)
def post_iban_validator(
    req: IBANValidationRequestV1,
    service: IBANService = Depends(IBANService),
):
    """validates provided IBAN. returns validation error description, if any"""
    try:
        service.validate_iban(req.number)

    except (IBANValidationError, CountryLookupError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {}
