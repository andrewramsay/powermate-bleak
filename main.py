import socket
import time
import argparse
import asyncio

from bleak import BleakClient
 
DEFAULT_ADDRESS = "00:12:92:08:01:FB" 
CC_UUID = "9cf53570-ddd9-47f3-ba63-09acefc60415"

ip = None
port = None
udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

async def callback(sender, data):
    if data[0] == 103:
        message = 'rotate_anticlockwise'
    elif data[0] == 104:
        message = 'rotate_clockwise'
    elif data[0] == 101:
        message = 'press'
    elif data[0] == 112:
        message = 'press_clockwise'
    elif data[0] == 105:
        message = 'press_anticlockwise'
    elif data[0] >= 114 and data[0] <= 119:
        message = f'long_press_{data[0] - 113}'
    elif data[0] == 102:
        message = 'release'
    else:
        message = f'unknown_{data[0]}'

    udpsocket.sendto(message.encode('utf-8'), (ip, port))
 
async def main(address):
    async with BleakClient(address) as bc:
        print('Connected to device, Ctrl-C to disconnect!')
        await bc.start_notify(CC_UUID, callback)
        while True:
            await asyncio.sleep(1)
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', '-i', required=False, default='127.0.0.1')
    parser.add_argument('--port', '-p', required=False, default=12345)
    parser.add_argument('--address', '-a', required=False, default=DEFAULT_ADDRESS)
    args = parser.parse_args()
    ip = args.ip
    port = args.port

    try:
        asyncio.run(main(args.address))
    except KeyboardInterrupt:
        pass
