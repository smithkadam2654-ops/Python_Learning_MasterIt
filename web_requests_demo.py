import urllib.request
import urllib.parse
import json

def demonstrate_web_requests():
    """Demonstrate how to make HTTP GET and POST requests."""
    
    # 1. Basic GET request
    print("--- GET Request ---")
    get_url = "https://jsonplaceholder.typicode.com/posts/1"
    try:
        with urllib.request.urlopen(get_url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print(f"Post Title: {data['title']}")
    except Exception as e:
        print(f"GET request failed: {e}")
        
    # 2. POST request with data
    print("\n--- POST Request ---")
    post_url = "https://jsonplaceholder.typicode.com/posts"
    post_data = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    
    # Encode the data
    data_encoded = json.dumps(post_data).encode('utf-8')
    
    # Create the request object
    req = urllib.request.Request(post_url, data=data_encoded, method='POST')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 201: # 201 Created
                result = json.loads(response.read().decode())
                print(f"Successfully created post with ID: {result['id']}")
    except Exception as e:
        print(f"POST request failed: {e}")

if __name__ == "__main__":
    demonstrate_web_requests()
