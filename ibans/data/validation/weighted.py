from typing import Iterable, Callable, Tuple


DigitExtractor = Callable[[str], slice]
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
        check_target = self.get_src(value)
        numbers = (int(x) for x in check_target)

        # weighted sum
        cs = sum(a * b for a, b in zip(numbers, self.weights))
        # modulo
        cs = cs % self.modulo
        cs_ready, cs = self.reminder_transformer(cs)

        # compliment
        if not cs_ready and self.comliment:
            cs = self.comliment - cs

        check_value = int(self.get_check(value))
        if cs != check_value:
            raise ValueError(f"Weigted sum digit mismatch ({cs} != {check_value})")
