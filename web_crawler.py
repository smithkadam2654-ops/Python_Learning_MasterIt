"""
Web Crawler - Web scraping and crawling utilities.
Features: HTTP requests, HTML parsing, and data extraction.
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import re


@dataclass
class WebPage:
    """Represents a web page with its content."""
    url: str
    title: str = ""
    content: str = ""
    links: List[str] = None
    
    def __post_init__(self):
        if self.links is None:
            self.links = []


class HTMLParser:
    """Simple HTML parser for extracting data."""
    
    @staticmethod
    def extract_title(html: str) -> str:
        """Extract title from HTML."""
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else ""
    
    @staticmethod
    def extract_links(html: str, base_url: str = "") -> List[str]:
        """Extract all links from HTML."""
        links = []
        
        # Match href attributes
        for match in re.finditer(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE):
            link = match.group(1)
            
            # Skip javascript, mailto, and anchor links
            if link.startswith(('javascript:', 'mailto:', '#')):
                continue
            
            # Convert relative URLs to absolute
            if base_url and not link.startswith(('http://', 'https://')):
                link = urljoin(base_url, link)
            
            links.append(link)
        
        return links
    
    @staticmethod
    def extract_text(html: str) -> str:
        """Extract text content from HTML (remove tags)."""
        # Remove script and style tags
        html = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.IGNORECASE | re.DOTALL)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    @staticmethod
    def extract_meta_tags(html: str) -> Dict[str, str]:
        """Extract meta tags from HTML."""
        meta_tags = {}
        
        for match in re.finditer(r'<meta\s+(.*?)>', html, re.IGNORECASE):
            meta_content = match.group(1)
            
            # Extract name and content
            name_match = re.search(r'name=["\']([^"\']+)["\']', meta_content, re.IGNORECASE)
            content_match = re.search(r'content=["\']([^"\']*)["\']', meta_content, re.IGNORECASE)
            
            if name_match and content_match:
                meta_tags[name_match.group(1)] = content_match.group(1)
        
        return meta_tags
    
    @staticmethod
    def extract_images(html: str, base_url: str = "") -> List[str]:
        """Extract all image URLs from HTML."""
        images = []
        
        for match in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE):
            img_url = match.group(1)
            
            if base_url and not img_url.startswith(('http://', 'https://')):
                img_url = urljoin(base_url, img_url)
            
            images.append(img_url)
        
        return images


class WebCrawler:
    """Simple web crawler for exploring websites."""
    
    def __init__(self, max_pages: int = 100, same_domain: bool = True) -> None:
        """
        Initialize web crawler.
        
        Args:
            max_pages: Maximum number of pages to crawl
            same_domain: Whether to only crawl pages from the same domain
        """
        self.max_pages = max_pages
        self.same_domain = same_domain
        self.visited: Set[str] = set()
        self.to_visit: List[str] = []
        self.pages: List[WebPage] = []
    
    def is_same_domain(self, url1: str, url2: str) -> bool:
        """Check if two URLs are from the same domain."""
        parsed1 = urlparse(url1)
        parsed2 = urlparse(url2)
        return parsed1.netloc == parsed2.netloc
    
    def normalize_url(self, url: str) -> str:
        """Normalize URL by removing fragment and trailing slash."""
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        return normalized
    
    def should_visit(self, url: str, base_url: str) -> bool:
        """Determine if URL should be visited."""
        normalized = self.normalize_url(url)
        
        # Skip if already visited
        if normalized in self.visited:
            return False
        
        # Skip if not HTTP/HTTPS
        if not url.startswith(('http://', 'https://')):
            return False
        
        # Skip if same domain constraint and different domain
        if self.same_domain and not self.is_same_domain(url, base_url):
            return False
        
        return True
    
    def crawl(self, start_url: str, fetch_func: callable) -> List[WebPage]:
        """
        Crawl website starting from given URL.
        
        Args:
            start_url: URL to start crawling from
            fetch_func: Function to fetch page content (url) -> str
            
        Returns:
            List of crawled pages
        """
        self.to_visit = [start_url]
        base_domain = urlparse(start_url).netloc
        
        while self.to_visit and len(self.pages) < self.max_pages:
            url = self.to_visit.pop(0)
            normalized = self.normalize_url(url)
            
            if normalized in self.visited:
                continue
            
            try:
                html = fetch_func(url)
                self.visited.add(normalized)
                
                # Parse page
                parser = HTMLParser()
                page = WebPage(
                    url=url,
                    title=parser.extract_title(html),
                    content=parser.extract_text(html),
                    links=parser.extract_links(html, url)
                )
                
                self.pages.append(page)
                
                # Add new links to visit
                for link in page.links:
                    if self.should_visit(link, start_url):
                        self.to_visit.append(link)
                
            except Exception as e:
                print(f"Error crawling {url}: {e}")
                self.visited.add(normalized)
        
        return self.pages
    
    def get_page_count(self) -> int:
        """Get number of crawled pages."""
        return len(self.pages)
    
    def get_all_links(self) -> Set[str]:
        """Get all unique links found during crawling."""
        links = set()
        for page in self.pages:
            links.update(page.links)
        return links


class DataExtractor:
    """Extract structured data from web pages."""
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Extract email addresses from text."""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """Extract phone numbers from text."""
        pattern = r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_prices(text: str) -> List[str]:
        """Extract prices from text."""
        pattern = r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """Extract dates in various formats."""
        patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',
            r'\d{4}-\d{2}-\d{2}',
            r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',
        ]
        dates = []
        for pattern in patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
        return dates
    
    @staticmethod
    def extract_social_links(html: str) -> Dict[str, List[str]]:
        """Extract social media links."""
        social_patterns = {
            'twitter': r'twitter\.com/\w+',
            'facebook': r'facebook\.com/\w+',
            'linkedin': r'linkedin\.com/\w+',
            'instagram': r'instagram\.com/\w+',
            'youtube': r'youtube\.com/\w+',
        }
        
        social_links = {}
        for platform, pattern in social_patterns.items():
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                social_links[platform] = matches
        
        return social_links


def mock_fetch(url: str) -> str:
    """Mock function to simulate fetching web pages."""
    # Simulate different pages based on URL
    if "home" in url:
        return """
        <html>
        <head><title>Home Page</title></head>
        <body>
        <h1>Welcome to Our Site</h1>
        <p>Contact us at info@example.com or call 555-123-4567</p>
        <a href="/about">About Us</a>
        <a href="/products">Products</a>
        <a href="https://twitter.com/example">Twitter</a>
        </body>
        </html>
        """
    elif "about" in url:
        return """
        <html>
        <head><title>About Us</title></head>
        <body>
        <h1>About Our Company</h1>
        <p>Founded in 2020</p>
        <a href="/">Home</a>
        <a href="/contact">Contact</a>
        </body>
        </html>
        """
    elif "products" in url:
        return """
        <html>
        <head><title>Products</title></head>
        <body>
        <h1>Our Products</h1>
        <p>Starting at $99.99</p>
        <a href="/">Home</a>
        </body>
        </html>
        """
    else:
        return "<html><head><title>Page</title></head><body><p>Content</p></body></html>"


def main() -> None:
    """Demonstrate web scraping utilities."""
    
    print("=== HTML Parser ===")
    html = """
    <html>
    <head>
        <title>Test Page</title>
        <meta name="description" content="A test page">
    </head>
    <body>
        <h1>Welcome</h1>
        <p>Contact us at info@example.com</p>
        <a href="/about">About</a>
        <a href="https://example.com">External</a>
        <img src="/logo.png" alt="Logo">
    </body>
    </html>
    """
    
    parser = HTMLParser()
    print(f"Title: {parser.extract_title(html)}")
    print(f"Links: {parser.extract_links(html, 'https://example.com')}")
    print(f"Images: {parser.extract_images(html, 'https://example.com')}")
    print(f"Meta tags: {parser.extract_meta_tags(html)}")
    print(f"Text: {parser.extract_text(html)[:50]}...")
    
    print("\n=== Data Extraction ===")
    text = """
    Contact us at info@example.com or support@test.com.
    Call us at 555-123-4567 or (555) 987-6543.
    Prices start at $99.99 and go up to $1,299.99.
    Founded on 01/15/2020.
    """
    
    extractor = DataExtractor()
    print(f"Emails: {extractor.extract_emails(text)}")
    print(f"Phone numbers: {extractor.extract_phone_numbers(text)}")
    print(f"Prices: {extractor.extract_prices(text)}")
    print(f"Dates: {extractor.extract_dates(text)}")
    
    print("\n=== Web Crawler ===")
    crawler = WebCrawler(max_pages=5, same_domain=True)
    pages = crawler.crawl("https://example.com/home", mock_fetch)
    
    print(f"Crawled {len(pages)} pages:")
    for page in pages:
        print(f"  {page.url}: {page.title}")
    
    print(f"\nTotal links found: {len(crawler.get_all_links())}")
    print(f"Links: {list(crawler.get_all_links())}")


if __name__ == "__main__":
    main()
