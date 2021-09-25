import json

class QueryMapper(object):
    @staticmethod
    def to_definition(query):
        response = {
            "identified_terms": query.terms
        }

        return json.dumps(response)