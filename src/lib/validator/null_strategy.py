from .ivalidator_chain_solo import IValidatorChainSolo
from typing import final


@final
class NullStrategy(IValidatorChainSolo):
    """An empty strategy for a null object pattern."""

    pass
