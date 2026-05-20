from .tq_expression_cue_strategy import TQExpressionCueStrategy
from ..ivalidator_chain import IValidatorChain


class TQExpressionCueAsteriskStrategy(TQExpressionCueStrategy):
    def __init__(self, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(r"\*", next_validator)
