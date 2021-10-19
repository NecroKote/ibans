from typing import Optional, List

from .validation import ValidationBase, LengthValidationRule, IValidator
from .validation.weighted import WeightedSumValidationRule, ZeroPassTransformer

__all__ = ["BasicIBANRules", "lookup_rules_by_iso3166a2"]


class BasicIBANRules(ValidationBase):
    """basic rule class containing length expectation"""

    length: int

    def __init__(self, length: int):
        self.length = length
        self.validators = [LengthValidationRule(length)] + self.country_validators()

    def country_validators(self) -> List[IValidator]:
        """additional validators, intended for extension by descendent classes"""

        return []


class AL_IBANRules(BasicIBANRules):
    """Albania-specific IBAN rules"""

    def country_validators(self) -> List[IValidator]:
        return [
            WeightedSumValidationRule(
                weights=(9, 7, 3, 1) * 2,
                modulo=10,
                compliment=10,
                src_extractor=lambda s: s[4:11],
                check_extractor=lambda s: s[11],
                reminder_transformer=ZeroPassTransformer,
            )
        ]


class HU_IBANRules(BasicIBANRules):
    """Hungary-specific IBAN rules"""

    def country_validators(self) -> List[IValidator]:
        weights = (9, 7, 3, 1) * 4

        return [
            # bank + branch
            WeightedSumValidationRule(
                weights=weights,
                modulo=10,
                compliment=10,
                src_extractor=lambda s: s[4:11],
                check_extractor=lambda s: s[11],
                reminder_transformer=ZeroPassTransformer,
            ),
            # account number
            WeightedSumValidationRule(
                weights=weights,
                modulo=10,
                compliment=10,
                src_extractor=lambda s: s[12:27],
                check_extractor=lambda s: s[27],
                reminder_transformer=ZeroPassTransformer,
            ),
        ]


_iso3166a2_rule_set = {
    "AL": AL_IBANRules(28),
    "AD": BasicIBANRules(24),
    "AT": BasicIBANRules(20),
    "AZ": BasicIBANRules(28),
    "BH": BasicIBANRules(22),
    "BY": BasicIBANRules(28),
    "BE": BasicIBANRules(16),
    "BA": BasicIBANRules(20),
    "BR": BasicIBANRules(29),
    "BG": BasicIBANRules(22),
    "CR": BasicIBANRules(22),
    "HR": BasicIBANRules(21),
    "CY": BasicIBANRules(28),
    "CZ": BasicIBANRules(24),
    "DK": BasicIBANRules(18),
    "DO": BasicIBANRules(28),
    "TL": BasicIBANRules(23),
    "EG": BasicIBANRules(29),
    "SV": BasicIBANRules(28),
    "EE": BasicIBANRules(20),
    "FO": BasicIBANRules(18),
    "FI": BasicIBANRules(18),
    "FR": BasicIBANRules(27),
    "GE": BasicIBANRules(22),
    "DE": BasicIBANRules(22),
    "GI": BasicIBANRules(23),
    "GR": BasicIBANRules(27),
    "GL": BasicIBANRules(18),
    "GT": BasicIBANRules(28),
    "HU": HU_IBANRules(28),
    "IS": BasicIBANRules(26),
    "IQ": BasicIBANRules(23),
    "IE": BasicIBANRules(22),
    "IL": BasicIBANRules(23),
    "IT": BasicIBANRules(27),
    "JO": BasicIBANRules(30),
    "KZ": BasicIBANRules(20),
    "XK": BasicIBANRules(20),
    "KW": BasicIBANRules(30),
    "LV": BasicIBANRules(21),
    "LB": BasicIBANRules(28),
    "LY": BasicIBANRules(25),
    "LI": BasicIBANRules(21),
    "LT": BasicIBANRules(20),
    "LU": BasicIBANRules(20),
    "MK": BasicIBANRules(19),
    "MT": BasicIBANRules(31),
    "MR": BasicIBANRules(27),
    "MU": BasicIBANRules(30),
    "MC": BasicIBANRules(27),
    "MD": BasicIBANRules(24),
    "ME": BasicIBANRules(22),
    "NL": BasicIBANRules(18),
    "NO": BasicIBANRules(15),
    "PK": BasicIBANRules(24),
    "PS": BasicIBANRules(29),
    "PL": BasicIBANRules(28),
    "PT": BasicIBANRules(25),
    "QA": BasicIBANRules(29),
    "RO": BasicIBANRules(24),
    "LC": BasicIBANRules(32),
    "SM": BasicIBANRules(27),
    "ST": BasicIBANRules(25),
    "SA": BasicIBANRules(24),
    "RS": BasicIBANRules(22),
    "SC": BasicIBANRules(31),
    "SK": BasicIBANRules(24),
    "SI": BasicIBANRules(19),
    "ES": BasicIBANRules(24),
    "SD": BasicIBANRules(18),
    "SE": BasicIBANRules(24),
    "CH": BasicIBANRules(21),
    "TN": BasicIBANRules(24),
    "TR": BasicIBANRules(26),
    "UA": BasicIBANRules(29),
    "AE": BasicIBANRules(23),
    "GB": BasicIBANRules(22),
    "VA": BasicIBANRules(22),
    "VG": BasicIBANRules(24),
}


def lookup_rules_by_iso3166a2(country_code: str) -> Optional[BasicIBANRules]:
    """return `BasicIBANRules` for a given country by it's ISO 3166 alpha-2 code"""

    country_code = country_code.strip().upper()
    if len(country_code) != 2:
        raise ValueError("`country_code` should contain excatly 2 characters")

    return _iso3166a2_rule_set.get(country_code)
