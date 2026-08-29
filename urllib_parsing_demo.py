import urllib.parse

def demonstrate_url_parsing():
    """Demonstrate parsing, inspecting, and building URLs."""
    
    print("--- 1. Parsing a URL ---")
    url = "https://www.example.com:8080/path/to/page?name=ferret&color=purple#section2"
    parsed_url = urllib.parse.urlparse(url)
    
    print(f"Original URL: {url}\n")
    print(f"Scheme: {parsed_url.scheme}")
    print(f"Netloc (Domain+Port): {parsed_url.netloc}")
    print(f"Path: {parsed_url.path}")
    print(f"Query parameters string: {parsed_url.query}")
    print(f"Fragment: {parsed_url.fragment}")
    
    print("\n--- 2. Parsing Query Parameters ---")
    # Parse the query string into a dictionary
    query_params = urllib.parse.parse_qs(parsed_url.query)
    print(f"Parsed parameters: {query_params}")
    print(f"Color: {query_params['color'][0]}")
    
    print("\n--- 3. Building a URL ---")
    # Build a query string from a dictionary
    new_params = {'search': 'python tutorials', 'page': 2}
    encoded_query = urllib.parse.urlencode(new_params)
    
    # Construct a new URL
    base_url = "https://api.mywebsite.com/v1/data"
    full_url = f"{base_url}?{encoded_query}"
    
    print(f"Constructed URL: {full_url}")

if __name__ == "__main__":
    demonstrate_url_parsing()
