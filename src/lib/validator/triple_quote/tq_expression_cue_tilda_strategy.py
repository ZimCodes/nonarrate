from .tq_expression_cue_strategy import TQExpressionCueStrategy
from ..ivalidator_chain import IValidatorChain


class TQExpressionCueTildaStrategy(TQExpressionCueStrategy):
    def __init__(self, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__("~", next_validator)
