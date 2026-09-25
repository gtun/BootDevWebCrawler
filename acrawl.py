import aiohttp
import asyncio
import requests
import crawl
from urllib.parse import urlsplit

class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int = 3, max_pages: int = 10):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.visited = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop: bool = False
        self.all_tasks = set()
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={"User-Agent": "BootCrawler/1.0"})
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        
    async def add_page_visit(self, normalized_url) -> bool:
        if self.should_stop:
            return False
        if len(self.visited) >= self.max_pages:
            self.should_stop = True
            print("Reached maximum number of pages to crawl.")
            
            return False
        async with self.lock:
            if normalized_url in self.visited:
                return False
            print(f"Crawling {normalized_url}")
            self.visited.add(normalized_url)
            return True
        
    async def get_html(self, url: str):
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
            if response.status >= 400:
                raise Exception(f"http error: {response.status}")
            if "text/html" not in response.headers.get("Content-Type",""):
                raise Exception("content type is not text/html")
            return await response.text()

    async def crawl_page(self, current_url: str):
        if self.should_stop:
            return    
        if urlsplit(current_url).netloc != self.base_domain:
            return
        normalized_url = crawl.normalize_url(current_url)
        
        if not await self.add_page_visit(normalized_url):
            return
        
        if normalized_url in self.page_data:
            return
        
        async with self.semaphore:
            current_url_html = await self.get_html(current_url)
            if current_url_html is None:
                return
                
            data = crawl.extract_page_data(current_url_html, current_url)
            async with self.lock:
                self.page_data[normalized_url] = data
            
            current_url_links: List = crawl.get_urls_from_html(current_url_html, current_url)
            
        tasks = [
            asyncio.create_task(self.crawl_page(link))
            for link in current_url_links
        ]
        await asyncio.gather(*tasks)
        
        tasks = []
        for link in current_url_links:
            task = asyncio.create_task(self.crawl_page(link))
            tasks.append(task)
            self.all_tasks.add(task)
        try:
            await asyncio.gather(*tasks)
        finally:
            for task in tasks:
                self.all_tasks.discard(task)
    
    async def crawl(self) -> dict:
        await self.crawl_page(self.base_url)
        return self.page_data
    
async def crawl_site_async(base_url: str, max_concurrency: int = 3, max_pages: int = 10) -> dict:
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()