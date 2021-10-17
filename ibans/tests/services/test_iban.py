import pytest

from ibans.services.iban import CountryLookupError, IBANService, IBANValidationError

# https://en.wikipedia.org/wiki/IBAN
VALID_IBANS = {
    "AT42 6000 0000 0108 0751",
    "AZ27 NABZ 0135 0100 0000 0000 7944",
    "AL02 2121 1016 0000 0000 0030 0002",
    "AL47 2121 1009 0000 0002 3569 8741",
    "AL35202111090000000001234567",
    "AD48 0004 0029 0000 6166 2011",
    "BY42 AKBB 3014 0002 9364 3701 0000",
    "BE05 7320 4109 1675",
    "BG97 BACX 9660 1051 8766 29",
    "BA39 1860 0016 1184 5047",
    "GB29 NWBK 6016 1331 9268 19",
    "DE89 3704 0044 0532 0130 00",
    "KZ75 125K ZT10 0130 0335",
    "MD68 EX 0700 0002 2515 9105 EU",
    "   NL91 ABNA     0417 1643 00  ",
    "UA853996220000000260012335661",
    "FI21 1234 5600 0007 85   ",
    "SE45 5000 0000 0583 9825 7466",
    "EE38 2200 2210 2014 5685 ",
    "BE71 0961      2345 6769",
    "BR15 0000 0000 0000 1093 2840 814 P2",
    "FR76 3000 6000 0112 3456 7890 189",
    "DE91 1000 0000 0123 4567 89",
    "GR96 0810 0010 0000 0123 4567 890",
    "MU43 BOMM 0101 1234 5678 9101 000 MUR",
    "PK70 BANK 0000 1234 5678 9000",
    "HU42 1177 3016 1111 1018 0000 0000",
    "HU93 1160 0006 0000 0000 1234 5676",
    "PL10 1050 0099 7603 1234 5678 9123",
    "RO09 BCYP 0000 0012 3456 7890",
    "LC14 BOSL 1234 5678 9012 3456 7890 1234",
    "SA44 2000 0001 2345 6789 1234",
    "ES79 2100 0813 6101 2345 6789",
    "CH56 0483 5012 3456 7800 9",
    "GB98 MIDL 0700 9312 3456 78",
}


@pytest.fixture(scope="function")
def ibans():
    return IBANService()


@pytest.mark.parametrize("number", VALID_IBANS)
def test_expected_results(ibans: IBANService, number):
    assert ibans.is_valid_iban(number) == True

    try:
        ibans.validate_iban(number)
    except Exception:
        pytest.fail("Unexpected exception")


@pytest.mark.parametrize(
    "case",
    [
        ("ABC", "should have at least"),
        ("Z" * 35, "no more that 34"),
        ("AZ00---------", "length mismatch"),
        ("EE43 BOMM 0101 1234 5678 9101 000 MUR", "length mismatch"),
        ("EE38 2200 2210 2014 5687", "check digits mismatch"),
    ],
)
def test_malformed_inputs(ibans: IBANService, case):
    number, match = case

    with pytest.raises(IBANValidationError, match=match):
        ibans.validate_iban(number)

    assert ibans.is_valid_iban(number) == False


def test_unknown_country(ibans: IBANService):
    number = "NN00----00001111----0000"

    with pytest.raises(CountryLookupError, match="`NN` is unknown to this service"):
        ibans.validate_iban(number)

    assert ibans.is_valid_iban(number) == False
