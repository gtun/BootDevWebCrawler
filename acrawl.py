import aiohttp
import asyncio
import requests

class AsyncCrawler():
    def __init__():
        self.base_url = ""
        self.base_domain = ""
        self.page_data = {}
        self.visited = []
        self.lock = asyncio.Lock()
        self.max_concurrency = 100
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = aiohttp.ClientSession()
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        
    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.visited:
                return False
            self.visited.append(normalized_url)
            return True
        
    async def get_html(url: str):
        async with self.session:
            try:
                response = requests.get(url, headers={
                **header_user_agent
                })
                if response.status_code >= 400:
                    raise Exception(f"http error: {response.status_code}")
                if "text/html" not in response.headers["Content-Type"]:
                    raise Exception("content type is not text/html")
                return response.text
            except Exception as e:
                print(f".get() error: {type(e).__name__}")

    async def crawl_page(self, base_url, current_url=None, page_data=None):    
        if urlsplit(current_url).netloc != base_url:
            return
        normalized_url = crawl.normalize_url(current_url)
        
        if not await add_page_visit(normalized_url):
            return
        
        if normalized_url in self.page_data:
            return
        
        async with self.semaphore:
            current_url_html = get_html(current_url)
                
            self.page_data[normalized_url] = crawl.extract_page_data(current_url_html, current_url)
            
            current_url_links: List = crawl.get_urls_from_html(current_url_html, current_url)
            
            for url_link in current_url_links:
                tasks = asyncio.create_task(crawl_page(base_url, url_link, self.page_data))
            await asyncio.gather(*tasks)    
            
        return
    
    async def crawl(self, base_url) -> dict:
        crawl_page(base_url)
        return self.page_data
    
    async def crawl_site_async(self, url):
        async with AsyncCrawler:
            await crawl(base_url)
            return self.page_data