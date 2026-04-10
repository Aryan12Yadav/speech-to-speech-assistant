import requests

res = requests.post(
     "https://lucknow-land-price-5.onrender.com/chat",
     json={
         "user_id":"user23421",
         "query":"alambagh property price"
     }
)
print(res.json())