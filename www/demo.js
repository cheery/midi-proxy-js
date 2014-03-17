// Generated by CoffeeScript 1.6.3
(function() {
  var createOscillator, frequencyFromNote, info, log2, main, noteFromFrequency, pressNote, releaseNote;

  if (window.AudioContext == null) {
    window.AudioContext = window.webkitAudioContext;
  }

  main = function() {
    var ctx, keyboard, ws;
    ctx = new AudioContext();
    keyboard = {};
    ws = new WebSocket('ws://localhost:9898/');
    ws.onopen = function(evt) {
      return info('connected');
    };
    ws.onclose = function(evt) {
      return info('disconnected');
    };
    ws.onmessage = function(evt) {
      var key, message;
      message = JSON.parse(evt.data);
      switch (message.type) {
        case 'note':
          if (message.press) {
            key = pressNote(ctx, message.note, message.velocity / 2 + 0.2);
            return keyboard[message.note] = key;
          } else {
            return releaseNote(ctx, keyboard[message.note]);
          }
      }
    };
    return ws.onerror = function(evt) {
      return info("error: " + evt.data);
    };
  };

  pressNote = function(ctx, note, volume, attack, release) {
    var freq, gain, now, osc;
    if (volume == null) {
      volume = 1.0;
    }
    if (attack == null) {
      attack = 0.25;
    }
    if (release == null) {
      release = 0.2;
    }
    freq = frequencyFromNote(note);
    gain = ctx.createGain();
    osc = createOscillator(ctx, freq);
    osc.connect(gain);
    gain.connect(ctx.destination);
    now = ctx.currentTime;
    gain.gain.setValueAtTime(0.0, now);
    gain.gain.linearRampToValueAtTime(volume, now + attack);
    return {
      osc: osc,
      gain: gain,
      volume: volume,
      attack: attack,
      release: release
    };
  };

  releaseNote = function(ctx, key) {
    var now;
    now = ctx.currentTime;
    key.gain.gain.linearRampToValueAtTime(0.0, now + key.release);
    return key.osc.stop(now + key.release);
  };

  createOscillator = function(ctx, freq) {
    var osc;
    osc = ctx.createOscillator();
    osc.frequency.value = freq;
    osc.type = "triangle";
    osc.start(0);
    return osc;
  };

  noteFromFrequency = function(freq) {
    return 69 + 12 * log2(freq / 440);
  };

  frequencyFromNote = function(note) {
    return Math.pow(2, (note - 69) / 12) * 440;
  };

  log2 = function(x) {
    return Math.log(x) / Math.LN2;
  };

  info = function(message) {
    var par;
    par = document.createElement('p');
    par.innerHTML = message;
    return document.body.appendChild(par);
  };

  window.addEventListener('load', main);

}).call(this);
