# Importing libraries
import asyncio
import websockets
import datetime
import json
from random import random

# Defining PORT to listening to
PORT = 5678


def generate_movement():
    return -1 if random() < 0.5 else 1


async def set_tickers(websocket):
    print("A client is connected")
    tickers = {f'ticker_{i:02}': 0 for i in range(100)}

    while True:
        for k in tickers.keys():
            tickers[k] += generate_movement()

        date = datetime.datetime.utcnow().isoformat() + "Z"
        data = json.dumps({"date": date, "tickers": tickers})

        try:
            await websocket.send(data)
        except websockets.exceptions.ConnectionClosed as e:
            print("A client is disconnected")
            print(e)
            break
        await asyncio.sleep(1)


async def main():
    async with websockets.serve(set_tickers, "localhost", PORT):
        await asyncio.Future()


if __name__ == "__main__":
    print(f"Server listening on port {PORT}")
    asyncio.run(main())
