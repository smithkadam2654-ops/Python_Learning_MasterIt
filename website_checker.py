import urllib.request
import urllib.error

def check_websites(urls):
    print("--- Website Status Checker ---")
    for url in urls:
        # Ensure the URL starts with http:// or https://
        if not url.startswith("http"):
            url = "https://" + url
            
        try:
            # Try to connect to the website (timeout after 3 seconds)
            response = urllib.request.urlopen(url, timeout=3)
            if response.status == 200:
                print(f"[✅] ONLINE  : {url}")
        except urllib.error.URLError:
            print(f"[❌] OFFLINE : {url}")
        except Exception as e:
            print(f"[⚠️] ERROR   : {url} ({e})")

if __name__ == "__main__":
    sites_to_check = [
        "google.com",
        "github.com",
        "this-fake-website-will-fail.com",
        "python.org"
    ]
    check_websites(sites_to_check)
