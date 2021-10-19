from typing import Optional, List, Callable


IValidator = Callable[[str], None]


class ValidationError(ValueError):
    """basic error, raised when validation failed"""

    def __init__(self, validator: IValidator, value: str, exc: Exception = None):
        self.validator = validator
        self.value = value
        self.cause = exc


class ValidationBase:
    """base for custom validators"""

    validators: Optional[List[IValidator]] = None

    def validate(self, value: str):
        """validates the `value` by passing it over all of the `validators`"""

        if self.validators is None:
            return

        for validator in self.validators:
            try:
                validator(value)
            except ValueError as e:
                raise ValidationError(validator, value, e)
