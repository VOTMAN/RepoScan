from tree_sitter import Query, QueryCursor, Tree

from parsers.languages import get_language
from parsers.queries import QUERIES

TYPESCRIPT_LANGUAGE = get_language("ts")


def queryTS(tree: Tree):
    queries = QUERIES["ts"]

    matches = {}
    for query_type, query_text in queries.items():
        query = Query(TYPESCRIPT_LANGUAGE, query_text)
        query_cursor = QueryCursor(query)
        match = query_cursor.matches(tree.root_node)
        matches[query_type] = match

    return matches
