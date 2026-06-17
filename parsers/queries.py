QUERIES = {
    "py": {
        "imports": """
            (import_statement
                name: (dotted_name) @module)

            (import_from_statement
                module_name: (dotted_name) @module)
        """,
        "chunks": """
            (function_definition
                name: (identifier) @name
            ) @chunk

            (class_definition
                name: (identifier) @name
            ) @chunk

            ( assignment
                left: (identifier) @name
            ) @chunk

            ( decorator
            	(call
                	function: (identifier) @name
                )
            ) @chunk

            ( expression_statement
            	(call
                	function: (identifier) @name
                )
            ) @chunk
        """,
    },
    "js": {
        "imports": """
            (import_statement
                (import_clause
                    (named_imports
                        (import_specifier
                            name: (identifier) @import_name
                        )
                    )
                )
                source: (string (string_fragment) @module)
            )
        """,
        "chunks": """
            (function_declaration
                name: (identifier) @name
            ) @chunk

            (class_declaration
                name: (identifier) @name
            ) @chunk
        """,
        "exports": """
            (export_statement
                declaration: (_) @decl
            )

            (export_statement
                value: (identifier) @default_export
            )
        """,
    },
    "ts": {
        "imports": """
            (import_statement
                (import_clause
                    (named_imports
                        (import_specifier
                            name: (identifier) @import_name
                        )
                    )
                )
                source: (string (string_fragment) @module)
            )
        """,
        "chunks": """
            (function_declaration
                name: (identifier) @name
            ) @chunk

            (class_declaration
                name: (type_identifier) @name
            ) @chunk

            (interface_declaration
                name: (type_identifier) @name
            ) @chunk

            (type_alias_declaration
                name: (type_identifier) @name
            ) @chunk
            (lexical_declaration
                (variable_declarator
                    name: (identifier) @name
                )
            ) @chunk
        """,
        "exports": """
            (export_statement
                declaration: (_) @decl
            )

            (export_statement
                value: (identifier) @default_export
            )
        """,
    },
}

QUERIES["tsx"] = QUERIES["jsx"] = QUERIES["ts"]
