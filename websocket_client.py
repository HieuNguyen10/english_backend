# import asyncio
# import logging
#
import websockets
#
# logger = logging.getLogger(__name__)
#
# is_alive = True
#
#
# async def alive():
#     while is_alive:
#         logger.info('alive')
#         await asyncio.sleep(300)
#
#
# async def async_processing():
#     async with websockets.connect('ws://localhost:5002/api/v1/notice/ws') as websocket:
#         print(f"websocket: {websocket}")
#         while True:
#             try:
#                 message = await websocket.recv()
#                 print(message)
#
#             except websockets.ConnectionClosed:
#                 print('ConnectionClosed')
#                 is_alive = False
#                 break
#
#
# # asyncio.get_event_loop().run_until_complete(asyncio.wait([
# #    alive(),
# #    async_processing()
# # ]))
#
#
# from contextlib import closing
# from websocket import create_connection
#
# with websockets.connect('ws://localhost:5002/api/v1/notice/ws') as websocket:
#     message = websocket.recv()
#     print(message)



import asyncio
import logging
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.basename(__file__), "..")))


PORT = int(os.environ.get("PORT") or "5002")


async def on_events(data, topic):
    print(f"running callback for {topic}!")


async def main():
    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImlhdCI6MTY3MjgyNzc5NSwibmJmIjoxNjcyODI3Nzk1LCJqdGkiOiJhMzUxY2YwNS0yZWRjLTQyN2UtOWQ3YS1iMmMzNWZjMDgwMWUiLCJleHAiOjE2NzI5MTQxOTUsInR5cGUiOiJhY2Nlc3MiLCJmcmVzaCI6ZmFsc2V9.ccsZL93U7sVoP03pIvYcNs-e0csNhJy2jhgI-0cMJe0"}

    async with websockets.connect(extra_headers=headers, origin="*", uri="ws://127.0.0.1:5002/api/v1/notice/message/1") as websocket:
        # await websocket.send(headers)
        while True:
            message = await websocket.recv()
            if message:
                print(message)
            else:
                await websocket.close()
                break

    # client = PubSubClient(["guns", "germs"], callback=on_events)

    # async def on_steel(data, topic):
    #     print("running callback steel!")
    #     print("Got data", data)
    #     asyncio.create_task(client.disconnect())
    #
    # client.subscribe("steel", on_steel)
    # client.start_client(f"ws://127.0.0.1:5002/api/v1/notice/message")
    #
    # await client.wait_until_done()


if __name__ == '__main__':
    asyncio.run(main())
