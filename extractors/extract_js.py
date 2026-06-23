from tree_sitter import Query, QueryCursor, Tree

from parsers.languages import get_language
from parsers.queries import QUERIES

JAVASCRIPT_LANGUAGE = get_language("js")


def queryJS(tree: Tree):
    queries = QUERIES["js"]

    matches = {}
    for query_type, query_text in queries.items():
        query = Query(JAVASCRIPT_LANGUAGE, query_text)
        query_cursor = QueryCursor(query)
        match = query_cursor.matches(tree.root_node)
        matches[query_type] = match

    return matches
