import http.client

conn = http.client.HTTPSConnection("free-nba.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "free-nba.p.rapidapi.com",
    'x-rapidapi-key': "eedd51b020mshc462a1043ca26dep113106jsn43a6a1a8e712"
    }

# conn.request("GET", "/games/%7Bid%7D", headers=headers)
# conn.request("GET", "/games?page=0&per_page=1", headers=headers)
conn.request("GET", "/games?seasons[]=2019&dates[]=2019-11-27", headers=headers)

res = conn.getresponse()
data = res.read()

# print(data.decode("utf-8"))
print(data)

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

# response = unirest.get("https://api-nba-v1.p.rapidapi.com/seasons/",
#   headers={
#     "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
#     "X-RapidAPI-Key": "eedd51b020mshc462a1043ca26dep113106jsn43a6a1a8e712"
#   }
# )
