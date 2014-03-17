window.AudioContext ?= window.webkitAudioContext

main = () ->
    ctx = new AudioContext()

    keyboard = {}

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
                    key = pressNote(ctx, message.note, message.velocity/2+0.2)
                    keyboard[message.note] = key
                else
                    releaseNote(ctx, keyboard[message.note])
    ws.onerror = (evt) ->
        info "error: #{evt.data}"

pressNote = (ctx, note, volume=1.0, attack=0.25, release=0.2) ->
    freq = frequencyFromNote(note)
    gain = ctx.createGain()
    osc = createOscillator(ctx, freq)
    osc.connect(gain)
    gain.connect(ctx.destination)
    now = ctx.currentTime
    gain.gain.setValueAtTime(0.0, now)
    gain.gain.linearRampToValueAtTime(volume, now + attack)
    return {osc, gain, volume, attack, release}

releaseNote = (ctx, key) ->
    now = ctx.currentTime
    key.gain.gain.linearRampToValueAtTime(0.0, now + key.release)
    key.osc.stop(now + key.release)

createOscillator = (ctx, freq) ->
    osc = ctx.createOscillator()
    osc.frequency.value = freq
    osc.type = "triangle"
    osc.start(0)
    return osc

noteFromFrequency = (freq) -> 69 + 12 * log2(freq / 440)
frequencyFromNote = (note) -> Math.pow(2, (note-69)/12) * 440

log2 = (x) ->
    return Math.log(x) / Math.LN2

info = (message) ->
    par = document.createElement('p')
    par.innerHTML = message
    document.body.appendChild(par)

window.addEventListener('load', main)
