"""
URL Shortener - URL shortening service with analytics.
Features: Short code generation, redirect tracking, and analytics.
"""

import random
import string
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RedirectStatus(Enum):
    """Redirect status."""
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    EXPIRED = "expired"


@dataclass
class URLRecord:
    """URL record."""
    original_url: str
    short_code: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    click_count: int = 0
    last_clicked: Optional[datetime] = None
    custom_alias: Optional[str] = None
    
    def is_expired(self) -> bool:
        """Check if URL has expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "original_url": self.original_url,
            "short_code": self.short_code,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "click_count": self.click_count,
            "last_clicked": self.last_clicked.isoformat() if self.last_clicked else None,
            "custom_alias": self.custom_alias
        }


@dataclass
class ClickEvent:
    """Click event for analytics."""
    short_code: str
    timestamp: datetime = field(default_factory=datetime.now)
    user_agent: Optional[str] = None
    referrer: Optional[str] = None
    ip_address: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "short_code": self.short_code,
            "timestamp": self.timestamp.isoformat(),
            "user_agent": self.user_agent,
            "referrer": self.referrer,
            "ip_address": self.ip_address
        }


class URLShortener:
    """URL shortening service."""
    
    def __init__(self, base_url: str = "http://short.est/") -> None:
        """
        Initialize URL shortener.
        
        Args:
            base_url: Base URL for shortened links
        """
        self.base_url = base_url
        self.urls: Dict[str, URLRecord] = {}
        self.custom_aliases: Dict[str, str] = {}  # alias -> short_code
        self.click_events: List[ClickEvent] = []
        self.code_length = 6
    
    def _generate_code(self) -> str:
        """Generate random short code."""
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(chars, k=self.code_length))
            if code not in self.urls:
                return code
    
    def shorten(self, url: str, custom_alias: Optional[str] = None,
                expires_in_days: Optional[int] = None) -> str:
        """
        Shorten a URL.
        
        Args:
            url: Original URL
            custom_alias: Optional custom alias
            expires_in_days: Optional expiration in days
            
        Returns:
            Shortened URL
        """
        # Validate custom alias
        if custom_alias:
            if custom_alias in self.custom_aliases:
                raise ValueError("Custom alias already exists")
            if not custom_alias.isalnum():
                raise ValueError("Custom alias must be alphanumeric")
        
        # Generate code
        short_code = custom_alias if custom_alias else self._generate_code()
        
        # Calculate expiration
        expires_at = None
        if expires_in_days:
            from datetime import timedelta
            expires_at = datetime.now() + timedelta(days=expires_in_days)
        
        # Create record
        record = URLRecord(
            original_url=url,
            short_code=short_code,
            expires_at=expires_at,
            custom_alias=custom_alias
        )
        
        self.urls[short_code] = record
        
        if custom_alias:
            self.custom_aliases[custom_alias] = short_code
        
        return f"{self.base_url}{short_code}"
    
    def resolve(self, short_code: str, user_agent: Optional[str] = None,
               referrer: Optional[str] = None, ip_address: Optional[str] = None) -> tuple:
        """
        Resolve shortened URL.
        
        Args:
            short_code: Short code
            user_agent: Optional user agent
            referrer: Optional referrer
            ip_address: Optional IP address
            
        Returns:
            Tuple of (status, original_url)
        """
        # Check custom alias
        if short_code in self.custom_aliases:
            short_code = self.custom_aliases[short_code]
        
        # Find record
        record = self.urls.get(short_code)
        
        if not record:
            return (RedirectStatus.NOT_FOUND, None)
        
        # Check expiration
        if record.is_expired():
            return (RedirectStatus.EXPIRED, None)
        
        # Update record
        record.click_count += 1
        record.last_clicked = datetime.now()
        
        # Log click event
        click_event = ClickEvent(
            short_code=short_code,
            user_agent=user_agent,
            referrer=referrer,
            ip_address=ip_address
        )
        self.click_events.append(click_event)
        
        return (RedirectStatus.SUCCESS, record.original_url)
    
    def get_url_info(self, short_code: str) -> Optional[Dict]:
        """
        Get information about a shortened URL.
        
        Args:
            short_code: Short code
            
        Returns:
            URL information or None
        """
        # Check custom alias
        if short_code in self.custom_aliases:
            short_code = self.custom_aliases[short_code]
        
        record = self.urls.get(short_code)
        if record:
            return record.to_dict()
        return None
    
    def delete_url(self, short_code: str) -> bool:
        """
        Delete a shortened URL.
        
        Args:
            short_code: Short code
            
        Returns:
            True if deleted
        """
        # Check custom alias
        if short_code in self.custom_aliases:
            short_code = self.custom_aliases[short_code]
        
        if short_code in self.urls:
            record = self.urls[short_code]
            if record.custom_alias:
                del self.custom_aliases[record.custom_alias]
            del self.urls[short_code]
            return True
        return False
    
    def get_analytics(self, short_code: str) -> Dict:
        """
        Get analytics for a shortened URL.
        
        Args:
            short_code: Short code
            
        Returns:
            Analytics data
        """
        # Check custom alias
        if short_code in self.custom_aliases:
            short_code = self.custom_aliases[short_code]
        
        record = self.urls.get(short_code)
        if not record:
            return {}
        
        # Get click events for this URL
        clicks = [event for event in self.click_events if event.short_code == short_code]
        
        # Calculate analytics
        total_clicks = len(clicks)
        unique_ips = len(set(event.ip_address for event in clicks if event.ip_address))
        
        # Clicks by day
        clicks_by_day = {}
        for event in clicks:
            day = event.timestamp.date().isoformat()
            clicks_by_day[day] = clicks_by_day.get(day, 0) + 1
        
        return {
            "short_code": short_code,
            "original_url": record.original_url,
            "total_clicks": total_clicks,
            "unique_visitors": unique_ips,
            "created_at": record.created_at.isoformat(),
            "last_clicked": record.last_clicked.isoformat() if record.last_clicked else None,
            "expires_at": record.expires_at.isoformat() if record.expires_at else None,
            "clicks_by_day": clicks_by_day
        }
    
    def get_all_urls(self) -> List[Dict]:
        """Get all shortened URLs."""
        return [record.to_dict() for record in self.urls.values()]
    
    def get_statistics(self) -> Dict:
        """Get overall statistics."""
        total_urls = len(self.urls)
        total_clicks = sum(record.click_count for record in self.urls.values())
        
        active_urls = len([r for r in self.urls.values() if not r.is_expired()])
        expired_urls = len([r for r in self.urls.values() if r.is_expired()])
        
        return {
            "total_urls": total_urls,
            "total_clicks": total_clicks,
            "active_urls": active_urls,
            "expired_urls": expired_urls,
            "custom_aliases": len(self.custom_aliases)
        }
    
    def cleanup_expired(self) -> int:
        """Remove expired URLs."""
        expired_codes = [code for code, record in self.urls.items() if record.is_expired()]
        
        for code in expired_codes:
            record = self.urls[code]
            if record.custom_alias:
                del self.custom_aliases[record.custom_alias]
            del self.urls[code]
        
        return len(expired_codes)


def main() -> None:
    """Demonstrate URL shortener."""
    
    print("=== URL Shortener Demo ===")
    
    shortener = URLShortener("http://short.est/")
    
    # Shorten URLs
    url1 = "https://www.example.com/very/long/url/that/needs/to/be/shortened"
    short1 = shortener.shorten(url1)
    print(f"Original: {url1}")
    print(f"Shortened: {short1}")
    
    url2 = "https://www.google.com/search?q=python+programming"
    short2 = shortener.shorten(url2, custom_alias="google")
    print(f"\nOriginal: {url2}")
    print(f"Shortened: {short2}")
    
    url3 = "https://github.com/smithkadam2654/ops"
    short3 = shortener.shorten(url3, expires_in_days=30)
    print(f"\nOriginal: {url3}")
    print(f"Shortened: {short3}")
    
    # Resolve URLs
    print("\n--- Resolving URLs ---")
    status, original = shortener.resolve("google")
    print(f"Resolve 'google': {status.value} -> {original}")
    
    status, original = shortener.resolve(short1.split("/")[-1])
    print(f"Resolve '{short1.split('/')[-1]}': {status.value} -> {original}")
    
    status, original = shortener.resolve("nonexistent")
    print(f"Resolve 'nonexistent': {status.value}")
    
    # Simulate clicks
    print("\n--- Simulating clicks ---")
    for i in range(5):
        shortener.resolve(short1.split("/")[-1], 
                        user_agent="Mozilla/5.0",
                        ip_address=f"192.168.1.{i}")
    
    for i in range(3):
        shortener.resolve("google",
                        user_agent="Chrome/90.0",
                        ip_address=f"10.0.0.{i}")
    
    # Get URL info
    print("\n--- URL Info ---")
    info = shortener.get_url_info("google")
    print(f"Info for 'google': {info}")
    
    # Get analytics
    print("\n--- Analytics ---")
    analytics = shortener.get_analytics("google")
    print(f"Analytics for 'google':")
    print(f"  Total clicks: {analytics['total_clicks']}")
    print(f"  Unique visitors: {analytics['unique_visitors']}")
    print(f"  Clicks by day: {analytics['clicks_by_day']}")
    
    # Get all URLs
    print("\n--- All URLs ---")
    all_urls = shortener.get_all_urls()
    for url_info in all_urls:
        print(f"  {url_info['short_code']}: {url_info['original_url'][:50]}...")
    
    # Statistics
    print("\n--- Statistics ---")
    stats = shortener.get_statistics()
    print(f"Total URLs: {stats['total_urls']}")
    print(f"Total clicks: {stats['total_clicks']}")
    print(f"Active URLs: {stats['active_urls']}")
    print(f"Expired URLs: {stats['expired_urls']}")
    print(f"Custom aliases: {stats['custom_aliases']}")
    
    # Delete URL
    print("\n--- Delete URL ---")
    deleted = shortener.delete_url("google")
    print(f"Deleted 'google': {deleted}")
    
    # Cleanup expired
    print("\n--- Cleanup ---")
    cleaned = shortener.cleanup_expired()
    print(f"Cleaned {cleaned} expired URLs")


if __name__ == "__main__":
    main()
