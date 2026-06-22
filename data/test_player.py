import requests
import json

player_id = 1114

url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"

headers = {
    "x-rapidapi-key": "56189fe37fmsha58bef222a0c2f2p10741djsn96fd2d678427",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print(json.dumps(response.json(), indent=2))