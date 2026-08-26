/* OCG Financial — sitewide behavior */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Header scroll state */
  var header = document.getElementById('siteHeader');
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 40); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* Mobile menu */
  var burger = document.getElementById('burger');
  var mobileMenu = document.getElementById('mobileMenu');
  if (burger && mobileMenu) {
    burger.addEventListener('click', function () {
      var open = mobileMenu.classList.toggle('open');
      burger.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    mobileMenu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        burger.classList.remove('open');
        mobileMenu.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
    /* Mobile submenu accordions */
    mobileMenu.querySelectorAll('.m-group').forEach(function (group) {
      var btn = group.querySelector('.m-group-btn');
      var sub = group.querySelector('.m-sub');
      if (!btn || !sub) return;
      btn.addEventListener('click', function () {
        var open = group.classList.toggle('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        sub.style.maxHeight = open ? sub.scrollHeight + 'px' : '0px';
      });
    });
  }

  /* Desktop dropdowns: click/tap + keyboard support (hover handled in CSS) */
  document.querySelectorAll('.has-drop').forEach(function (li) {
    var btn = li.querySelector('.nav-drop-btn');
    if (!btn) return;
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var open = li.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.querySelectorAll('.has-drop.open').forEach(function (other) {
        if (other !== li) {
          other.classList.remove('open');
          var ob = other.querySelector('.nav-drop-btn');
          if (ob) ob.setAttribute('aria-expanded', 'false');
        }
      });
    });
    li.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        li.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.has-drop')) {
      document.querySelectorAll('.has-drop.open').forEach(function (li) {
        li.classList.remove('open');
        var b = li.querySelector('.nav-drop-btn');
        if (b) b.setAttribute('aria-expanded', 'false');
      });
    }
  });

  /* Scroll reveal */
  var revealEls = document.querySelectorAll('.reveal, .process-step, .sec-divider, .founder-photo, .journey');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* Animated counters */
  var counters = document.querySelectorAll('[data-count-to]');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var countIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var target = parseFloat(el.dataset.countTo);
        var prefix = el.dataset.prefix || '';
        var suffix = el.dataset.suffix || '';
        var decimals = el.dataset.countTo.indexOf('.') !== -1 ? 1 : 0;
        var duration = 1300;
        var start = performance.now();
        (function tick(now) {
          var p = Math.min((now - start) / duration, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = prefix + (target * eased).toFixed(decimals) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        })(performance.now());
        countIO.unobserve(el);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { countIO.observe(el); });
  } else {
    counters.forEach(function (el) {
      el.textContent = (el.dataset.prefix || '') + el.dataset.countTo + (el.dataset.suffix || '');
    });
  }

  /* Hero parallax (desktop only) */
  var consoleWrap = document.querySelector('.console-wrap');
  var hero = document.querySelector('.hero');
  if (consoleWrap && hero && !reduceMotion && window.matchMedia('(min-width:980px)').matches) {
    hero.addEventListener('mousemove', function (e) {
      var rect = hero.getBoundingClientRect();
      var x = (e.clientX - rect.left) / rect.width - 0.5;
      var y = (e.clientY - rect.top) / rect.height - 0.5;
      consoleWrap.style.transform = 'translate(' + (x * 8) + 'px, ' + (y * 8) + 'px)';
    });
  }

  /* Featured video: the Wistia player is only fetched once someone clicks,
     so the page carries a poster image rather than a third-party player. */
  document.querySelectorAll('.vf-player[data-wistia]').forEach(function (wrap) {
    var poster = wrap.querySelector('.vf-poster');
    if (!poster) return;
    /* If the poster image ever stops resolving, fall back to the panel
       gradient rather than a broken-image icon. */
    var thumb = poster.querySelector('img');
    if (thumb) {
      thumb.addEventListener('error', function () { thumb.style.display = 'none'; });
    }
    poster.addEventListener('click', function () {
      var frame = document.createElement('iframe');
      frame.className = 'vf-frame';
      frame.src = 'https://fast.wistia.net/embed/iframe/' +
        encodeURIComponent(wrap.getAttribute('data-wistia')) +
        '?autoPlay=true&playerColor=d9b355';
      frame.title = poster.getAttribute('data-title') || 'Video';
      frame.setAttribute('allow', 'autoplay; fullscreen');
      frame.setAttribute('allowfullscreen', '');
      frame.setAttribute('frameborder', '0');
      wrap.appendChild(frame);
      poster.remove();
    });
  });

  /* Tax news cards, fetched from the aggregator function.

     Feed content is third-party text: every value is written with
     textContent or setAttribute, never innerHTML, so a hostile title or
     excerpt cannot inject markup into the page. */
  var newsLists = document.querySelectorAll('.news-list');
  if (newsLists.length) {
    (function () {
      var endpoint = newsLists[0].getAttribute('data-endpoint') || '/api/tax-news';

      var setStatus = function (list, message) {
        list.setAttribute('aria-busy', 'false');
        list.textContent = '';
        var p = document.createElement('p');
        p.className = 'news-status';
        p.textContent = message;
        list.appendChild(p);
      };

      var formatDate = function (iso) {
        if (!iso) return '';
        var d = new Date(iso);
        if (isNaN(d.getTime())) return '';
        try {
          return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        } catch (e) {
          return d.toISOString().slice(0, 10);
        }
      };

      var card = function (item) {
        var a = document.createElement('a');
        a.className = 'news-card';
        a.href = item.link;
        a.target = '_blank';
        a.rel = 'noopener noreferrer';

        var meta = document.createElement('div');
        meta.className = 'news-meta';
        var src = document.createElement('span');
        src.className = 'news-source';
        src.textContent = item.source || '';
        meta.appendChild(src);
        var when = formatDate(item.date);
        if (when) {
          var sep = document.createElement('span');
          sep.className = 'news-sep';
          sep.textContent = '·';
          var time = document.createElement('time');
          time.className = 'news-date';
          time.setAttribute('datetime', item.date);
          time.textContent = when;
          meta.appendChild(sep);
          meta.appendChild(time);
        }
        a.appendChild(meta);

        var h = document.createElement('h3');
        h.className = 'news-title';
        h.textContent = item.title || '';
        a.appendChild(h);

        if (item.excerpt) {
          var p = document.createElement('p');
          p.className = 'news-excerpt';
          p.textContent = item.excerpt;
          a.appendChild(p);
        }

        var more = document.createElement('span');
        more.className = 'news-more';
        more.textContent = 'Read more →';
        a.appendChild(more);
        return a;
      };

      var render = function (items) {
        newsLists.forEach(function (list) {
          if (!items.length) {
            setStatus(list, 'Headlines are unavailable right now. Please check back shortly.');
            return;
          }
          var limit = parseInt(list.getAttribute('data-limit'), 10) || items.length;
          var frag = document.createDocumentFragment();
          items.slice(0, limit).forEach(function (item) { frag.appendChild(card(item)); });
          list.setAttribute('aria-busy', 'false');
          list.textContent = '';
          list.appendChild(frag);
        });
      };

      if (typeof fetch !== 'function') {
        newsLists.forEach(function (l) { setStatus(l, 'Headlines are unavailable right now. Please check back shortly.'); });
        return;
      }

      fetch(endpoint, { headers: { Accept: 'application/json' } })
        .then(function (res) {
          if (!res.ok) throw new Error(res.status);
          return res.json();
        })
        .then(function (data) { render((data && data.items) || []); })
        .catch(function () { render([]); });
    })();
  }

  /* Footer year */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
