import requests

CLIENT_ID = "3539cf685adc4153b5d9b5fa48cbe582"
CLIENT_SECRET = "2f111c0b7f8c4eb393148ec5f543c610"

def dapatkan_token_oauth2():
    url = "https://oauth.fatsecret.com/connect/token"
    payload = {'grant_type': 'client_credentials', 'scope': 'premier'}
    response = requests.post(url, data=payload, auth=(CLIENT_ID, CLIENT_SECRET))
    if response.status_code == 200:
        return response.json().get('access_token')
    print("Error auth:", response.text)
    return None

def cari_indomilk():
    token = dapatkan_token_oauth2()
    if not token:
        return
    print("Token valid.")
    url = "https://platform.fatsecret.com/rest/server.api"
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        "method": "foods.search",
        "search_expression": "indomilk",
        "format": "json",
        "max_results": 20
    }
    response = requests.get(url, headers=headers, params=params)
    print("Status:", response.status_code)
    try:
        data = response.json()
        foods = data.get("foods", {}).get("food", [])
        print(f"Found: {len(foods)}")
        if foods:
            for f in foods[:3]:
                print(f.get('food_name'), f.get('brand_name'))
    except Exception as e:
        print("Error json:", e)
        print("Response text:", response.text)

if __name__ == "__main__":
    cari_indomilk()