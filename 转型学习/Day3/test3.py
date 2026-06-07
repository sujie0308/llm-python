import asyncio
from unittest import result


async def fetch_data():
 return "data"
 core  = fetch_data()
async def main():
    result = await fetch_data()
    print(result)
asyncio.run(main())

async def fetch(id:int):
    await asyncio.sleep(1)
    return f"data_{id}"

async def main2():
    
    results = await asyncio.gather(fetch(1),fetch(2),fetch(3))
    print(results)
asyncio.run(main2())
