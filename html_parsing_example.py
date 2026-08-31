from html.parser import HTMLParser
import urllib.request
import ssl

# Create a custom parser by inheriting from Python's built-in HTMLParser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        
    # This method is automatically called whenever an opening tag (like <a>, <p>, <div>) is found
    def handle_starttag(self, tag, attrs):
        # We only care about hyperlink tags (<a>)
        if tag == 'a':
            # Look through the attributes of the <a> tag
            for attr_name, attr_value in attrs:
                # If we find an 'href' attribute, save its value (the URL)
                if attr_name == 'href' and attr_value:
                    self.links.append(attr_value)

def scrape_links(url):
    print(f"Fetching HTML from: {url}")
    try:
        # Bypass SSL verification for local example purposes
        context = ssl._create_unverified_context()
        
        # Adding a User-Agent header because some websites block default Python requests
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, context=context) as response:
            # Decode the response into a string
            html_content = response.read().decode('utf-8')
            
        print("Parsing HTML for links...")
        # Initialize our custom parser
        parser = MyHTMLParser()
        
        # Feed the raw HTML string into the parser
        parser.feed(html_content)
        
        print(f"\nFound {len(parser.links)} links on the page! Here are the first 10:")
        
        # Print up to the first 10 links found
        for link in parser.links[:10]:
            print(f"- {link}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Let's scrape the official Python website as a safe example
    target_url = "https://www.python.org/"
    scrape_links(target_url)
