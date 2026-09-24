import asyncio
import sys

from acrawl import crawl_site_async


async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")

    page_data = await crawl_site_async(base_url)

    print(f"{len(page_data)} pages crawled on {base_url}:")
    for page in page_data.values():
        print(f"- {page['url']}: {page['heading']}")


if __name__ == "__main__":
    asyncio.run(main())
