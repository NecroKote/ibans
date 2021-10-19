from typing import Iterable, Callable, Tuple


DigitExtractor = Callable[[str], str]
ReminderTransformer = Callable[[int], Tuple[bool, int]]

IdentityTransformer = lambda x: (False, x)
ZeroPassTransformer = lambda x: (x == 0, x)


class WeightedSumValidationRule:
    """weighted sum validation"""

    def __init__(
        self,
        weights: Iterable[int],
        modulo: int,
        src_extractor: DigitExtractor,
        check_extractor: DigitExtractor,
        compliment: int = None,
        reminder_transformer: ReminderTransformer = IdentityTransformer,
    ):
        self.weights = weights
        self.modulo = modulo
        self.comliment = compliment
        self.get_src = src_extractor
        self.get_check = check_extractor
        self.reminder_transformer = reminder_transformer

    def __call__(self, value: str):
        # extract the region of interest from `value`
        check_string = self.get_src(value)

        # extract "check digit" from `value`
        check_digit = self.get_check(value)

        if not check_string.isnumeric():
            raise ValueError("non-digit input within checked region")

        numbers = (int(x) for x in check_string)

        # calculate the weighted sum
        cs = sum(a * b for a, b in zip(numbers, self.weights))
        cs = cs % self.modulo

        # transform the checksum, if necessery
        cs_ready, cs = self.reminder_transformer(cs)

        # use "compliment" if result if not already prepared by transformer
        if not cs_ready and self.comliment:
            cs = self.comliment - cs

        # compare the two
        if str(cs) != check_digit:
            raise ValueError(f"Weigted sum digit mismatch ({cs} != {check_digit})")
