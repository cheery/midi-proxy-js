# Midi Proxy for Javascript

This simple proxy relays the MIDI events from physical devices into your browser. It runs only on Linux.

There are [more details in my blog](http://boxbase.org/entries/2014/mar/17/midi-proxy)

## Function

Whenever you connect a websocket into a localhost:9898, and you have the proxy running, it will send MIDI events to the socket until you disconnect.

There is a single type of event it relays. It's an object in JSON format. Contains following fields:

 * `type` - this is "note"
 * `press` - whether the note was pressed or not.
 * `channel` - channel of the MIDI device
 * `note` - note that was played
 * `velocity` - velocity of the key

Here's a small example, written in coffeescript:

    ws = new WebSocket('ws://localhost:9898/')
    ws.onopen = (evt) ->
        info 'connected'
    ws.onclose = (evt) ->
        info 'disconnected'
    ws.onmessage = (evt) ->
        message = JSON.parse(evt.data)
        switch message.type
            when 'note'
                if message.press
                    console.log "press",   message.note, message.velocity
                else
                    console.log "release", message.note, message.velocity
    ws.onerror = (evt) ->
        info "error: #{evt.data}"

## Installation

Install greenlets, for example via pip:

    pip install greenlet

Download the `asyncio` module from [codeflow.org](http://codeflow.org/):

    wget http://codeflow.org/download/asyncio.tar.bz2
    tar -xf asyncio.tar.bz2

Plug in your MIDI keyboard, Run the midi-proxy.py:

    python midi-proxy.py

Browse to the [http://localhost:9898/](http://localhost:9898/) and press a key on your keyboard. It should play a sound.
