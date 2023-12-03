import requests

def get_skyscanner_api_key():
    # Replace 'YOUR_SKYSCANNER_API_KEY' with your actual Skyscanner API key
    return 'YOUR_SKYSCANNER_API_KEY'

def skyscanner_autosuggest(query):
    endpoint = "https://partners.api.skyscanner.net/apiservices/autosuggest/v1.0"
    api_key = get_skyscanner_api_key()
    
    params = {
        'apiKey': api_key,
        'query': query,
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if 'Places' in data:
        return data['Places'][0]['PlaceId']
    else:
        return None

def get_cheapest_flight(origin, destination, outbound_date):
    endpoint = "https://partners.api.skyscanner.net/apiservices/browsequotes/v1.0"
    api_key = get_skyscanner_api_key()

    origin_id = skyscanner_autosuggest(origin)
    destination_id = skyscanner_autosuggest(destination)

    if origin_id and destination_id:
        params = {
            'apiKey': api_key,
            'originPlace': origin_id,
            'destinationPlace': destination_id,
            'outboundDate': outbound_date,
            'sortBy': 'price',
            'sortOrder': 'asc',
            'pageSize': 1,
        }

        response = requests.get(endpoint, params=params)
        data = response.json()

        if 'Quotes' in data and data['Quotes']:
            cheapest_quote = data['Quotes'][0]
            return cheapest_quote
    return None

if __name__ == "__main__":
    origin = input("Enter the origin city or airport code: ")
    destination = input("Enter the destination city or airport code: ")
    outbound_date = input("Enter the outbound date (YYYY-MM-DD): ")

    cheapest_flight = get_cheapest_flight(origin, destination, outbound_date)

    if cheapest_flight:
        print("\nCheapest Flight Details:")
        print(f"Price: {cheapest_flight['MinPrice']} {cheapest_flight['Currency']}")
        print(f"Direct Flight: {'Yes' if cheapest_flight['Direct'] else 'No'}")
        print(f"Carrier: {cheapest_flight['CarrierIds']}")
    else:
        print("No flight information available.")
