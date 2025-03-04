import json
import requests
 
def custom_weather_service(cities_input_string: str) -> dict:
   #print(f"cities_input_string")
   base_weather_url="https://wttr.in/"
   cities_input = cities_input_string.split(",")
   cities = []
   for city in cities_input:
        # Ensure to get the JSON format: '?format=j1'
        city_temp_url = base_weather_url + city + "?format=j1"
        response = requests.get(city_temp_url)
        #response = requests.get(city_temp_url, verify=False)
        if (response.status_code == 200):    
           # convert from byte to text
           byte_content = response.content
           text_content = byte_content.decode("utf-8")          
           # load json
           content = json.loads(text_content)
           # extract temperature
           temperature = content['current_condition'][0]['temp_C']
           cities.append({"city": city, "temperature":temperature})
        else:
         cities.append({"city": f"{city} ERROR", "temperature":0})
   sorted_by_temperature =  sorted(cities, key=lambda x: (x['city'],x['temperature']), reverse=True)
   result_text_list = json.dumps(sorted_by_temperature)  
   return result_text_list