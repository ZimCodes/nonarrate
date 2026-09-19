from .parenthetical_rule import ParentheticalRule


class BasicParentheticalRule(ParentheticalRule):
    """Filters parenthetical containing common introspection word or phrase.

    Example:
    mc "(Thoughts) Hmm... That door looks mighty sturdy."
    """

    def __init__(self):
        introspection = ["thoughts?", "think(ing)?", "inner voices?", "inner monologue"]
        super().__init__("|".join(introspection))
