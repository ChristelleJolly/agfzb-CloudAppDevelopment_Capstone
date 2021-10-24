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

        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        database = client["reviews"]
        
        next_id = database.doc_count()+1
        
        data = {
            "id": next_id,
            "name": dict["name"],
            "dealership": dict["dealership"],
            "review": dict["review"],
            "purchase": dict["purchase"],
            "another": dict["another"],
            "purchase_date": dict["purchase_date"],
            "car_make": dict["car_make"],
            "car_model": dict["car_model"],
            "car_year": dict["car_year"],
        }
        
        # Create a document using the Database API
        my_document = database.create_document(data)

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return my_document
