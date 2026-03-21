from abc import ABC
import re
from .ivalidator_chain import IValidatorChain


class IValidatorChainSolo(IValidatorChain, ABC):
    """Provide an instance-focused abstract interface for processing validation requests through a chain of handlers."""

    def __init__(self, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat: "re.Pattern | None" = None

    def is_valid(self, line: str) -> bool:
        if self._validate_pat and self._validate_pat.match(line):
            return True
        elif self._next_validator:
            return self._next_validator.is_valid(line)
        return False
