QUERIES = {
    "py": {
        "imports": """
            (import_statement name: (dotted_name) @import_path)
            (import_from_statement module_name: (dotted_name) @import_path)
        """,

        "chunks": """
            (function_definition name: (identifier) @name) @func
            (class_definition name: (identifier) @name) @class
        """,
    },
    "js": {
        "imports": "(import_declaration) @import",

        "chunks": """
            (function_declaration name: (identifier) @name) @func
            (class_declaration name: (identifier) @name) @class
        """,
    },
    "ts": {
    "imports": """
        (import_statement source: (string (string_fragment) @import_path))
    """,

    "chunks": """
        (export_statement declaration: (function_declaration name: (identifier) @name) @chunk)
        (export_statement declaration: (class_declaration name: (type_identifier) @name) @chunk)
        (export_statement declaration: (interface_declaration name: (type_identifier) @name) @chunk)
        (export_statement declaration: (type_alias_declaration name: (type_identifier) @name) @chunk)

        (function_declaration name: (identifier) @name) @chunk
        (class_declaration name: (type_identifier) @name) @chunk
    """,

    "exports": """
        (export_statement declaration: (_) @decl)
        
        (export_statement value: (identifier) @default_export)
    """
    },
}