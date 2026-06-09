from tree_sitter import Language, Parser

import tree_sitter_javascript as tsjs
import tree_sitter_typescript as tsts
import tree_sitter_python as tspy

from getStruct import load_repository


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


repo = load_repository(
    "https://github.com/VOTMAN/SynciNote"
)


for rel_path, node in repo.files.items():

    parser = get_parser(node.extension)

    if parser is None:
        continue

    with open(node.path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = parser.parse(code.encode("utf-8"))

    print(f"\n=== {rel_path} ===")

    root = tree.root_node

    print("Root:", root.type)

    for child in root.children[:10]:
        print("  ->", child.type)