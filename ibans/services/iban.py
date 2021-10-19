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
    """
    raise when IBAN validation failed.
    countains input number in `iban` and `reason` of failure
    """

    def __init__(self, iban: str, reason: str):
        self.iban = iban
        self.reason = reason

    def __str__(self):
        return f"{self.reason}"


class IBANService:
    """service, responsible for validation of IBAN"""

    _iban_alphabet_lookup = {
        char.upper(): (10 + idx) for idx, char in enumerate(ascii_lowercase)
    }
    _iban_checksum_modulo = 97
    _iban_min_length = 4
    _iban_max_length = 34

    def _normalize_string(self, string: str) -> str:
        """normalizes input string by removing all whitespaces and converting it to uppercase"""

        return re.sub(r"\s", "", string).upper()

    def _validate_iban_checksum(self, iban: str) -> bool:
        """performs checksum validation of a normalized IBAN"""

        # 1. rearrange 4 characters at the start
        number = iban[4:] + iban[:4]

        # 2. convert letters to digits
        dest = ""
        for char in number:
            if char.isnumeric():
                dest += char
            else:
                dest += str(self._iban_alphabet_lookup[char])
        iban_integer = int(dest)

        # 3. check remainder
        return iban_integer % self._iban_checksum_modulo == 1

    def _validate_iban_basic(self, iban: str):
        """performs checksum validation of an input IBAN"""

        # validate input length
        iban_len = len(iban)
        if iban_len < self._iban_min_length:
            raise IBANValidationError(
                iban, "input should have at least country code and a check sum"
            )

        elif iban_len > self._iban_max_length:
            raise IBANValidationError(
                iban,
                f"valid IBAN must have no more that {self._iban_max_length} characters",
            )

        # valiate input consists only from alpha-numerical characters
        elif not iban.isalnum():
            raise IBANValidationError(iban, "IBAN contains non alpha-numerical symbols")

        country_code = iban[:2].upper()

        # lookup code rules
        country_rules = lookup_rules_by_iso3166a2(country_code)
        if country_rules is None:
            raise CountryLookupError(country_code)

        # validate according to country rules (at least - BBAN length)
        try:
            country_rules.validate(iban)
        except ValidationError as e:
            raise IBANValidationError(e.value, f"{e.cause}")

        # now goes IBAN checksum
        if not self._validate_iban_checksum(iban):
            raise IBANValidationError(iban, "IBAN check digits mismatch")

    def validate_iban(self, iban: str):
        """validates input string to be a valid IBAN number. raises `IBANValidationError` and `CountryLookupError`"""

        iban_normalized = self._normalize_string(iban)
        return self._validate_iban_basic(iban_normalized)

    def is_valid_iban(self, iban: str) -> bool:
        """return `True` if input is a valid IBAN number"""

        iban_normalized = self._normalize_string(iban)
        try:
            self._validate_iban_basic(iban_normalized)
        except (IBANValidationError, CountryLookupError):
            return False

        return True
