class LengthValidationRule:
    """length rule"""

    def __init__(self, length: int):
        self.length = length

    def __call__(self, value: str):
        if len(value) != self.length:
            raise ValueError(f"IBAN length mismatch ({len(value)} != {self.length})")
