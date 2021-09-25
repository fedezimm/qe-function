import logging
import azure.functions as func
from controller.topic import getTopic

def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('GET /topics')

  term = req.params.get('term')
  if term:
    response = getTopic(term)
    return func.HttpResponse(f"{response}")
  else:
    return func.HttpResponse(
      "Term to get topics missing",
      status_code=400
    )
