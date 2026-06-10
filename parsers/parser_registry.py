from tree_sitter import Parser

from .languages import PARSER_MAP

PARSERS = {}

for ext, language in PARSER_MAP.items():
    parser = Parser(language)
    PARSERS[ext] = parser


def get_parser(extension: str) -> Parser | None:
    return PARSERS.get(extension)