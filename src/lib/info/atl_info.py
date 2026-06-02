import re
from typing import final


@final
class AtlInfo:
    """Holds line information involving Animation and Transformation language (atl).

    The information stored here is used to tell nonarrate to ignore all Animation and Transformation Language blocks
    and their contents.

    Reference:
        https://www.renpy.org/doc/html/transforms.html#atl-animation-and-transformation-language
    """

    __atl_pat: re.Pattern = re.compile(r'[^"\']*\b(?:image|layeredimage|show|scene|transform)\b[^:]+:')

    def __init__(self):
        self.is_atl = False
        self.indent_num = 0

    def reset(self):
        """Reset all values back to default."""
        self.is_atl = False
        self.indent_num = 0

    @classmethod
    def is_block(cls, strip_line: str) -> bool:
        """Check if stripped line is the start of an atl block.

        Args:
            strip_line: a line stripped of leading and trailing whitespace characters.

        Returns:
            a boolean determining if line is an Animation and Transformation Language block.
        """
        return True if cls.__atl_pat.match(strip_line) else False
