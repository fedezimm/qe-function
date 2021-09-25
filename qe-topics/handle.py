import logging
import json
import azure.functions as func
from model.qe_topics.query import Query
from application.qe_topics.query_mapper import QueryMapper

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.') 

    query = None
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        query = req_body.get('query')

    if query:
        query = Query(query)

        #get the terms
        return QueryMapper.to_definition(query)


        #return func.HttpResponse('{"terms_identified":['+ term[0]+',' + term[1]+']}')
    else:
        return func.HttpResponse(
             "You should provide a query in order to get the topics!",
             status_code=400
        )
