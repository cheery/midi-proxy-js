from asyncio import schedule, http, log
from asyncio.log import Logger
from asyncio.filehost import FileHost, mimetypes
import sys, os, json
import stream

devices_dir = "/dev/snd"
websockets = []

filehost = FileHost(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'www'))

def main():
    nomidi = True
    for filename in os.listdir(devices_dir):
        path = os.path.join(devices_dir, filename)
        if filename.startswith('midi'):
            fd = stream.open(path)
            schedule(read_midi, fd)
            nomidi = False
    if nomidi:
        print("no midi devices found")
        sys.exit(1)

    log = Logger(sys.stdout, sys.stdout)
    server = http.Server(http_application, log, port=9898)
    schedule(server.run)

    schedule.run()

def read_midi(fd):
    while 1:
        code = ord(fd.read(1))
        channel = code & 0xF
        if code & 0xF0 == 0x90: # note on
            note     = ord(fd.read(1))
            velocity = ord(fd.read(1)) / 127.0
            broadcast({"type":"note", "press":True, "channel":channel, "note":note, "velocity":velocity})
        elif code & 0xF0 == 0x80: # note off
            note     = ord(fd.read(1))
            velocity = ord(fd.read(1)) / 127.0
            broadcast({"type":"note", "press":False, "channel":channel, "note":note, "velocity":velocity})
        else:
            print("ignored hex=%x" % code)

def broadcast(message):
    text = json.dumps(message)
    for ws in websockets:
        ws.sendText(text)

def http_application(request, response):
    if request.websocket:
        response.upgrade(websocket_callback)
    else:
        return filehost(request, response)

def websocket_callback(command, payload):
    if command=='connect':
        websockets.append(payload)
    elif command=='close':
        websockets.remove(payload)
    else:
        print(command, payload)

if __name__=='__main__':
    main()
