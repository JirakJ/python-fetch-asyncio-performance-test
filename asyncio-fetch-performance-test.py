import asyncio
import time 
import aiohttp
from aiohttp.client import ClientSession

async def download_link(url:str,session:ClientSession):
    async with session.get(url) as response:
        result = await response.text()
        print(f'Read {len(result)} from {url}')

async def download_all(urls:list):
    my_conn = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=my_conn) as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(download_link(url=url,session=session))
            tasks.append(task)
        await asyncio.gather(*tasks,return_exceptions=True) # the await must be nest inside of the session

url_list = ["https://www.google.com"]*100

start = time.time()
loop = asyncio.get_event_loop()
task = loop.create_task(download_all(url_list))

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass

end = time.time()
print(f'download {len(url_list)} links in {end - start} seconds')
