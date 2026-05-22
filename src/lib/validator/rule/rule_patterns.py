from .rule import Rule
from .cue_rule import CueRule
from .basic_char_rule import BasicCharRule
from .basic_object_rule import BasicObjectRule
from .tq_cue_rule import TQCueRule
from .tq_text_tag_rule import TQTextTagRule
from .var_object_rule import VarObjectRule
from .object_rule import ObjectRule
from .char_rule import CharRule
from .text_tag_rule import TextTagRule
from enum import Enum


class DialogueRules(Enum):
    # "Hey! I'm actually a narrator."
    BASIC = Rule(r'^(["\'])(?:\\.|(?!\1).)+(?:\1\s*with .+)?[^:]$')
    # mc "{i}Maybe there's food left over.{/i}"
    # mc "{tag}{i}Maybe there's food left over.{/i}{/tag}"
    ITALIC = Rule(
        r'^[^=]+([\'"])(?:{\w+(?:=[^}]+)?})*\{i\}((?:(?!\{/?i\}).)+)(?:\{/?i\})?(?:[.?!]?(?:{/\w+})*|(?:{/\w+})*[/?!]?)\s*(?:\1|\1\s*with .+)?$')
    # mc "............."
    # mc "{tag}........................{/tag}"
    # mc "!!!"
    # mc "????"
    ONLY_PUNCTUATION = Rule(r'^[^=]+([\'"])(?:{\w+(?:=[^}]+)?})*[.?!]+(?:{/\w+})*\s*(?:\1|\1\s*with .+)?$')
    # mc "(It's got to be here somewhere.)"
    # mc "{tag}(It's got to be here somewhere.){/tag}"
    PARENTHESIS = Rule(
        r'^[^=]+([\'"])(?:{\w+(?:=[^}]+)?})*(?:\\|\\[\'"])?\([^()]+(?:\\?\)(?:\\[\'"])?)?(?:[.?!]?(?:{/\w+})*|(?:{/\w+})*[/?!]?)\s*(?:\1|\1\s*with .+)?$')
    # mc "~yawns~"
    # mc "{tag}~yawns~{/tag}"
    EXPRESSION_CUE_TILDA = CueRule('~')
    # mc *smiles*
    # mc "{tag}*smiles*{/tag}"
    EXPRESSION_CUE_ASTERISK = CueRule(r'\*')
    # elnor "{fzs}This is a small bold font tag.{/fzs}"
    # gabby "{ba=100}Big bold asterisk text!{/ba}"
    TEXT_TAG = TextTagRule


# NOTE: DynamicCharacter() is an outdated variant of Character()
# REF: https://www.renpy.org/wiki/renpy/doc/reference/functions/DynamicCharacter
class SpeakerRules(Enum):
    CHARACTER = CharRule
    # "My Thoughts" "Hey there!"
    CHARACTER_BASIC = BasicCharRule()
    # " " "Hey there!"
    CHARACTER_NONE = Rule(r'([\'"])\s*\1\s*([\'"])[^\2]+\2?')
    OBJECT = ObjectRule
    # Character("My Thoughts")
    OBJECT_BASIC = [BasicObjectRule()]
    OBJECT_ITALIC = [Rule(r"what_italic\s*=\s*True"), Rule(r"what_prefix\s*=\s*([\"'])\{i}\1"),
                     Rule(r"(?:Dynamic)?Character\(\s*(['\"])\s*\{i\}[^\"']+\{/?i\}\s*\1")]
    # Character(None)
    OBJECT_NONE = [Rule(r"(?:Dynamic)?Character\s*\(\s*(?:name\s*=\s*)?None.*\)"), Rule(r"(?:Dynamic)?Character\s*\(\s*\)"),
                   Rule(r"(?:Dynamic)?Character\s*\(\s*[\"']\s*[\"']\s*.*\)"),
                   Rule(r"(?:Dynamic)?Character\s*\((?!\s*[\"']{2}|\s*name\s?=|\s*None)(?:\s*[\w_]+\s*=\s*.+)+\)"),
                   # Filters empty translation function, '_()' and '_("")'
                   # Ref: https://www.renpy.org/doc/html/translation.html#menu-and-string-translations
                   Rule(r"(?:Dynamic)?Character\s*\(\s*_\(\s*(?:[\"']\s*[\"']\s*)?\)")]
    # narrator_variable = Character(...)
    OBJECT_VAR = VarObjectRule

class TripleQuoteRules(Enum):
    EXPRESSION_CUE_TILDA = TQCueRule('~')
    EXPRESSION_CUE_ASTERISK = TQCueRule(r'\*')
    ITALIC = Rule(r'^(?:{\w+(?:=[^}]+)?})*\{i\}((?:(?!\{/?i\}).)+)(?:\{/?i\})?(?:[.?!]?(?:{/\w+})*|(?:{/\w+})*[/?!]?)$')
    ONLY_PUNCTUATION = Rule(r'^(?:{\w+(?:=[^}]+)?})*[.?!]+(?:{/\w+})*$')
    PARENTHESIS = Rule(r'^(?:{\w+(?:=[^}]+)?})*(?:\\|\\[\'"])?\([^()]+(?:\\?\)(?:\\[\'"])?)?(?:[.?!]?(?:{/\w+})*|(?:{/\w+})*[/?!]?)$')
    TEXT_TAG = TQTextTagRule
