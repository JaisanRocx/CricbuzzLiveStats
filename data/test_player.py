import requests
import json

player_id = 1114

url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"

headers = {
    "x-rapidapi-key": "YOUR_API_KEY",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print(json.dumps(response.json(), indent=2))