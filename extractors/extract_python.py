from tree_sitter import Query, QueryCursor, Tree

from parsers.languages import get_language
from parsers.queries import QUERIES

PYTHON_LANGUAGE = get_language("py")


def queryPython(tree: Tree):
    queries = QUERIES["py"]

    matches = {}
    for query_type, query_text in queries.items():
        query = Query(PYTHON_LANGUAGE, query_text)
        query_cursor = QueryCursor(query)
        match = query_cursor.matches(tree.root_node)
        matches[query_type] = match

    return matches
