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
    data = {f'ticker_{i:02}': 0 for i in range(100)}
    data.update({"date": datetime.datetime.utcnow().isoformat() + "Z"})

    while True:
        json_data = json.dumps(data)
        try:
            await websocket.send(json_data)
        except websockets.exceptions.ConnectionClosed as e:
            print("A client is disconnected")
            break

        await asyncio.sleep(1)

        for key in data.keys():
            if key == "date":
                data[key] = datetime.datetime.utcnow().isoformat() + "Z"
            else:
                data[key] += generate_movement()


async def main():
    async with websockets.serve(set_tickers, "localhost", PORT):
        await asyncio.Future()


if __name__ == "__main__":
    print(f"Server listening on port {PORT}")
    asyncio.run(main())
