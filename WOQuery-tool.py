import json
import requests
from urllib.parse import quote
from datetime import datetime

def fetch_maximo_workorder(query_string: str) -> str:
    base_maximo_url = "https://maximo.eam360.com/maximo/api/os/MXWODETAIL"
    headers = {
        "Content-Type": "application/json",
        "apikey": "rpqsm7nlu25bnj4njh67ico9o6165dfsn93n2g90",
        "Accept": "application/json"
    }
    params = {
        "lean": "1",
        "ignorecollectionref": "1",
        "oslc.select": "wonum,siteid,assetnum,status,location,description,worktype,reportdate"
    }

    # Split the query string into multiple queries
    queries = query_string.split(",")
    workorders = []

    # Current date to handle the "today" query scenario
    today = datetime.today().strftime('%Y-%m-%d')

    for query in queries:
        query = query.strip()

        # Initialize filter_query
        filter_query = ""

        if "#" in query:
            # It's a query with '#' (like Work Order=WO123 or status=WAPPR)
            key, value = query.split("#", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')  # Clean the value from quotes
            if key.lower() == "wo":
                # Query by work order number
                filter_query = 'wonum="' + quote(value) + '"'
        elif "=" in query:
            key, value = query.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"') 
            if key.lower() == "status":
                # Query by work order status (e.g., WAPPR)
                filter_query = 'status="' + value + '"'
        elif "reported on" in query:
            key, value = query.split("reported on", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"') 
            #Query by date (e.g., today)
            if key.lower() == "today":
                # Handle "today" query, use the current date
                #filter_query = 'reportdate="{quote(today)}"'
                filter_query = 'reportdate="' + quote(today) + '"'
            else:
                # Use a specific date passed by the user
                filter_query = 'reportdate="' + quote(value) + '"'
        else:
            filter_query = 'wonum="' + quote(value) + '"'

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

            # If there are work orders in the response, append them to the workorders list
            if "member" in data and data["member"]:
                for workorder_data in data["member"]:
                    workorders.append(workorder_data)
            else:
                workorders.append({"query": query, "message": "NOT FOUND"})

        except requests.exceptions.RequestException as e:
            workorders.append({"query": query, "message": f"ERROR: {str(e)}"})
        except json.JSONDecodeError:
            workorders.append({"query": query, "message": "ERROR: Invalid JSON response"})
        except KeyError:
            workorders.append({"query": query, "message": "ERROR: Missing key in response"})

    # Return the results as a formatted JSON string
    return json.dumps(workorders, indent=2)
