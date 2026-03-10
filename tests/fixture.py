from lib.arg.cli_parser import CLIParser

DUMMY_PATH = "tests/dummy"  # Path to dummy file directory


def get_args(parser: CLIParser, arguments: str | list):
    if isinstance(arguments, str):
        return parser.parse_args(arguments.split())
    return parser.parse_args(arguments)


def get_dialogue_list(valid_indexes: list[int], dialogues: dict[int, str]):
    valid_lines = []
    invalid_lines = []
    for i, line in dialogues.items():
        if i in valid_indexes:
            valid_lines.append(line)
        else:
            invalid_lines.append(line)
    return valid_lines, invalid_lines
