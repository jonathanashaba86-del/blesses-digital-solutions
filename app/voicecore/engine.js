/* =========================================================================
   VoiceCore — conversation engine
   Blessed Digital Solutions

   Runs entirely in the browser. No backend, no API keys. Every business is
   configured through VoiceCore.config, so one build white-labels per client.

   The intent layer is deterministic on purpose: it is auditable, it works
   offline, and it never invents a price or a booking slot. When an LLM is
   wired in later it plugs into Brain.reply() as a fallback for `unknown`,
   leaving booking, pricing and hours answered from the config as they are.
   ========================================================================= */
(function (global) {
  'use strict';

  var VoiceCore = {};

  /* ---------------------------------------------------------------------
     1. Business configuration
     --------------------------------------------------------------------- */
  VoiceCore.defaultConfig = {
    business: 'Nakawa Dental Clinic',
    persona: 'Maria',
    tagline: 'Reception',
    location: 'Plot 14, Jinja Road, Kampala',
    phone: '+256 700 123 456',
    languages: ['en', 'lg', 'sw'],
    hours: {
      mon: [8, 18], tue: [8, 18], wed: [8, 18], thu: [8, 18],
      fri: [8, 18], sat: [9, 14], sun: null
    },
    services: [
      { name: 'Consultation', minutes: 30, price: 'UGX 30,000' },
      { name: 'Teeth cleaning', minutes: 45, price: 'UGX 80,000' },
      { name: 'Filling', minutes: 60, price: 'UGX 150,000' },
      { name: 'Extraction', minutes: 45, price: 'UGX 120,000' }
    ],
    handoffNumber: '+256 700 123 456',
    afterHoursPromise: 'The team calls back the next working morning.'
  };

  VoiceCore.config = JSON.parse(JSON.stringify(VoiceCore.defaultConfig));

  VoiceCore.configure = function (patch) {
    Object.keys(patch || {}).forEach(function (k) { VoiceCore.config[k] = patch[k]; });
    return VoiceCore.config;
  };

  /* ---------------------------------------------------------------------
     2. Language
     --------------------------------------------------------------------- */
  var DAY_KEYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
  var DAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  var LANG = {
    en: {
      label: 'English',
      speech: 'en-GB',
      greet: function (c) {
        return 'Hello, you have reached ' + c.business + '. This is ' + c.persona +
          '. How can I help you today?';
      },
      askService: 'Certainly. Which service do you need?',
      askDay: 'Which day suits you?',
      askTime: 'What time works best?',
      askName: 'May I have your name for the booking?',
      askPhone: 'And a phone number we can confirm on?',
      closed: 'We are closed then. ',
      offer: 'The nearest open time is ',
      confirmed: 'Booked. ',
      summarySent: 'I have sent the confirmation by SMS.',
      handoff: 'Let me put you through to the team on ',
      handoffCtx: ' They will have this whole conversation in front of them, so you will not repeat yourself.',
      complaint: 'I am sorry that happened, and thank you for telling us. I am flagging this for the owner now, marked urgent.',
      thanks: 'My pleasure. Anything else?',
      bye: 'Thank you for calling ' + '', 
      unknown: 'I want to get this right rather than guess. I am passing you to a colleague — one moment.',
      hoursIntro: 'Our hours are: ',
      priceIntro: 'Here is what those cost: ',
      locationIntro: 'We are at ',
      servicesIntro: 'We offer: '
    },
    lg: {
      label: 'Luganda',
      speech: 'en-GB',
      greet: function (c) {
        return 'Oli otya, otutuuseeko ku ' + c.business + '. Nze ' + c.persona +
          '. Nnyinza ntya okukuyamba leero?';
      },
      askService: 'Kale. Mpulira oyagala mukolo ki?',
      askDay: 'Oyagala lunaku ki?',
      askTime: 'Ssaawa mmeka esinga okukugwanira?',
      askName: 'Erinnya lyo ge ani?',
      askPhone: 'Ne namba ya ssimu gy’oyinza okukakasibwako?',
      closed: 'Ku ssaawa ezo tuba tuggaddewo. ',
      offer: 'Ekiseera ekisinga okumpi kye ',
      confirmed: 'Kikwatiddwa. ',
      summarySent: 'Nkuweerezza obubaka bwa SMS okukakasa.',
      handoff: 'Ka nkuwe omukozi ku ',
      handoffCtx: ' Ajja kuba n’emboozi eno yonna, tojja kuddamu kwogera byonna.',
      complaint: 'Nsonyiwa nnyo olw’ekyo, era webale okutubuulira. Nkitwala eri nnannyini bizinensi kati, nga kya bwangu.',
      thanks: 'Kirungi. Waliwo ekirala?',
      bye: 'Webale nnyo.',
      unknown: 'Njagala nkuwe eky’amazima so si kuteebereza. Ka nkuwe munnange — lindako katono.',
      hoursIntro: 'Essaawa zaffe: ',
      priceIntro: 'Bino bye bibalirwa: ',
      locationIntro: 'Tuli ku ',
      servicesIntro: 'Tuwa: '
    },
    sw: {
      label: 'Kiswahili',
      speech: 'sw-KE',
      greet: function (c) {
        return 'Habari, umefika ' + c.business + '. Mimi ni ' + c.persona +
          '. Nikusaidieje leo?';
      },
      askService: 'Sawa. Unahitaji huduma gani?',
      askDay: 'Siku gani inakufaa?',
      askTime: 'Saa ngapi inakufaa zaidi?',
      askName: 'Naomba jina lako kwa ajili ya miadi.',
      askPhone: 'Na namba ya simu tutakayothibitisha nayo?',
      closed: 'Tumefungwa wakati huo. ',
      offer: 'Muda wa karibu zaidi ni ',
      confirmed: 'Imehifadhiwa. ',
      summarySent: 'Nimetuma uthibitisho kwa SMS.',
      handoff: 'Nitakuunganisha na timu kwa ',
      handoffCtx: ' Watakuwa na mazungumzo haya yote, hutarudia chochote.',
      complaint: 'Samahani sana kwa hilo, na asante kwa kutuambia. Ninapeleka hili kwa mmiliki sasa, kama la haraka.',
      thanks: 'Karibu sana. Kuna kingine?',
      bye: 'Asante kwa kupiga simu.',
      unknown: 'Nataka kukupa jibu sahihi badala ya kubahatisha. Nitakuunganisha na mwenzangu — subiri kidogo.',
      hoursIntro: 'Saa zetu za kazi: ',
      priceIntro: 'Gharama ni hizi: ',
      locationIntro: 'Tupo ',
      servicesIntro: 'Tunatoa: '
    }
  };

  VoiceCore.languages = LANG;

  /* Language hints — short, high-signal words only, so a single Luganda or
     Swahili word in an English sentence does not flip the whole conversation. */
  var LANG_HINTS = {
    lg: ['oli otya', 'webale', 'nkwagala', 'nsonyiwa', 'ssaawa', 'olunaku', 'nnyabo',
         'ssebo', 'bambi', 'njagala', 'kale', 'nedda', 'ye ani', 'mmeka', 'wano'],
    sw: ['habari', 'asante', 'samahani', 'karibu', 'ninahitaji', 'nataka', 'saa ngapi',
         'lini', 'wapi', 'bei gani', 'tafadhali', 'ndiyo', 'hapana', 'sawa']
  };

  function detectLanguage(text, current) {
    var t = ' ' + text.toLowerCase() + ' ';
    var best = null, bestScore = 0;
    Object.keys(LANG_HINTS).forEach(function (code) {
      var score = 0;
      LANG_HINTS[code].forEach(function (w) {
        if (t.indexOf(' ' + w) !== -1 || t.indexOf(w + ' ') !== -1) score += w.indexOf(' ') !== -1 ? 2 : 1;
      });
      if (score > bestScore) { bestScore = score; best = code; }
    });
    return bestScore >= 2 ? best : (current || 'en');
  }

  /* ---------------------------------------------------------------------
     3. Intent detection
     --------------------------------------------------------------------- */
  var INTENTS = [
    { name: 'complaint', weight: 3, patterns: [
      'complain', 'complaint', 'terrible', 'awful', 'rude', 'angry', 'unhappy',
      'disappointed', 'refund', 'wasted', 'never came', 'still waiting', 'poor service',
      'bad service', 'kibi', 'tekirungi', 'mbi', 'malalamiko', 'nsonyiwa naye'
    ] },
    { name: 'human', weight: 3, patterns: [
      'speak to someone', 'talk to a person', 'real person', 'human', 'manager',
      'owner', 'put me through', 'transfer me', 'someone else', 'muntu', 'mtu halisi'
    ] },
    { name: 'booking', weight: 2, patterns: [
      'book', 'booking', 'appointment', 'reserve', 'reservation', 'schedule',
      'slot', 'come in', 'see the doctor', 'available', 'availability', 'fit me in',
      'njagala okulagaana', 'okulagaana', 'miadi', 'nataka kuweka'
    ] },
    { name: 'price', weight: 2, patterns: [
      'how much', 'price', 'cost', 'charge', 'fee', 'rate', 'expensive',
      'ssente', 'bbeeyi', 'mmeka', 'bei', 'gharama', 'pesa ngapi'
    ] },
    { name: 'hours', weight: 2, patterns: [
      'open', 'opening', 'close', 'closing', 'hours', 'what time do you',
      'are you open', 'weekend', 'sunday', 'ssaawa ki', 'muggula', 'saa ngapi mnafungua'
    ] },
    { name: 'location', weight: 2, patterns: [
      'where are you', 'location', 'address', 'directions', 'how do i get',
      'find you', 'wa muli', 'mpali', 'mko wapi', 'mahali'
    ] },
    { name: 'services', weight: 1, patterns: [
      'what do you do', 'services', 'offer', 'treatments', 'what can you',
      'do you do', 'mukola ki', 'huduma'
    ] },
    { name: 'greeting', weight: 1, patterns: [
      'hello', 'hi ', 'hey', 'good morning', 'good afternoon', 'good evening',
      'oli otya', 'habari', 'wasuze'
    ] },
    { name: 'thanks', weight: 1, patterns: [
      'thank', 'thanks', 'appreciate', 'webale', 'asante'
    ] },
    { name: 'bye', weight: 1, patterns: [
      'bye', 'goodbye', 'that is all', 'thats all', 'nothing else', 'weeraba', 'kwaheri'
    ] },
    { name: 'affirm', weight: 1, patterns: [
      'yes', 'yeah', 'yep', 'sure', 'ok', 'okay', 'correct', 'right', 'please do',
      'ye', 'kale', 'ndiyo', 'sawa'
    ] },
    { name: 'deny', weight: 1, patterns: [
      'no', 'nope', 'not really', 'cancel', 'nedda', 'hapana'
    ] }
  ];

  function detectIntent(text) {
    var t = ' ' + text.toLowerCase().replace(/[^\w\s]/g, ' ').replace(/\s+/g, ' ') + ' ';
    var scores = {};
    INTENTS.forEach(function (intent) {
      intent.patterns.forEach(function (p) {
        if (t.indexOf(' ' + p) !== -1 || t.indexOf(p) !== -1) {
          scores[intent.name] = (scores[intent.name] || 0) + intent.weight;
        }
      });
    });
    var best = 'unknown', bestScore = 0;
    Object.keys(scores).forEach(function (k) {
      if (scores[k] > bestScore) { bestScore = scores[k]; best = k; }
    });
    return { name: best, score: bestScore, all: scores };
  }

  /* ---------------------------------------------------------------------
     4. Slot extraction — day, time, service, name, phone
     --------------------------------------------------------------------- */
  function extractPhone(text) {
    var m = text.replace(/[\s\-()]/g, '').match(/(\+?256\d{9}|0\d{9}|\+\d{9,14})/);
    return m ? m[0] : null;
  }

  function extractDay(text) {
    var t = text.toLowerCase();
    var now = new Date();
    if (/\btoday\b|\bleero\b|\bleo\b/.test(t)) return startOfDay(now);
    if (/\btomorrow\b|\benkya\b|\bkesho\b/.test(t)) {
      var d = startOfDay(now); d.setDate(d.getDate() + 1); return d;
    }
    var names = {
      sunday: 0, sun: 0, monday: 1, mon: 1, tuesday: 2, tue: 2, tues: 2,
      wednesday: 3, wed: 3, thursday: 4, thu: 4, thur: 4, thurs: 4,
      friday: 5, fri: 5, saturday: 6, sat: 6
    };
    var found = null;
    Object.keys(names).forEach(function (n) {
      if (found === null && new RegExp('\\b' + n + '\\b').test(t)) found = names[n];
    });
    if (found !== null) {
      var target = startOfDay(now);
      var delta = (found - target.getDay() + 7) % 7;
      target.setDate(target.getDate() + (delta === 0 ? 7 : delta));
      return target;
    }
    var dm = t.match(/\b(\d{1,2})\s*[\/\-]\s*(\d{1,2})\b/);
    if (dm) {
      var d2 = new Date(now.getFullYear(), parseInt(dm[2], 10) - 1, parseInt(dm[1], 10));
      if (d2 < startOfDay(now)) d2.setFullYear(d2.getFullYear() + 1);
      return d2;
    }
    return null;
  }

  function extractTime(text) {
    var t = text.toLowerCase();
    var m = t.match(/\b(\d{1,2})[:.](\d{2})\s*(am|pm)?/);
    if (m) {
      var h = parseInt(m[1], 10), min = parseInt(m[2], 10);
      if (m[3] === 'pm' && h < 12) h += 12;
      if (m[3] === 'am' && h === 12) h = 0;
      return { h: h, m: min };
    }
    m = t.match(/\b(\d{1,2})\s*(am|pm)\b/);
    if (m) {
      var h2 = parseInt(m[1], 10);
      if (m[2] === 'pm' && h2 < 12) h2 += 12;
      if (m[2] === 'am' && h2 === 12) h2 = 0;
      return { h: h2, m: 0 };
    }
    m = t.match(/\b(?:at|by|around|ssaawa|saa)\s+(\d{1,2})\b/);
    if (m) {
      var h3 = parseInt(m[1], 10);
      if (h3 >= 1 && h3 <= 7) h3 += 12; /* "at 2" in a working day means 14:00 */
      return { h: h3, m: 0 };
    }
    return null;
  }

  function extractService(text) {
    var t = text.toLowerCase();
    var services = VoiceCore.config.services || [];
    var hit = null;
    services.forEach(function (s) {
      if (hit) return;
      var words = s.name.toLowerCase().split(/\s+/);
      var matched = words.some(function (w) { return w.length > 3 && t.indexOf(w) !== -1; });
      if (matched) hit = s;
    });
    return hit;
  }

  function extractName(text) {
    var t = text.trim();
    var m = t.match(/(?:my name is|i am|i'm|this is|erinnya lyange|jina langu ni)\s+([a-z' ]{2,40})/i);
    if (m) return titleCase(m[1].trim());
    /* A short bare reply to "may I have your name" is the name itself. */
    if (/^[a-z' ]{2,40}$/i.test(t) && t.split(/\s+/).length <= 4) return titleCase(t);
    return null;
  }

  function titleCase(s) {
    return s.replace(/\w\S*/g, function (w) {
      return w.charAt(0).toUpperCase() + w.slice(1).toLowerCase();
    });
  }

  function startOfDay(d) {
    var x = new Date(d.getTime());
    x.setHours(0, 0, 0, 0);
    return x;
  }

  /* ---------------------------------------------------------------------
     5. Opening hours
     --------------------------------------------------------------------- */
  function hoursFor(date) {
    var key = DAY_KEYS[date.getDay()];
    return VoiceCore.config.hours[key] || null;
  }

  function isOpenAt(date, time) {
    var h = hoursFor(date);
    if (!h) return false;
    var mins = time.h * 60 + time.m;
    return mins >= h[0] * 60 && mins < h[1] * 60;
  }

  function nextOpenSlot(fromDate, time) {
    var d = startOfDay(fromDate);
    for (var i = 0; i < 14; i++) {
      var h = hoursFor(d);
      if (h) {
        var candidate = time && i === 0 ? Math.max(time.h, h[0]) : h[0];
        if (candidate < h[1]) return { date: new Date(d.getTime()), time: { h: candidate, m: 0 } };
      }
      d.setDate(d.getDate() + 1);
    }
    return null;
  }

  function formatHours() {
    var cfg = VoiceCore.config.hours;
    var parts = [];
    DAY_KEYS.forEach(function (k, i) {
      var h = cfg[k];
      parts.push(DAY_NAMES[i].slice(0, 3) + ' ' + (h ? pad(h[0]) + ':00–' + pad(h[1]) + ':00' : 'closed'));
    });
    return parts.join(', ');
  }

  function pad(n) { return (n < 10 ? '0' : '') + n; }

  function formatDate(d) {
    return DAY_NAMES[d.getDay()] + ' ' + d.getDate() + ' ' +
      ['January','February','March','April','May','June','July','August','September','October','November','December'][d.getMonth()];
  }

  function formatTime(t) { return pad(t.h) + ':' + pad(t.m); }

  VoiceCore.format = { date: formatDate, time: formatTime, hours: formatHours };
  VoiceCore.hours = { isOpenAt: isOpenAt, nextOpenSlot: nextOpenSlot, hoursFor: hoursFor };

  /* ---------------------------------------------------------------------
     6. Storage — conversations, bookings, leads
     --------------------------------------------------------------------- */
  var KEY = 'voicecore.store.v1';
  var listeners = [];

  function blank() {
    return { conversations: [], bookings: [], leads: [], updated: Date.now() };
  }

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return blank();
      var parsed = JSON.parse(raw);
      return parsed && parsed.conversations ? parsed : blank();
    } catch (e) {
      return blank();
    }
  }

  function write(data) {
    data.updated = Date.now();
    try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) { /* private mode */ }
    listeners.forEach(function (fn) { try { fn(data); } catch (e) {} });
    return data;
  }

  var Store = {
    all: read,
    reset: function () { return write(blank()); },
    onChange: function (fn) { listeners.push(fn); return function () {
      listeners = listeners.filter(function (f) { return f !== fn; });
    }; },

    /* One memory across phone, WhatsApp and web chat: a conversation is keyed
       by contact where we have one, and only falls back to session id. */
    openConversation: function (channel, sessionId, contact) {
      var data = read();
      var found = null;
      if (contact) {
        found = data.conversations.filter(function (c) {
          return c.contact === contact && Date.now() - c.updated < 1000 * 60 * 60 * 24 * 30;
        }).pop();
      }
      if (!found) {
        found = data.conversations.filter(function (c) { return c.sessionId === sessionId; }).pop();
      }
      if (!found) {
        found = {
          id: 'c' + Date.now() + Math.random().toString(36).slice(2, 6),
          sessionId: sessionId,
          channel: channel,
          channels: [channel],
          contact: contact || null,
          name: null,
          tag: 'question',
          urgent: false,
          messages: [],
          started: Date.now(),
          updated: Date.now(),
          handedOff: false
        };
        data.conversations.push(found);
        write(data);
      } else if (found.channels.indexOf(channel) === -1) {
        found.channels.push(channel);
        found.channel = channel;
        write(data);
      }
      return found.id;
    },

    append: function (conversationId, message) {
      var data = read();
      data.conversations.forEach(function (c) {
        if (c.id !== conversationId) return;
        c.messages.push(message);
        c.updated = Date.now();
      });
      return write(data);
    },

    /* Tags only ever escalate. A customer who books and then asks a price is
       still a booking, not a lead; a complaint outranks everything. */
    tagRank: { question: 0, lead: 1, booking: 2, complaint: 3 },

    patchConversation: function (conversationId, patch) {
      var data = read();
      var rank = Store.tagRank;
      data.conversations.forEach(function (c) {
        if (c.id !== conversationId) return;
        Object.keys(patch).forEach(function (k) {
          if (k === 'tag') {
            var next = rank[patch.tag] == null ? 0 : rank[patch.tag];
            var curr = rank[c.tag] == null ? 0 : rank[c.tag];
            if (next <= curr) return;
          }
          if (patch[k] === null || patch[k] === undefined) return;
          c[k] = patch[k];
        });
        c.updated = Date.now();
      });
      return write(data);
    },

    get: function (conversationId) {
      return read().conversations.filter(function (c) { return c.id === conversationId; })[0] || null;
    },

    addBooking: function (booking) {
      var data = read();
      booking.id = 'b' + Date.now() + Math.random().toString(36).slice(2, 5);
      booking.created = Date.now();
      data.bookings.push(booking);
      return write(data);
    },

    addLead: function (lead) {
      var data = read();
      lead.id = 'l' + Date.now() + Math.random().toString(36).slice(2, 5);
      lead.created = Date.now();
      data.leads.push(lead);
      return write(data);
    }
  };

  VoiceCore.store = Store;

  /* ---------------------------------------------------------------------
     7. Brain — one turn of conversation
     --------------------------------------------------------------------- */
  function Session(channel, sessionId, contact) {
    this.channel = channel;
    this.sessionId = sessionId || 's' + Math.random().toString(36).slice(2, 10);
    this.lang = 'en';
    this.slots = { service: null, date: null, time: null, name: null, phone: contact || null };
    this.flow = null;          /* 'booking' while collecting slots */
    this.conversationId = Store.openConversation(channel, this.sessionId, contact || null);
    this.turns = 0;
  }

  Session.prototype.say = function (text, meta) {
    Store.append(this.conversationId, {
      role: 'agent', text: text, at: Date.now(), meta: meta || null
    });
    return text;
  };

  Session.prototype.hear = function (text) {
    Store.append(this.conversationId, { role: 'customer', text: text, at: Date.now() });
  };

  Session.prototype.greeting = function () {
    var t = LANG[this.lang];
    var open = this.isOpenNow();
    var text = t.greet(VoiceCore.config);
    if (!open) {
      text += ' ' + (this.lang === 'en'
        ? 'We are closed right now, but I can take a booking or a message. ' + VoiceCore.config.afterHoursPromise
        : t.closed);
    }
    return this.say(text);
  };

  Session.prototype.isOpenNow = function () {
    var now = new Date();
    return isOpenAt(now, { h: now.getHours(), m: now.getMinutes() });
  };

  Session.prototype.nextMissingSlot = function () {
    if (!this.slots.service) return 'service';
    if (!this.slots.date) return 'date';
    if (!this.slots.time) return 'time';
    if (!this.slots.name) return 'name';
    if (!this.slots.phone) return 'phone';
    return null;
  };

  Session.prototype.absorb = function (text) {
    var s = this.slots;
    var svc = extractService(text); if (svc) s.service = svc;
    var day = extractDay(text); if (day) s.date = day;
    var time = extractTime(text); if (time) s.time = time;
    var phone = extractPhone(text); if (phone) s.phone = phone;
    if (!s.name && this.flow === 'booking' && this.awaiting === 'name') {
      var nm = extractName(text); if (nm) s.name = nm;
    } else if (!s.name) {
      var nm2 = text.match(/(?:my name is|i am|i'm|this is)\s+([a-z' ]{2,40})/i);
      if (nm2) s.name = titleCase(nm2[1].trim());
    }
  };

  Session.prototype.askFor = function (slot) {
    var t = LANG[this.lang];
    this.awaiting = slot;
    if (slot === 'service') {
      var names = (VoiceCore.config.services || []).map(function (s) { return s.name; });
      return this.say(t.askService + ' ' + t.servicesIntro + names.join(', ') + '.',
        { quick: names });
    }
    if (slot === 'date') return this.say(t.askDay, { quick: ['Today', 'Tomorrow', 'This week'] });
    if (slot === 'time') return this.say(t.askTime, { quick: ['09:00', '11:00', '14:00', '16:00'] });
    if (slot === 'name') return this.say(t.askName);
    if (slot === 'phone') return this.say(t.askPhone);
    return this.say(t.unknown);
  };

  Session.prototype.completeBooking = function () {
    var t = LANG[this.lang];
    var s = this.slots;
    var cfg = VoiceCore.config;

    if (!isOpenAt(s.date, s.time)) {
      var next = nextOpenSlot(s.date, s.time);
      if (next) {
        s.date = next.date;
        s.time = next.time;
        var msg = t.closed + t.offer + formatDate(s.date) + ' at ' + formatTime(s.time) + '.';
        this.awaiting = 'confirm';
        this.flow = 'confirm';
        return this.say(msg, { quick: ['Yes, book it', 'Another time'] });
      }
    }

    Store.addBooking({
      conversationId: this.conversationId,
      name: s.name,
      phone: s.phone,
      service: s.service ? s.service.name : 'Consultation',
      minutes: s.service ? s.service.minutes : 30,
      price: s.service ? s.service.price : null,
      when: s.date.getTime() + (s.time.h * 60 + s.time.m) * 60000,
      channel: this.channel
    });
    Store.patchConversation(this.conversationId, {
      tag: 'booking', name: s.name, contact: s.phone
    });

    this.flow = null;
    this.awaiting = null;

    var line = t.confirmed + (s.service ? s.service.name : 'Appointment') + ' — ' +
      formatDate(s.date) + ' at ' + formatTime(s.time) +
      (s.name ? ', for ' + s.name : '') + '. ' + t.summarySent;
    if (s.service && s.service.price) line += ' (' + s.service.price + ')';
    var reset = this.slots;
    this.slots = { service: null, date: null, time: null, name: reset.name, phone: reset.phone };
    return this.say(line, { booking: true });
  };

  Session.prototype.reply = function (text) {
    this.turns++;
    this.hear(text);
    this.lang = detectLanguage(text, this.lang);
    var t = LANG[this.lang];
    var intent = detectIntent(text);
    this.absorb(text);

    /* Mid-flow: confirming a moved slot */
    if (this.flow === 'confirm') {
      if (intent.name === 'affirm') { this.flow = 'booking'; return this.completeBooking(); }
      if (intent.name === 'deny') {
        this.flow = 'booking';
        this.slots.date = null; this.slots.time = null;
        return this.askFor('date');
      }
    }

    /* Escalation always wins */
    if (intent.name === 'complaint') {
      Store.patchConversation(this.conversationId, { tag: 'complaint', urgent: true });
      return this.say(t.complaint + ' ' + t.handoff + VoiceCore.config.handoffNumber + '.' + t.handoffCtx,
        { urgent: true });
    }
    if (intent.name === 'human') {
      Store.patchConversation(this.conversationId, { handedOff: true });
      return this.say(t.handoff + VoiceCore.config.handoffNumber + '.' + t.handoffCtx, { handoff: true });
    }

    /* Booking flow */
    if (intent.name === 'booking' || this.flow === 'booking') {
      this.flow = 'booking';
      Store.patchConversation(this.conversationId, { tag: 'booking' });
      var missing = this.nextMissingSlot();
      if (missing) return this.askFor(missing);
      return this.completeBooking();
    }

    /* Informational answers, straight from the config — never invented */
    if (intent.name === 'price') {
      var lines = (VoiceCore.config.services || []).map(function (s) {
        return s.name + ' ' + (s.price || 'on request');
      });
      Store.patchConversation(this.conversationId, { tag: 'lead' });
      return this.say(t.priceIntro + lines.join('; ') + '.', { quick: ['Book one', 'Your hours?'] });
    }
    if (intent.name === 'hours') {
      return this.say(t.hoursIntro + formatHours() + '.', { quick: ['Book a time'] });
    }
    if (intent.name === 'location') {
      return this.say(t.locationIntro + VoiceCore.config.location + '.', { quick: ['Book a time'] });
    }
    if (intent.name === 'services') {
      var names = (VoiceCore.config.services || []).map(function (s) { return s.name; });
      return this.say(t.servicesIntro + names.join(', ') + '.', { quick: names.slice(0, 3) });
    }
    if (intent.name === 'greeting') return this.greeting();
    if (intent.name === 'thanks') return this.say(t.thanks);
    if (intent.name === 'bye') {
      return this.say(this.lang === 'en'
        ? 'Thank you for calling ' + VoiceCore.config.business + '. Goodbye.'
        : t.bye);
    }

    /* Unknown: capture the lead rather than lose it, then hand off honestly. */
    Store.patchConversation(this.conversationId, { tag: 'lead' });
    if (this.slots.phone || this.slots.name) {
      Store.addLead({
        conversationId: this.conversationId,
        name: this.slots.name, phone: this.slots.phone,
        note: text, channel: this.channel
      });
    }
    return this.say(t.unknown, { handoff: true });
  };

  VoiceCore.Session = Session;
  VoiceCore.detectIntent = detectIntent;
  VoiceCore.detectLanguage = detectLanguage;

  /* ---------------------------------------------------------------------
     8. Voice of the Customer brief — the monthly one-pager, generated
     --------------------------------------------------------------------- */
  VoiceCore.voiceOfCustomer = function () {
    var data = Store.all();
    var convs = data.conversations;
    var byTag = { booking: 0, lead: 0, complaint: 0, question: 0 };
    convs.forEach(function (c) { byTag[c.tag] = (byTag[c.tag] || 0) + 1; });

    var afterHours = convs.filter(function (c) {
      var d = new Date(c.started);
      return !isOpenAt(d, { h: d.getHours(), m: d.getMinutes() });
    }).length;

    var handoffs = convs.filter(function (c) { return c.handedOff; }).length;
    var urgent = convs.filter(function (c) { return c.urgent; });

    /* Themes: what customers actually asked about, counted from real turns. */
    var themes = {};
    convs.forEach(function (c) {
      c.messages.filter(function (m) { return m.role === 'customer'; }).forEach(function (m) {
        var i = detectIntent(m.text);
        if (i.name !== 'unknown' && i.name !== 'affirm' && i.name !== 'deny' && i.name !== 'greeting') {
          themes[i.name] = (themes[i.name] || 0) + 1;
        }
      });
    });
    var ranked = Object.keys(themes).map(function (k) { return { theme: k, count: themes[k] }; })
      .sort(function (a, b) { return b.count - a.count; });

    var missed = convs.filter(function (c) {
      return c.tag === 'lead' && !data.bookings.some(function (b) { return b.conversationId === c.id; });
    }).length;

    return {
      conversations: convs.length,
      bookings: data.bookings.length,
      leads: data.leads.length,
      byTag: byTag,
      afterHours: afterHours,
      afterHoursShare: convs.length ? Math.round(afterHours / convs.length * 100) : 0,
      handoffs: handoffs,
      urgent: urgent,
      themes: ranked,
      missedOpportunities: missed,
      generated: Date.now()
    };
  };

  /* ---------------------------------------------------------------------
     9. Config persistence — the dashboard writes it, every page reads it
     --------------------------------------------------------------------- */
  var CFG_KEY = 'voicecore.config.v1';

  VoiceCore.saveConfig = function () {
    try { localStorage.setItem(CFG_KEY, JSON.stringify(VoiceCore.config)); } catch (e) {}
    return VoiceCore.config;
  };

  VoiceCore.loadConfig = function () {
    try {
      var raw = localStorage.getItem(CFG_KEY);
      if (raw) {
        var saved = JSON.parse(raw);
        Object.keys(VoiceCore.defaultConfig).forEach(function (k) {
          if (saved[k] !== undefined) VoiceCore.config[k] = saved[k];
        });
      }
    } catch (e) {}
    return VoiceCore.config;
  };

  VoiceCore.loadConfig();

  global.VoiceCore = VoiceCore;
})(window);
