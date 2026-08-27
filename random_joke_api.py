import urllib.request
import json

def get_random_joke():
    """Fetch a random setup and punchline joke from an API."""
    url = "https://official-joke-api.appspot.com/random_joke"
    
    try:
        # Send a GET request to the URL
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print("Here's a joke for you:")
                print(f"- {data['setup']}")
                print(f"  {data['punchline']}")
            else:
                print(f"Failed to retrieve joke. Status code: {response.status}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    get_random_joke()
