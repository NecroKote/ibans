import re

import pytest
from fastapi.testclient import TestClient

from ibans.app import app
from ibans.api.v1.schema import IBANValidationResponseV1


client = TestClient(app)

OK_NUMBERS = (
    "   NL91 ABNA     0417 1643 00  ",
    "AZ27 NABZ 0135 0100 0000 0000 7944",
    "BE71 0961      2345 6769",
    "BR15 0000 0000 0000 1093 2840 814 P2",
)

FAILING_NUMBERS = (
    ("AZXX NABZ 0135 0100 0000 0000 7944", "check digits mismatch"),
    ("ABC", "should have at least"),
    ("Z" * 35, "no more that 34"),
    ("NN00----00001111----0000", "is unknown to this service"),
    ("AZ00---------", "length mismatch"),
    ("EE38 2200 2210 2014 5687", "check digits mismatch"),
)


def _v1_obj_from_response(response) -> IBANValidationResponseV1:
    try:
        response_obj = IBANValidationResponseV1.parse_obj(response.json())
    except:
        pytest.fail("Response scheme mismatch")

    else:
        return response_obj


@pytest.mark.parametrize("number", OK_NUMBERS)
def test_get_iban_ok(number):
    response = client.get("/v1/iban/is_valid", params={"number": number})

    assert response.status_code == 200

    response_obj = _v1_obj_from_response(response)
    assert response_obj.is_valid == True


@pytest.mark.parametrize("number", OK_NUMBERS)
def test_get_iban_ok_extra_args(number):
    response = client.get(
        "/v1/iban/is_valid", params={"number": number, "extra": 123456}
    )

    assert response.status_code == 200

    response_obj = _v1_obj_from_response(response)
    assert response_obj.is_valid == True


@pytest.mark.parametrize("case", FAILING_NUMBERS)
def test_get_iban_invalid(case):
    number, _ = case
    response = client.get("/v1/iban/is_valid", params={"number": number})

    assert response.status_code == 200

    response_obj = _v1_obj_from_response(response)
    assert response_obj.is_valid == False


def test_get_iban_number_missing():
    response = client.get("/v1/iban/is_valid", params={})

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "value_error.missing"


@pytest.mark.parametrize("number", OK_NUMBERS)
def test_post_iban_valid(number):
    response = client.post("/v1/iban/validate", json={"number": number})

    assert response.status_code == 204


@pytest.mark.parametrize("case", FAILING_NUMBERS)
def test_post_iban_invalid_with_reason(case):
    number, match = case
    response = client.post("/v1/iban/validate", json={"number": number})

    assert response.status_code == 400
    assert re.search(match, response.json()["detail"]) is not None


def test_post_iban_number_missing():
    response = client.post("/v1/iban/validate", json={})

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "value_error.missing"
