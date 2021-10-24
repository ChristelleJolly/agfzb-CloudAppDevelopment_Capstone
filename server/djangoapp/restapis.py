import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os
import sys
from dotenv import load_dotenv
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):

    response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    status_code = response.status_code
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, data, **kwargs):
    response = requests.post(url, params=kwargs, json=data)
    status_code = response.status_code
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealers_from_state(url, **kwargs):
    results = []
    if "state" not in kwargs:
        raise KeyError("state expected")
    json_result = get_request(url, state=kwargs.get("state"))
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer_doc in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    if "dealerid" not in kwargs:
        raise KeyError("dealerid expected")
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerid=kwargs.get("dealerid"))
    if json_result:
        reviews = json_result["reviews"]
        for review_doc in reviews:
            review_obj = DealerReview(id=review_doc["id"], name=review_doc["name"], car_make=review_doc["car_make"], car_model=review_doc["car_model"], \
                car_year=review_doc["car_year"], dealership=review_doc["dealership"], purchase=review_doc["purchase"], \
                purchase_date=review_doc["purchase_date"], review=review_doc["review"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    load_dotenv()

    api_key = os.getenv("WATSON_NLU_API_KEY")
    url = os.getenv("WATSON_NLU_URL")

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)
    sentiment_label = ""

    try:
        json_result = natural_language_understanding.analyze(
            text=text,
            features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()
    
        if json_result and json_result["sentiment"]:
            sentiment_label = json_result["sentiment"]["document"]["label"]
    except:
        print("Unexpected error with NLU service:", sys.exc_info()[0])
    
    return sentiment_label

