from whoosh.fields import ID
from haystack.backends.whoosh_backend import BaseEngine, WhooshSearchBackend, WhooshSearchQuery


class CustomSearchBackend(WhooshSearchBackend):
    """
    Custom search backend, to workaround the fact that haystack doesn't let
    use manage the stoplist (stopwords).
    """
    # Another solution could be to use a TEXT field with a custom analyzer like:
    # from whoosh.analysis import StandardAnalyzer
    # from whoosh.fields import TEXT
    # custom_analyser = StandardAnalyzer(stoplist=None, minsize=0)
    # field = TEXT(analyzer=custom_analyser)

    def build_schema(self, fields):
        content_field_name, schema = super(CustomSearchBackend, self).build_schema(fields)
        if "country" in schema._fields:
            schema.remove("country")
            schema.add("country", ID())
        return (content_field_name, schema)


class WhooshEngine(BaseEngine):
    backend = CustomSearchBackend
    query = WhooshSearchQuery
