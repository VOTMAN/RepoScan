import tree_sitter_javascript as tsjs
import tree_sitter_python as tspy
import tree_sitter_typescript as tsts
from tree_sitter import Language, Parser


PARSER_MAP = {
    "ts": Language(tsts.language_typescript()),
    "js": Language(tsjs.language()),
    "py": Language(tspy.language()),
}


PARSERS = {}

for ext, language in PARSER_MAP.items():
    parser = Parser(language)
    PARSERS[ext] = parser


def get_parser(extension: str) -> Parser | None:
    return PARSERS.get(extension)