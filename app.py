import requests
import json
import pytest

BASE_URL = "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create"
API_KEY = "sh428739766321522266746152871799"
invalid_api_key = 'invalid'

payload = {
    "query": {
        "market": "UK",
        "locale": "en-GB",
        "currency": "GBP",
        "queryLegs": [
            {
                "originPlaceId": {"iata": "LHR"},
                "destinationPlaceId": {"iata": "EDI"},
                "date": {"year": 2024, "month": 4, "day": 10}
            }
        ],
        "adults": 1,
        "childrenAges": [],
        "cabinClass": "CABIN_CLASS_ECONOMY",
        "excludedAgentsIds": [],
        "excludedCarriersIds": [],
        "includedAgentsIds": [],
        "includedCarriersIds": []
    }
}

payload_json = json.dumps(payload)

headers_invalid = {
    'x-api-key': invalid_api_key,
    'Content-Type': 'application/json'
}

headers = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json'

}

# Test function to verify the status code of the API response
def test_response_status_code():
    response = requests.post(BASE_URL, headers=headers, data=payload_json)
    assert response.status_code == 200

# Test function to verify the content type of the API response
def test_response_content_type():
    response = requests.post(BASE_URL, headers=headers, data=payload_json)
    assert response.headers['Content-Type'] == 'application/json'

# Test function to verify the presence of required fields in the API response
def test_response_fields():
    response = requests.post(BASE_URL, headers=headers, data=payload_json).json()
    assert 'status' in response
    assert 'action' in response
    assert 'content' in response

def test_error_handling_invalid_credentials():
    response = requests.post(BASE_URL, headers=headers_invalid, data=payload_json)
    # Verify that the response status code is 401 (Unauthorized)
    assert response.status_code == 401
    # Verify that the response contains an error message indicating invalid credentials
    assert "Invalid API key" in response.json()['message']

