/* =========================================================================
   VoiceCore — embeddable reception widget
   Blessed Digital Solutions

   One script tag on any client site:
     <script src="/app/voicecore/engine.js"></script>
     <script src="/app/voicecore/widget.js" data-business="Nakawa Dental"></script>

   Styles are injected here so the widget carries no CSS dependency and
   cannot be broken by the host page's stylesheet.
   ========================================================================= */
(function (global) {
  'use strict';

  if (!global.VoiceCore) {
    console.error('VoiceCore widget: engine.js must load first.');
    return;
  }

  var VC = global.VoiceCore;
  var CSS = [
    '.vc-root{--vc-navy:#08122a;--vc-navy-2:#0b1b3a;--vc-gold:#c9a227;--vc-gold-2:#dcbb4e;',
    '--vc-gold-3:#ecd48b;--vc-ink:#f2f5fb;--vc-slate:#93a2bb;--vc-line:rgba(255,255,255,.13);',
    "font-family:'Inter',-apple-system,'Segoe UI',system-ui,sans-serif;position:fixed;right:20px;bottom:20px;z-index:2147483000;}",
    '.vc-root *{box-sizing:border-box;margin:0;}',
    '.vc-launch{display:flex;align-items:center;gap:.6rem;border:0;cursor:pointer;padding:.8rem 1.25rem;',
    'border-radius:999px;background:linear-gradient(140deg,var(--vc-gold-2),#a8811a);color:var(--vc-navy);',
    "font-family:'Jost','Segoe UI',sans-serif;font-weight:600;font-size:.95rem;letter-spacing:.01em;",
    'box-shadow:0 12px 30px -10px rgba(201,162,39,.85);transition:transform .2s ease,box-shadow .2s ease;}',
    '.vc-launch:hover{transform:translateY(-2px);box-shadow:0 18px 36px -12px rgba(201,162,39,1);}',
    '.vc-launch svg{width:19px;height:19px;}',
    '.vc-dot{width:8px;height:8px;border-radius:50%;background:#1f9d55;box-shadow:0 0 0 3px rgba(31,157,85,.28);}',
    '.vc-dot.vc-off{background:#c9a227;box-shadow:0 0 0 3px rgba(201,162,39,.25);}',
    '.vc-panel{width:min(94vw,392px);height:min(78vh,620px);background:var(--vc-navy);border:1px solid var(--vc-line);',
    'border-radius:18px;overflow:hidden;display:none;flex-direction:column;color:var(--vc-ink);',
    'box-shadow:0 40px 90px -30px rgba(0,0,0,.85);}',
    '.vc-root[data-open="1"] .vc-panel{display:flex;}',
    '.vc-root[data-open="1"] .vc-launch{display:none;}',
    '.vc-head{padding:.9rem 1rem;border-bottom:1px solid var(--vc-line);display:flex;align-items:center;gap:.75rem;',
    'background:linear-gradient(140deg,var(--vc-navy-2),var(--vc-navy));}',
    '.vc-av{width:40px;height:40px;border-radius:11px;flex:none;display:grid;place-items:center;',
    'background:linear-gradient(150deg,var(--vc-gold-2),#a8811a);color:var(--vc-navy);',
    "font-family:'Jost',sans-serif;font-weight:600;font-size:1.05rem;}",
    ".vc-who{flex:1;min-width:0;line-height:1.25;}",
    ".vc-who b{font-family:'Jost',sans-serif;font-weight:500;font-size:1rem;display:block;}",
    '.vc-who span{font-size:.74rem;color:var(--vc-slate);display:flex;align-items:center;gap:.4rem;letter-spacing:.04em;}',
    '.vc-x{background:none;border:0;color:var(--vc-slate);cursor:pointer;font-size:1.5rem;line-height:1;padding:.2rem .4rem;border-radius:6px;}',
    '.vc-x:hover{color:#fff;background:rgba(255,255,255,.08);}',
    '.vc-chan{display:flex;gap:0;border-bottom:1px solid var(--vc-line);background:rgba(255,255,255,.02);}',
    '.vc-chan button{flex:1;background:none;border:0;border-bottom:2px solid transparent;cursor:pointer;',
    "padding:.55rem .3rem;color:var(--vc-slate);font-family:'Jost',sans-serif;font-size:.76rem;",
    'letter-spacing:.12em;text-transform:uppercase;}',
    '.vc-chan button[aria-pressed="true"]{color:var(--vc-gold-3);border-bottom-color:var(--vc-gold);}',
    '.vc-log{flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:.7rem;scroll-behavior:smooth;}',
    '.vc-msg{max-width:86%;padding:.7rem .9rem;border-radius:14px;font-size:.93rem;line-height:1.55;white-space:pre-wrap;}',
    '.vc-msg.vc-agent{align-self:flex-start;background:rgba(255,255,255,.06);border:1px solid var(--vc-line);border-bottom-left-radius:5px;}',
    '.vc-msg.vc-cust{align-self:flex-end;background:linear-gradient(150deg,var(--vc-gold-2),#a8811a);color:var(--vc-navy);',
    'font-weight:500;border-bottom-right-radius:5px;}',
    '.vc-msg.vc-sys{align-self:center;background:none;border:1px dashed var(--vc-line);color:var(--vc-slate);',
    'font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;padding:.35rem .8rem;border-radius:999px;}',
    '.vc-msg.vc-urgent{border-color:rgba(201,162,39,.55);box-shadow:0 0 0 1px rgba(201,162,39,.25) inset;}',
    '.vc-quick{display:flex;flex-wrap:wrap;gap:.4rem;padding:0 1rem .6rem;}',
    '.vc-quick button{background:rgba(255,255,255,.05);border:1px solid var(--vc-line);color:var(--vc-ink);',
    'border-radius:999px;padding:.42rem .85rem;font-size:.82rem;cursor:pointer;transition:border-color .2s,background .2s;}',
    '.vc-quick button:hover{border-color:var(--vc-gold);background:rgba(201,162,39,.14);}',
    '.vc-typing{align-self:flex-start;display:flex;gap:4px;padding:.75rem .95rem;background:rgba(255,255,255,.06);',
    'border:1px solid var(--vc-line);border-radius:14px;border-bottom-left-radius:5px;}',
    '.vc-typing i{width:6px;height:6px;border-radius:50%;background:var(--vc-slate);animation:vcb 1.1s infinite;}',
    '.vc-typing i:nth-child(2){animation-delay:.16s;}.vc-typing i:nth-child(3){animation-delay:.32s;}',
    '@keyframes vcb{0%,60%,100%{opacity:.25;transform:translateY(0);}30%{opacity:1;transform:translateY(-3px);}}',
    '.vc-foot{border-top:1px solid var(--vc-line);padding:.7rem;display:flex;gap:.5rem;align-items:flex-end;',
    'background:rgba(255,255,255,.02);}',
    '.vc-foot textarea{flex:1;resize:none;background:rgba(255,255,255,.06);border:1px solid var(--vc-line);',
    'border-radius:12px;color:var(--vc-ink);padding:.6rem .8rem;font-size:.92rem;line-height:1.45;max-height:96px;',
    "font-family:inherit;}",
    '.vc-foot textarea::placeholder{color:#6d7d99;}',
    '.vc-foot textarea:focus{outline:none;border-color:var(--vc-gold);}',
    '.vc-btn{width:40px;height:40px;flex:none;border-radius:11px;border:1px solid var(--vc-line);cursor:pointer;',
    'background:rgba(255,255,255,.06);color:var(--vc-ink);display:grid;place-items:center;transition:all .2s;}',
    '.vc-btn:hover{border-color:var(--vc-gold);color:var(--vc-gold-3);}',
    '.vc-btn svg{width:18px;height:18px;}',
    '.vc-btn.vc-send{background:linear-gradient(140deg,var(--vc-gold-2),#a8811a);color:var(--vc-navy);border-color:transparent;}',
    '.vc-btn.vc-live{background:#b3261e;color:#fff;border-color:transparent;animation:vcp 1.2s infinite;}',
    '@keyframes vcp{0%,100%{box-shadow:0 0 0 0 rgba(179,38,30,.6);}50%{box-shadow:0 0 0 7px rgba(179,38,30,0);}}',
    '.vc-note{padding:0 1rem .7rem;font-size:.7rem;color:#6d7d99;letter-spacing:.06em;text-align:center;}',
    '@media (prefers-reduced-motion:reduce){.vc-root *{animation:none!important;transition:none!important;}}'
  ].join('');

  var ICON = {
    phone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6.6 3h3.2l1.6 4-2 1.4a12 12 0 0 0 5.2 5.2l1.4-2 4 1.6v3.2A2.6 2.6 0 0 1 17.4 19 14.4 14.4 0 0 1 5 6.6 2.6 2.6 0 0 1 6.6 3Z"/></svg>',
    mic: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>',
    send: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'
  };

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  function Widget(opts) {
    opts = opts || {};
    this.channel = 'web';
    this.speak = opts.speak !== false;
    this.session = null;
    this.build();
    if (opts.open) this.open();
  }

  Widget.prototype.build = function () {
    var self = this;
    var cfg = VC.config;

    var style = el('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    var root = el('div', 'vc-root');
    root.setAttribute('data-open', '0');

    /* Launcher */
    var launch = el('button', 'vc-launch');
    launch.type = 'button';
    launch.innerHTML = ICON.phone + '<span>Talk to ' + esc(cfg.persona) + '</span>';
    launch.setAttribute('aria-label', 'Open reception chat');
    launch.addEventListener('click', function () { self.open(); });

    /* Panel */
    var panel = el('div', 'vc-panel');
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', cfg.persona + ' — reception');

    var open = self.isOpenNow();
    var head = el('div', 'vc-head');
    head.appendChild(el('div', 'vc-av', esc(cfg.persona.charAt(0))));
    var who = el('div', 'vc-who');
    who.innerHTML = '<b>' + esc(cfg.persona) + '</b><span><i class="vc-dot' + (open ? '' : ' vc-off') +
      '"></i>' + (open ? 'Answering now' : 'After hours — still answering') + '</span>';
    head.appendChild(who);
    var close = el('button', 'vc-x', '&times;');
    close.type = 'button';
    close.setAttribute('aria-label', 'Close');
    close.addEventListener('click', function () { self.close(); });
    head.appendChild(close);

    /* Channel switcher — proves one memory across all three */
    var chan = el('div', 'vc-chan');
    ['web', 'whatsapp', 'phone'].forEach(function (c) {
      var b = el('button', null, c === 'web' ? 'Web chat' : c === 'whatsapp' ? 'WhatsApp' : 'Phone');
      b.type = 'button';
      b.setAttribute('aria-pressed', c === 'web' ? 'true' : 'false');
      b.addEventListener('click', function () { self.switchChannel(c); });
      chan.appendChild(b);
    });

    var log = el('div', 'vc-log');
    log.setAttribute('role', 'log');
    log.setAttribute('aria-live', 'polite');

    var quick = el('div', 'vc-quick');

    var foot = el('div', 'vc-foot');
    var ta = el('textarea');
    ta.rows = 1;
    ta.placeholder = 'Type, or tap the mic to speak…';
    ta.setAttribute('aria-label', 'Your message');
    ta.addEventListener('input', function () {
      ta.style.height = 'auto';
      ta.style.height = Math.min(ta.scrollHeight, 96) + 'px';
    });
    ta.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); self.submit(); }
    });
    var mic = el('button', 'vc-btn vc-mic', ICON.mic);
    mic.type = 'button';
    mic.setAttribute('aria-label', 'Speak');
    mic.addEventListener('click', function () { self.toggleMic(); });
    var send = el('button', 'vc-btn vc-send', ICON.send);
    send.type = 'button';
    send.setAttribute('aria-label', 'Send');
    send.addEventListener('click', function () { self.submit(); });
    foot.appendChild(ta); foot.appendChild(mic); foot.appendChild(send);

    var note = el('div', 'vc-note', 'VoiceCore by Blessed Digital Solutions');

    panel.appendChild(head); panel.appendChild(chan); panel.appendChild(log);
    panel.appendChild(quick); panel.appendChild(foot); panel.appendChild(note);
    root.appendChild(panel); root.appendChild(launch);
    document.body.appendChild(root);

    this.root = root; this.log = log; this.quick = quick; this.ta = ta; this.mic = mic;
    this.headWho = who;

    if (!('speechSynthesis' in window)) this.speak = false;
    this.setupRecognition();
  };

  Widget.prototype.isOpenNow = function () {
    var now = new Date();
    return VC.hours.isOpenAt(now, { h: now.getHours(), m: now.getMinutes() });
  };

  Widget.prototype.open = function () {
    this.root.setAttribute('data-open', '1');
    if (!this.session) {
      this.session = new VC.Session(this.channel);
      this.agent(this.session.greeting());
      this.renderQuick(['Book an appointment', 'What are your prices?', 'Are you open now?']);
    }
    this.ta.focus();
  };

  Widget.prototype.close = function () {
    this.root.setAttribute('data-open', '0');
    this.stopMic();
  };

  Widget.prototype.switchChannel = function (c) {
    if (c === this.channel) return;
    this.channel = c;
    var btns = this.root.querySelectorAll('.vc-chan button');
    ['web', 'whatsapp', 'phone'].forEach(function (name, i) {
      btns[i].setAttribute('aria-pressed', name === c ? 'true' : 'false');
    });
    var label = c === 'web' ? 'web chat' : c === 'whatsapp' ? 'WhatsApp' : 'phone';
    this.system('Continued on ' + label + ' — same conversation');
    if (this.session) {
      this.session.channel = c;
      VC.store.openConversation(c, this.session.sessionId, this.session.slots.phone);
    }
  };

  Widget.prototype.bubble = function (cls, text) {
    var b = el('div', 'vc-msg ' + cls);
    b.textContent = text;
    this.log.appendChild(b);
    this.log.scrollTop = this.log.scrollHeight;
    return b;
  };

  Widget.prototype.agent = function (text, meta) {
    var b = this.bubble('vc-agent', text);
    if (meta && meta.urgent) b.classList.add('vc-urgent');
    this.say(text);
    return b;
  };

  Widget.prototype.system = function (text) { this.bubble('vc-sys', text); };

  Widget.prototype.renderQuick = function (items) {
    var self = this;
    this.quick.innerHTML = '';
    (items || []).forEach(function (label) {
      var b = el('button', null, esc(label));
      b.type = 'button';
      b.addEventListener('click', function () { self.send(label); });
      self.quick.appendChild(b);
    });
  };

  Widget.prototype.submit = function () {
    var text = this.ta.value.trim();
    if (!text) return;
    this.ta.value = '';
    this.ta.style.height = 'auto';
    this.send(text);
  };

  Widget.prototype.send = function (text) {
    var self = this;
    if (!this.session) this.open();
    this.bubble('vc-cust', text);
    this.renderQuick([]);

    var typing = el('div', 'vc-typing', '<i></i><i></i><i></i>');
    this.log.appendChild(typing);
    this.log.scrollTop = this.log.scrollHeight;

    var delay = Math.min(1100, 320 + text.length * 12);
    setTimeout(function () {
      typing.remove();
      var before = VC.store.get(self.session.conversationId);
      var reply = self.session.reply(text);
      var after = VC.store.get(self.session.conversationId);
      var last = after.messages[after.messages.length - 1];
      var meta = last && last.meta ? last.meta : null;
      self.agent(reply, meta);
      self.renderQuick(meta && meta.quick ? meta.quick : []);
      if (meta && meta.booking) self.system('Booking written to the dashboard');
      if (before && after && before.tag !== after.tag) {
        self.system('Tagged: ' + after.tag);
      }
    }, delay);
  };

  /* ---- Voice: speech synthesis out ---- */
  Widget.prototype.say = function (text) {
    if (!this.speak || !('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(text);
      var lang = this.session ? VC.languages[this.session.lang] : null;
      u.lang = lang ? lang.speech : 'en-GB';
      u.rate = 1.02;
      u.pitch = 1.05;
      window.speechSynthesis.speak(u);
    } catch (e) { /* voice is a bonus, never a blocker */ }
  };

  /* ---- Voice: speech recognition in ---- */
  Widget.prototype.setupRecognition = function () {
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { this.mic.title = 'Voice input is not supported in this browser'; return; }
    var self = this;
    var rec = new SR();
    rec.continuous = false;
    rec.interimResults = true;
    rec.lang = 'en-GB';
    rec.addEventListener('result', function (e) {
      var text = '';
      for (var i = e.resultIndex; i < e.results.length; i++) text += e.results[i][0].transcript;
      self.ta.value = text;
      if (e.results[e.results.length - 1].isFinal) {
        self.stopMic();
        self.submit();
      }
    });
    rec.addEventListener('end', function () { self.stopMic(); });
    rec.addEventListener('error', function () { self.stopMic(); });
    this.rec = rec;
  };

  Widget.prototype.toggleMic = function () {
    if (!this.rec) {
      this.system('Voice input needs Chrome or Edge — typing works everywhere');
      return;
    }
    if (this.listening) { this.stopMic(); return; }
    try {
      if (this.session) this.rec.lang = VC.languages[this.session.lang].speech;
      this.rec.start();
      this.listening = true;
      this.mic.classList.add('vc-live');
      this.ta.placeholder = 'Listening…';
    } catch (e) { this.stopMic(); }
  };

  Widget.prototype.stopMic = function () {
    if (!this.listening) return;
    this.listening = false;
    this.mic.classList.remove('vc-live');
    this.ta.placeholder = 'Type, or tap the mic to speak…';
    try { this.rec.stop(); } catch (e) {}
  };

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  VC.Widget = Widget;

  /* Auto-mount from the script tag's data attributes */
  var tag = document.currentScript;
  if (tag && tag.dataset.autostart !== 'false') {
    var patch = {};
    if (tag.dataset.business) patch.business = tag.dataset.business;
    if (tag.dataset.persona) patch.persona = tag.dataset.persona;
    if (tag.dataset.phone) patch.handoffNumber = patch.phone = tag.dataset.phone;
    if (Object.keys(patch).length) VC.configure(patch);
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { VC.widget = new Widget(); });
    } else {
      VC.widget = new Widget();
    }
  }
})(window);
