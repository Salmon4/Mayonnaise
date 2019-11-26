# import http.client
#
# conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")
#
# headers = {
#     'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
#     'x-rapidapi-key': "eedd51b020mshc462a1043ca26dep113106jsn43a6a1a8e712"
#     }
#
# conn.request("GET", "/seasons/", headers=headers)
#
# res = conn.getresponse()
# data = res.read()

# import requests
#
# url = "https://api-nba-v1.p.rapidapi.com/seasons/"
#
# headers = {
#     'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
#     'x-rapidapi-key': "eedd51b020mshc462a1043ca26dep113106jsn43a6a1a8e712"
#     }
#
# response = requests.request("GET", url, headers=headers)
#
# print(response.text)

response = unirest.get("https://api-nba-v1.p.rapidapi.com/seasons/",
  headers={
    "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "eedd51b020mshc462a1043ca26dep113106jsn43a6a1a8e712"
  }
)
