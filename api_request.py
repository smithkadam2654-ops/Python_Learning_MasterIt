import urllib.request
import json
import ssl

def fetch_random_joke():
    # A free, public API that doesn't require authentication
    url = "https://official-joke-api.appspot.com/random_joke"
    
    try:
        print("Fetching a random joke from the internet...\n")
        
        # Bypass SSL verification for the sake of a simple local example
        # (In production code, you shouldn't bypass SSL verification)
        context = ssl._create_unverified_context()
        
        # Make the HTTP GET request
        with urllib.request.urlopen(url, context=context) as response:
            # Read and decode the response data from bytes to a string
            data = response.read().decode('utf-8')
            
            # Parse the JSON string into a Python dictionary
            joke_data = json.loads(data)
            
            # Print the joke
            print(f"Setup: {joke_data['setup']}")
            print(f"Punchline: {joke_data['punchline']}")
            
    except urllib.error.URLError as e:
        print(f"Failed to fetch data. Are you connected to the internet? Reason: {e.reason}")
    except json.JSONDecodeError:
        print("Failed to parse the JSON response.")

if __name__ == "__main__":
    fetch_random_joke()
