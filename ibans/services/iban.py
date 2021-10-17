import re
from string import ascii_lowercase

from ibans.data.rules import lookup_rules_by_iso3166a2
from ibans.data.validation import ValidationError


class CountryLookupError(LookupError):
    """
    raised when country is a valid ISO-3166 country
    but unprocessable by this service
    """

    def __init__(self, country):
        self.country = country

    def __str__(self):
        return f"country `{self.country}` is unknown to this service"


class IBANValidationError(ValueError):
    def __init__(self, iban: str, reason: str):
        self.iban = iban
        self.reason = reason

    def __str__(self):
        return f"{self.reason}"


class IBANService:
    """service, responsible for validation of IBAN"""

    def _normalize_number(self, inp: str) -> str:
        """normalizes input string by removing all whitespaces and converting to uppercase"""

        return re.sub(r"\s", "", inp)

    def _validate_iban_checksum(self, iban: str) -> bool:
        """performs checsum validation of a normalized IBAN"""

        # 1. rearrange 4 characters at the start
        number = iban[4:] + iban[:4]

        # 2. convert letters to digits
        alphabet = {c.upper(): (10 + i) for i, c in enumerate(ascii_lowercase)}
        dest = ""
        for c in number:
            if c.isnumeric():
                dest += c
            else:
                dest += str(alphabet[c])

        # 3. interpret as an integer and check remainder
        return int(dest) % 97 == 1

    def _validate_iban_basic(self, inp: str):
        """performs checksum validation of an input IBAN"""

        # validate input length
        inp_len = len(inp)
        if inp_len < 4:
            raise IBANValidationError(
                inp, "input should have at least country code and a check sum"
            )

        elif inp_len > 34:
            raise IBANValidationError(
                inp, "valid IBAN must have no more that 34 characters"
            )

        # validate country
        country_a2 = inp[:2].upper()

        # lookup code rules
        country_rules = lookup_rules_by_iso3166a2(country_a2)
        if country_rules is None:
            raise CountryLookupError(country_a2)

        # validate according to country rules (at least - BBAN length)
        try:
            country_rules.validate(inp)
        except ValidationError as e:
            raise IBANValidationError(e.value, f"{e.cause}")

        # now goes IBAN checksum
        if not self._validate_iban_checksum(inp):
            raise IBANValidationError(inp, "IBAN check digits mismatch")

    def validate_iban(self, inp: str):
        """validates input string to be a valid IBAN number. raises `ValueError` and `CountryLookupError`"""

        inp = self._normalize_number(inp)
        return self._validate_iban_basic(inp)

    def is_valid_iban(self, inp: str) -> bool:
        """return `True` if input is a valid IBAN number"""

        inp = self._normalize_number(inp)
        try:
            self._validate_iban_basic(inp)
        except (IBANValidationError, CountryLookupError):
            return False

        return True
