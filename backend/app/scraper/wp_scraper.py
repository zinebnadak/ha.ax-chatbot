# Send an HTTP request -> Receive the HTML/JSON response -> Parse the DOM -> Select elements -> Store structured data as json in /data
# uv run playwright install chromium
# input?
# output?
# type/shape of output?

import asyncio
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.ha.ax",
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())