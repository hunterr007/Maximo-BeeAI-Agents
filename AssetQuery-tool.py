import json
import requests
from urllib.parse import quote

def fetch_maximo_assets(query_string: str) -> str:
    base_maximo_url = "https://<MAXIMO_URL>/maximo/api/os/mxasset"
    headers = {
        "Content-Type": "application/json",
        "apikey": <MAXIMO_API_KEY>,
        "Accept": "application/json"
    }
    params = {
        "lean": "1",
        "ignorecollectionref": "1",
        "oslc.select": "assetnum,status,location,description,assettype"
    }

    # Split the query string into multiple queries
    queries = query_string.split(",")
    assets = []

    for query in queries:
        query = query.strip()

        # Initialize filter_query
        filter_query = ""

        # Check if the query is for assetnum or status
        if '=' in query:
            # It's a query with = (like status=Not Ready or assetnum=12345)
            key, value = query.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')  # Clean the value from quotes

            # If the key is status, handle it specifically
            if key.lower() == "status":
                # URL-encode the value of status (e.g., "Not Ready" becomes "Not%20Ready")
                encoded_value = quote(value)
                filter_query = f'status="{encoded_value}"'

            else:
                # For other fields like assetnum, simply URL-encode the value
                encoded_value = quote(value)
                filter_query = f'{key}="{encoded_value}"'

        else:
            # It's a simple assetnum query
            filter_query = f'assetnum="{quote(query)}"'

        # Now, update the params dictionary with the dynamic filter query
        params["oslc.where"] = filter_query

        # Print the constructed URL for debugging (to verify the query)
        print("Constructed URL with params:", base_maximo_url, params)

        try:
            # Make the GET request to the Maximo API with the correct params
            response = requests.get(base_maximo_url, headers=headers, params=params)

            # Print response status and body for debugging
            print("Response Status Code:", response.status_code)
            print("Response Body:", response.text)

            # If the request was successful, process the JSON data
            response.raise_for_status()
            data = response.json()

            # If there are assets in the response, append them to the assets list
            if "member" in data and data["member"]:
                for asset_data in data["member"]:
                    assets.append(asset_data)
            else:
                assets.append({"query": query, "message": "NOT FOUND"})

        except requests.exceptions.RequestException as e:
            assets.append({"query": query, "message": f"ERROR: {str(e)}"})
        except json.JSONDecodeError:
            assets.append({"query": query, "message": "ERROR: Invalid JSON response"})
        except KeyError:
            assets.append({"query": query, "message": "ERROR: Missing key in response"})

    # Return the results as a formatted JSON string
    return json.dumps(assets, indent=2)
