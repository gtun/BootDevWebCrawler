import sys
import requests
import crawl
import asyncio
from urllib.parse import urlsplit
from acrawl import crawl_site_async



async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    initial_url: str = sys.argv[1]
    max_concurrency: int = int(sys.argv[2])
    max_pages: int = int(sys.argv[3])
    
    page_data = {}
    page_data = await crawl_site_async(initial_url, max_concurrency, max_pages)
    print(f"{len(page_data)} page scanned on {initial_url}:")
    for key in page_data:
        print(key)

"""
def get_html(url: str):
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

def crawl_page(base_url, current_url=None, page_data=None):
    if page_data is None:
        page_data = {}
    if urlsplit(current_url).netloc != base_url:
        return
    normalized_url = crawl.normalize_url(current_url)
    if normalized_url in page_data:
        return
    current_url_html = get_html(current_url)
        
    page_data[normalized_url] = crawl.extract_page_data(current_url_html, current_url)
    
    current_url_links: List = crawl.get_urls_from_html(current_url_html, current_url)
    
    for url_link in current_url_links:
        crawl_page(base_url, url_link, page_data)
    
    return

async def crawl_site_async(initial_url):
    async with acrawl.AsyncCrawler():
        return await crawl()

"""

if __name__ == "__main__":
    asyncio.run(main())