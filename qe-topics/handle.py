import logging

import azure.functions as func
from model.qe_topics.query import Query

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if query:
        query = Query(query)
        term = query.terms
        return func.HttpResponse('{"terms_identified":['+ term[0]+',' + term[1]+']}')
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
