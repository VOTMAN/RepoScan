from models.symbols import ChunkNode, FileNode, ImportNode

from .extract_js import queryJS
from .extract_jsx_tsx import queryTSX
from .extract_python import queryPython
from .extract_ts import queryTS

EXTRACTORS = {
    "py": queryPython,
    "js": queryJS,
    "ts": queryTS,
    "tsx": queryTSX,
    "jsx": queryTSX,
}

TYPE_MAP = {
    "function_definition": "function",
    "class_definition": "class",
    "function_declaration": "function",
    "class_declaration": "class",
    "interface_declaration": "interface",
    "type_alias_declaration": "type",
    "lexical_declaration": "variable",
    "assignment": "variable",
}


def parse_imports(import_matches: list[int, dict], code: str) -> list[str]:
    imports = []

    for _, capture in import_matches:
        if "module" in capture:
            node = capture["module"][0]
            name = code[node.start_byte : node.end_byte]

            names = []
            if "import_name" in capture:
                names = [
                    code[n.start_byte : n.end_byte] for n in capture["import_name"]
                ]
            imports.append(
                ImportNode(module=name, names=names, is_relative=name.startswith("."))
            )

    return imports


def get_export_pos(export_matches) -> set[tuple[int, int]]:
    positions = set()

    for _, capture in export_matches:
        if "decl" in capture:
            positions.add(capture["decl"][0].start_point)

    return positions


def parse_chunks(
    chunk_matches, exported_pos: set, code: str, file_node
) -> list[ChunkNode]:
    seen = set()
    chunks = []

    for _, capture in chunk_matches:
        chunk_ast = capture["chunk"][0]
        name_ast = capture["name"][0]

        if chunk_ast.start_point in seen:
            continue
        seen.add(chunk_ast.start_point)

        chunks.append(
            ChunkNode(
                name=code[name_ast.start_byte : name_ast.end_byte],
                kind=TYPE_MAP.get(chunk_ast.type, chunk_ast.type),
                path=file_node.path,
                content=code[chunk_ast.start_byte : chunk_ast.end_byte],
                start_line=chunk_ast.start_point[0] + 1,
                end_line=chunk_ast.end_point[0] + 1,
                exported=chunk_ast.start_point in exported_pos,
                language=file_node.language,
            )
        )

    return chunks


def extract(file_node: FileNode, tree, source_code):
    if not tree:
        file_node.chunks = [
            ChunkNode(
                name=file_node.path.split("/")[-1],
                kind="file",
                path=file_node.path,
                content=source_code,
                start_line=0,
                end_line=len(source_code),
                exported="unknown",
                language=file_node.language,
            )
        ]
        return file_node

    extractor = EXTRACTORS.get(file_node.extension)

    if extractor is None:
        return []

    raw = extractor(tree)

    exported_positions = get_export_pos(raw.get("exports", []))

    file_node.imports = parse_imports(raw.get("imports", []), source_code)

    file_node.exports = [
        source_code[capture["decl"][0].start_byte : capture["decl"][0].end_byte]
        for _, capture in raw.get("exports", [])
        if "decl" in capture
    ]
    file_node.chunks = parse_chunks(
        raw.get("chunks", []), exported_positions, source_code, file_node
    )

    return file_node
