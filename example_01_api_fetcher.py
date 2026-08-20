import urllib.request
import json

def fetch_random_joke():
    """Fetches a random joke from the official joke API."""
    url = "https://official-joke-api.appspot.com/random_joke"
    
    try:
        # We use urllib to make a simple HTTP GET request
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                # Parse the JSON response into a Python dictionary
                data = json.loads(response.read().decode('utf-8'))
                print(f"Here is a joke for you:")
                print(f"- {data['setup']}")
                print(f"  {data['punchline']}")
            else:
                print(f"Failed to fetch a joke. Status code: {response.status}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_random_joke()
