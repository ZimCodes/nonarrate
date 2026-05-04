import re


class AtlInfo:
    """Holds line information involving Animation and Transformation language (atl).

    The information stored here is used to tell nonarrate to ignore all Animation and Transformation language blocks
    and their contents.

    Reference:
        https://www.renpy.org/doc/html/transforms.html#atl-animation-and-transformation-language
    """

    __atl_pat: re.Pattern = re.compile(r".*\b(?:image|layeredimage|show|scene|transform)\b[^:]+:")

    def __init__(self):
        pass
