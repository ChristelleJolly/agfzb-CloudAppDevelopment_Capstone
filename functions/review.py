#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result
import requests
import json

def main(dict):

    try:
        if "dealerId" not in dict:
            return {"error": "Missing dealerId parameter"}
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        database = client["reviews"]
        reviews = database.get_query_result(selector={"dealership": dict["dealerId"]})
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"reviews" : reviews.all()}
