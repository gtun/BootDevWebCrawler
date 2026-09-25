import asyncio
from urllib.parse import urlsplit

import aiohttp

import crawl

HEADERS = {"User-Agent": "BootCrawler/1.0"}


class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int = 5):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.visited = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None  # opened in __aenter__

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=HEADERS)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        async with self.lock:
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True

    async def get_html(self, url: str) -> str:
        # [#3] aiohttp, not requests. requests blocks the whole event loop
        #      while it waits, so nothing else can run -- that defeats async.
        # [#3] `async with self.session.get(url)` opens and closes ONE request.
        #      Your `async with self.session:` closed the entire session
        #      after the first page.
        async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            if response.status >= 400:  # [#3] aiohttp: .status (requests: .status_code)
                raise Exception(f"http error {response.status}")
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                raise Exception(f"not html ({content_type})")
            return await response.text()  # [#3] aiohttp: text() is async, so await it

    async def crawl_page(self, current_url: str):
        # 1. stay on the same site
        if urlsplit(current_url).netloc != self.base_domain:
            return

        # 2. claim this URL; if another task already did, stop
        normalized_url = crawl.normalize_url(current_url)
        if not await self.add_page_visit(normalized_url):
            return

        # 3. fetch + parse, holding one of the limited "request slots"
        async with self.semaphore:
            print(f"crawling {current_url}")
            html = await self.get_html(current_url)
            if html is None:
                return
            data = crawl.extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_url] = data

        # 4. crawl children concurrently -- OUTSIDE the semaphore block,
        #    so this task gives its slot back before waiting on children
        tasks = [
            asyncio.create_task(self.crawl_page(link))
            for link in data["outgoing_links"]
        ]
        await asyncio.gather(*tasks)

    async def crawl(self) -> dict:
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(base_url: str, max_concurrency: int = 5) -> dict:
    async with AsyncCrawler(base_url, max_concurrency) as crawler:
        return await crawler.crawl()
