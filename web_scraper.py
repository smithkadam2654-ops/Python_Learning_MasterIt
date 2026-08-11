#!/usr/bin/env python3
"""
Web Scraper Framework
Provides a flexible framework for web scraping with error handling
"""

import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional
import logging

class WebScraper:
    def __init__(self, base_url: str, delay: float = 1.0):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.visited_urls = set()
        self.scraped_data = []
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL belongs to the same domain."""
        parsed_url = urlparse(url)
        return parsed_url.netloc == urlparse(self.base_url).netloc
    
    def _extract_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract all links from a page."""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(self.base_url, href)
            if self._is_valid_url(full_url) and full_url not in self.visited_urls:
                links.append(full_url)
        return links
    
    def _extract_data(self, soup: BeautifulSoup) -> Dict:
        """Extract data from the page. Override this method in subclasses."""
        return {
            'title': soup.title.string if soup.title else None,
            'text': soup.get_text().strip(),
            'links': [link['href'] for link in soup.find_all('a', href=True)]
        }
    
    def scrape_page(self, url: str) -> Optional[Dict]:
        """Scrape a single page."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            data = self._extract_data(soup)
            data['url'] = url
            data['scrape_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            return data
        except Exception as e:
            logging.error(f"Error scraping {url}: {e}")
            return None
    
    def scrape_site(self, max_pages: int = 10) -> List[Dict]:
        """Scrape the entire website."""
        to_visit = [self.base_url]
        self.visited_urls.add(self.base_url)
        scraped_count = 0
        
        while to_visit and scraped_count < max_pages:
            current_url = to_visit.pop(0)
            logging.info(f"Scraping: {current_url}")
            
            data = self.scrape_page(current_url)
            if data:
                self.scraped_data.append(data)
                scraped_count += 1
                
                # Extract new links
                new_links = self._extract_links(BeautifulSoup(data['text'], 'html.parser'))
                to_visit.extend(new_links)
                self.visited_urls.update(new_links)
            
            # Respect rate limiting
            time.sleep(self.delay)
        
        return self.scraped_data

if __name__ == "__main__":
    # Example usage
    import logging
    
    logging.basicConfig(level=logging.INFO)
    
    # Note: This is for demonstration purposes
    # In practice, you would use a real website
    scraper = WebScraper("https://example.com")
    
    print("Web scraper framework ready for use")
    print("You can subclass WebScraper and override _extract_data() for custom scraping logic")