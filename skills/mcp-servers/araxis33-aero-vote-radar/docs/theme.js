/* deftools light/dark, 31.10.2026. Loaded in <head> without defer: it sets the theme
   before the first paint, so a dark-mode visitor never sees a white flash. The page
   follows the device until the visitor picks one with the header button; the pick is
   kept per browser. The button is added here so no page has to carry its markup. */
(function () {
  var KEY = 'deftools-theme';
  var root = document.documentElement;
  var pick = null;
  try { pick = localStorage.getItem(KEY); } catch (e) {}
  if (pick !== 'light' && pick !== 'dark') pick = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  root.dataset.theme = pick;

  function paintMeta() {
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = root.dataset.theme === 'dark' ? '#10131b' : '#eff1f4';
  }

  function addButton() {
    var host = document.querySelector('header .wrap') || document.querySelector('header');
    if (!host || document.getElementById('theme-btn')) return;
    var b = document.createElement('button');
    b.type = 'button'; b.id = 'theme-btn'; b.className = 'theme-btn';
    function show() {
      var dark = root.dataset.theme === 'dark';
      b.textContent = dark ? 'Light' : 'Dark';
      b.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      paintMeta();
    }
    b.addEventListener('click', function () {
      root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(KEY, root.dataset.theme); } catch (e) {}
      show();
    });
    var nav = host.querySelector('nav');
    if (nav) nav.parentNode.insertBefore(b, nav.nextSibling); else host.appendChild(b);
    show();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', addButton);
  else addButton();
})();
