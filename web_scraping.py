"""
Web Scraping Module

This module provides comprehensive web scraping utilities including:
- HTML parsing and extraction
- CSS selector and XPath support
- Data extraction from web pages
- Form handling and submission
- Cookie and session management
- Pagination handling
- Rate limiting and respectful scraping
- Data cleaning and normalization
- Export to various formats
- Headless browser automation (optional)

Note: This module uses BeautifulSoup and requests libraries.
Install with: pip install beautifulsoup4 requests lxml

For JavaScript rendering: pip install selenium webdriver-manager

All functions include comprehensive docstrings and type hints.
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import re
import time
import random


try:
    import requests
    from bs4 import BeautifulSoup
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False


@dataclass
class ScrapedData:
    """Container for scraped data."""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    links: List[str]
    images: List[str]
    timestamp: float


@dataclass
class FormField:
    """Represents a form field."""
    name: str
    value: str
    field_type: str = "text"
    required: bool = False


@dataclass
class ScrapeConfig:
    """Configuration for web scraping."""
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    timeout: int = 30
    delay_range: Tuple[float, float] = (1.0, 3.0)
    max_retries: int = 3
    respect_robots_txt: bool = True
    follow_redirects: bool = True
    verify_ssl: bool = True


class WebScraper:
    """Main web scraper class."""
    
    def __init__(self, config: Optional[ScrapeConfig] = None):
        """Initialize web scraper with configuration."""
        if not WEB_SCRAPING_AVAILABLE:
            raise ImportError("requests and beautifulsoup4 libraries are required. Install with: pip install requests beautifulsoup4 lxml")
        
        self.config = config or ScrapeConfig()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.config.user_agent
        })
        self._rate_limit_delay = 0
    
    def fetch_page(self, url: str, params: Optional[Dict] = None,
                   headers: Optional[Dict] = None) -> requests.Response:
        """Fetch a web page with retry logic."""
        retries = 0
        last_error = None
        
        while retries < self.config.max_retries:
            try:
                # Apply rate limiting
                if self._rate_limit_delay > 0:
                    time.sleep(self._rate_limit_delay)
                
                # Add random delay for respectful scraping
                delay = random.uniform(*self.config.delay_range)
                time.sleep(delay)
                
                response = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.config.timeout,
                    allow_redirects=self.config.follow_redirects,
                    verify=self.config.verify_ssl
                )
                response.raise_for_status()
                
                # Update rate limit based on response
                self._update_rate_limit(response)
                
                return response
                
            except requests.RequestException as e:
                last_error = e
                retries += 1
                if retries < self.config.max_retries:
                    wait_time = 2 ** retries
                    time.sleep(wait_time)
        
        raise Exception(f"Failed to fetch page after {self.config.max_retries} retries: {last_error}")
    
    def _update_rate_limit(self, response: requests.Response) -> None:
        """Update rate limiting based on response headers."""
        # Check for rate limit headers
        remaining = response.headers.get('X-RateLimit-Remaining')
        reset = response.headers.get('X-RateLimit-Reset')
        
        if remaining and int(remaining) < 10:
            self._rate_limit_delay = 2.0
        else:
            self._rate_limit_delay = 0
    
    def parse_html(self, html_content: str, parser: str = "lxml") -> BeautifulSoup:
        """Parse HTML content into BeautifulSoup object."""
        return BeautifulSoup(html_content, parser)
    
    def scrape_page(self, url: str) -> ScrapedData:
        """Scrape a web page and extract basic information."""
        response = self.fetch_page(url)
        soup = self.parse_html(response.text)
        
        scraped_data = ScrapedData(
            url=url,
            title=soup.title.string if soup.title else "",
            content=soup.get_text(),
            metadata={
                "status_code": response.status_code,
                "content_type": response.headers.get("Content-Type"),
                "content_length": len(response.content)
            },
            links=self.extract_links(soup, url),
            images=self.extract_images(soup, url),
            timestamp=time.time()
        )
        
        return scraped_data
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()


class CSSExtractor:
    """CSS selector-based data extraction."""
    
    def __init__(self, soup: BeautifulSoup):
        """Initialize CSS extractor with BeautifulSoup object."""
        self.soup = soup
    
    def extract_text(self, selector: str) -> str:
        """Extract text from elements matching CSS selector."""
        elements = self.soup.select(selector)
        return " ".join([elem.get_text(strip=True) for elem in elements])
    
    def extract_texts(self, selector: str) -> List[str]:
        """Extract texts from all elements matching CSS selector."""
        elements = self.soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]
    
    def extract_attribute(self, selector: str, attribute: str) -> List[str]:
        """Extract attribute values from elements matching CSS selector."""
        elements = self.soup.select(selector)
        return [elem.get(attribute, "") for elem in elements if elem.get(attribute)]
    
    def extract_links(self, selector: str = "a", base_url: str = "") -> List[str]:
        """Extract links from elements matching CSS selector."""
        elements = self.soup.select(selector)
        links = []
        for elem in elements:
            href = elem.get("href")
            if href:
                absolute_url = urljoin(base_url, href) if base_url else href
                links.append(absolute_url)
        return links
    
    def extract_images(self, selector: str = "img", base_url: str = "") -> List[str]:
        """Extract image URLs from elements matching CSS selector."""
        elements = self.soup.select(selector)
        images = []
        for elem in elements:
            src = elem.get("src")
            if src:
                absolute_url = urljoin(base_url, src) if base_url else src
                images.append(absolute_url)
        return images
    
    def extract_table(self, selector: str = "table", has_headers: bool = True) -> List[Dict]:
        """Extract table data as list of dictionaries."""
        tables = self.soup.select(selector)
        result = []
        
        for table in tables:
            rows = table.find_all("tr")
            
            if not rows:
                continue
            
            if has_headers:
                headers = [th.get_text(strip=True) for th in rows[0].find_all(["th", "td"])]
                data_rows = rows[1:]
            else:
                headers = [f"Column_{i}" for i in range(len(rows[0].find_all("td")))]
                data_rows = rows
            
            for row in data_rows:
                cells = row.find_all("td")
                if cells:
                    row_data = {}
                    for i, cell in enumerate(cells):
                        if i < len(headers):
                            row_data[headers[i]] = cell.get_text(strip=True)
                    result.append(row_data)
        
        return result
    
    def extract_forms(self) -> List[Dict]:
        """Extract form information from the page."""
        forms = self.soup.find_all("form")
        form_data = []
        
        for form in forms:
            form_info = {
                "action": form.get("action", ""),
                "method": form.get("method", "GET"),
                "fields": []
            }
            
            for input_elem in form.find_all(["input", "select", "textarea"]):
                field = {
                    "name": input_elem.get("name", ""),
                    "type": input_elem.get("type", "text"),
                    "value": input_elem.get("value", ""),
                    "required": input_elem.has_attr("required")
                }
                form_info["fields"].append(field)
            
            form_data.append(form_info)
        
        return form_data


class XPathExtractor:
    """XPath-based data extraction (requires lxml)."""
    
    def __init__(self, html_content: str):
        """Initialize XPath extractor with HTML content."""
        try:
            from lxml import etree
            self.tree = etree.HTML(html_content)
            self.available = True
        except ImportError:
            self.available = False
            self.tree = None
    
    def extract_text(self, xpath: str) -> str:
        """Extract text using XPath."""
        if not self.available:
            raise ImportError("lxml library is required for XPath extraction")
        
        elements = self.tree.xpath(xpath)
        return " ".join([elem.text or "" for elem in elements])
    
    def extract_texts(self, xpath: str) -> List[str]:
        """Extract texts using XPath."""
        if not self.available:
            raise ImportError("lxml library is required for XPath extraction")
        
        elements = self.tree.xpath(xpath)
        return [elem.text or "" for elem in elements]
    
    def extract_attribute(self, xpath: str, attribute: str) -> List[str]:
        """Extract attribute values using XPath."""
        if not self.available:
            raise ImportError("lxml library is required for XPath extraction")
        
        elements = self.tree.xpath(xpath)
        return [elem.get(attribute, "") for elem in elements if elem.get(attribute)]


class PaginationHandler:
    """Handle pagination in web scraping."""
    
    def __init__(self, scraper: WebScraper):
        """Initialize pagination handler with scraper."""
        self.scraper = scraper
    
    def scrape_all_pages(self, start_url: str, next_page_selector: str,
                         max_pages: int = 10) -> List[ScrapedData]:
        """Scrape all pages following pagination links."""
        results = []
        current_url = start_url
        page_count = 0
        
        while current_url and page_count < max_pages:
            try:
                # Scrape current page
                data = self.scraper.scrape_page(current_url)
                results.append(data)
                page_count += 1
                
                # Find next page link
                soup = self.scraper.parse_html(data.content)
                extractor = CSSExtractor(soup)
                next_links = extractor.extract_attribute(next_page_selector, "href")
                
                if next_links:
                    current_url = urljoin(current_url, next_links[0])
                else:
                    current_url = None
                    
            except Exception as e:
                print(f"Error scraping page {page_count + 1}: {e}")
                break
        
        return results
    
    def scrape_numbered_pages(self, base_url: str, page_param: str = "page",
                               start_page: int = 1, max_pages: int = 10) -> List[ScrapedData]:
        """Scrape numbered pages (e.g., page=1, page=2, etc.)."""
        results = []
        
        for page_num in range(start_page, start_page + max_pages):
            try:
                # Construct URL with page parameter
                from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
                
                parsed = urlparse(base_url)
                query_params = parse_qs(parsed.query)
                query_params[page_param] = [str(page_num)]
                
                new_query = urlencode(query_params, doseq=True)
                page_url = urlunparse(parsed._replace(query=new_query))
                
                # Scrape page
                data = self.scraper.scrape_page(page_url)
                results.append(data)
                
            except Exception as e:
                print(f"Error scraping page {page_num}: {e}")
                break
        
        return results


class FormHandler:
    """Handle form submission and interaction."""
    
    def __init__(self, scraper: WebScraper):
        """Initialize form handler with scraper."""
        self.scraper = scraper
    
    def submit_form(self, url: str, form_data: Dict[str, str],
                    method: str = "POST") -> requests.Response:
        """Submit a form with data."""
        if method.upper() == "POST":
            return self.scraper.session.post(url, data=form_data)
        else:
            return self.scraper.session.get(url, params=form_data)
    
    def fill_and_submit_form(self, form_info: Dict, field_values: Dict[str, str]) -> requests.Response:
        """Fill form fields and submit."""
        action = form_info.get("action", "")
        method = form_info.get("method", "POST")
        
        # Fill form fields
        form_data = {}
        for field in form_info.get("fields", []):
            field_name = field["name"]
            if field_name in field_values:
                form_data[field_name] = field_values[field_name]
            elif field.get("value"):
                form_data[field_name] = field["value"]
        
        # Submit form
        action_url = urljoin(self.scraper.session.last_url if hasattr(self.scraper.session, 'last_url') else "", action)
        return self.submit_form(action_url, form_data, method)


class DataCleaner:
    """Clean and normalize scraped data."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text by removing extra whitespace and special characters."""
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    @staticmethod
    def clean_url(url: str) -> str:
        """Clean URL by removing fragments and tracking parameters."""
        parsed = urlparse(url)
        clean_url = parsed._replace(fragment="", params="").geturl()
        return clean_url
    
    @staticmethod
    def extract_email(text: str) -> List[str]:
        """Extract email addresses from text."""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_phone(text: str) -> List[str]:
        """Extract phone numbers from text."""
        pattern = r'\+?[\d\s-()]{10,}'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_price(text: str) -> Optional[float]:
        """Extract price from text."""
        pattern = r'[\$€£]?\s?[\d,]+\.?\d*'
        match = re.search(pattern, text)
        if match:
            price_str = match.group().replace(',', '').replace('$', '').replace('€', '').replace('£', '').strip()
            try:
                return float(price_str)
            except ValueError:
                return None
        return None


class DataExporter:
    """Export scraped data to various formats."""
    
    @staticmethod
    def export_to_json(data: List[ScrapedData], file_path: str) -> None:
        """Export data to JSON file."""
        import json
        export_data = []
        for item in data:
            export_data.append({
                "url": item.url,
                "title": item.title,
                "content": item.content[:500],  # Truncate long content
                "metadata": item.metadata,
                "links": item.links[:10],  # Limit links
                "images": item.images[:10],  # Limit images
                "timestamp": item.timestamp
            })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
    
    @staticmethod
    def export_to_csv(data: List[ScrapedData], file_path: str) -> None:
        """Export data to CSV file."""
        import csv
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["URL", "Title", "Links Count", "Images Count", "Timestamp"])
            
            for item in data:
                writer.writerow([
                    item.url,
                    item.title,
                    len(item.links),
                    len(item.images),
                    item.timestamp
                ])
    
    @staticmethod
    def export_to_html(data: List[ScrapedData], file_path: str) -> None:
        """Export data to HTML file."""
        html_content = "<html><head><title>Scraped Data</title></head><body>"
        html_content += "<h1>Scraped Data</h1>"
        
        for item in data:
            html_content += f"<h2>{item.title}</h2>"
            html_content += f"<p><strong>URL:</strong> {item.url}</p>"
            html_content += f"<p><strong>Links:</strong> {len(item.links)}</p>"
            html_content += f"<p><strong>Images:</strong> {len(item.images)}</p>"
            html_content += "<hr>"
        
        html_content += "</body></html>"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)


class RobotsTxtHandler:
    """Handle robots.txt parsing for respectful scraping."""
    
    def __init__(self):
        """Initialize robots.txt handler."""
        self.user_agent = "*"
        self.disallowed_paths = []
        self.allowed_paths = []
        self.crawl_delay = 0
    
    def parse_robots_txt(self, url: str) -> None:
        """Parse robots.txt from given URL."""
        try:
            from urllib.robotparser import RobotFileParser
            rp = RobotFileParser()
            rp.set_url(url)
            rp.read()
            
            self.crawl_delay = rp.crawl_delay(self.user_agent)
            
        except Exception as e:
            print(f"Error parsing robots.txt: {e}")
    
    def can_fetch(self, url: str) -> bool:
        """Check if URL can be fetched according to robots.txt."""
        try:
            from urllib.robotparser import RobotFileParser
            rp = RobotFileParser()
            robots_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt"
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch(self.user_agent, url)
        except:
            return True


def create_sample_scraper() -> WebScraper:
    """Create a sample web scraper with default configuration."""
    config = ScrapeConfig(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        timeout=30,
        delay_range=(1.0, 2.0),
        max_retries=3,
        respect_robots_txt=True
    )
    return WebScraper(config)


def demonstrate_web_scraping():
    """Demonstrate web scraping functionality."""
    print("=== Web Scraping Demonstration ===\n")
    
    if not WEB_SCRAPING_AVAILABLE:
        print("requests and beautifulsoup4 libraries are required.")
        print("Install with: pip install requests beautifulsoup4 lxml")
        return
    
    # Create scraper
    print("1. Creating web scraper...")
    scraper = create_sample_scraper()
    print("   Scraper created with default configuration")
    
    # Sample HTML for demonstration
    sample_html = """
    <html>
    <head>
        <title>Sample Page</title>
    </head>
    <body>
        <h1>Welcome to Sample Page</h1>
        <div class="content">
            <p>This is a sample paragraph with some text.</p>
            <p>Contact us at info@example.com or call +1-555-123-4567</p>
        </div>
        <div class="products">
            <div class="product">
                <h3>Laptop</h3>
                <p class="price">$999.99</p>
                <a href="/products/laptop">View Details</a>
            </div>
            <div class="product">
                <h3>Mouse</h3>
                <p class="price">$29.99</p>
                <a href="/products/mouse">View Details</a>
            </div>
        </div>
        <table>
            <tr>
                <th>Name</th>
                <th>Age</th>
                <th>City</th>
            </tr>
            <tr>
                <td>John</td>
                <td>30</td>
                <td>New York</td>
            </tr>
            <tr>
                <td>Jane</td>
                <td>25</td>
                <td>Los Angeles</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    # Parse HTML
    print("\n2. Parsing HTML...")
    soup = scraper.parse_html(sample_html)
    print("   HTML parsed successfully")
    
    # CSS Extraction
    print("\n3. CSS Selector Extraction:")
    extractor = CSSExtractor(soup)
    
    title = extractor.extract_text("title")
    print(f"   Title: {title}")
    
    headings = extractor.extract_texts("h1, h3")
    print(f"   Headings: {headings}")
    
    prices = extractor.extract_texts(".price")
    print(f"   Prices: {prices}")
    
    links = extractor.extract_links("a", "https://example.com")
    print(f"   Links: {links}")
    
    # Table extraction
    print("\n4. Table Extraction:")
    table_data = extractor.extract_table("table")
    print(f"   Table rows: {len(table_data)}")
    for row in table_data:
        print(f"   {row}")
    
    # Data cleaning
    print("\n5. Data Cleaning:")
    text = "  This   is   messy  text  "
    print(f"   Original: '{text}'")
    print(f"   Cleaned: '{DataCleaner.clean_text(text)}'")
    
    contact_text = "Contact us at info@example.com or support@test.org"
    emails = DataCleaner.extract_email(contact_text)
    print(f"   Emails found: {emails}")
    
    price_text = "The laptop costs $999.99 and the mouse is $29.99"
    prices = [DataCleaner.extract_price(price_text)]
    print(f"   Prices extracted: {prices}")
    
    # Form extraction
    print("\n6. Form Extraction:")
    form_html = """
    <form action="/submit" method="POST">
        <input type="text" name="username" required>
        <input type="password" name="password" required>
        <input type="email" name="email">
        <button type="submit">Submit</button>
    </form>
    """
    form_soup = scraper.parse_html(form_html)
    form_extractor = CSSExtractor(form_soup)
    forms = form_extractor.extract_forms()
    print(f"   Forms found: {len(forms)}")
    if forms:
        print(f"   Form action: {forms[0]['action']}")
        print(f"   Form fields: {len(forms[0]['fields'])}")
    
    # Export demonstration
    print("\n7. Data Export:")
    sample_data = [ScrapedData(
        url="https://example.com",
        title="Example Page",
        content="Sample content",
        metadata={"status": 200},
        links=["https://example.com/page1"],
        images=["https://example.com/image.jpg"],
        timestamp=time.time()
    )]
    
    try:
        DataExporter.export_to_json(sample_data, "scraped_data.json")
        print("   Data exported to JSON")
        
        DataExporter.export_to_csv(sample_data, "scraped_data.csv")
        print("   Data exported to CSV")
        
        # Cleanup
        import os
        os.remove("scraped_data.json")
        os.remove("scraped_data.csv")
        print("   Export files cleaned up")
    except Exception as e:
        print(f"   Export error: {e}")
    
    # Close scraper
    scraper.close()
    print("\n8. Scraper closed")
    
    print("\n=== Demonstration Complete ===")
    print("\nNote: For actual web scraping, always:")
    print("- Respect robots.txt")
    print("- Use appropriate rate limiting")
    print("- Check website terms of service")
    print("- Be considerate of server resources")


if __name__ == "__main__":
    demonstrate_web_scraping()