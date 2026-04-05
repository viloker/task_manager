/* Theme toggle — light / dark
   Applied before paint to avoid flash of wrong theme. */
(function () {
  var KEY = 'tm:theme';
  var html = document.documentElement;

  var ICONS = {
    /* shown when current theme is DARK (click → go light) */
    dark: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>',
    /* shown when current theme is LIGHT (click → go dark) */
    light: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
  };

  function getPreferred() {
    var stored = localStorage.getItem(KEY);
    if (stored === 'dark' || stored === 'light') return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    html.dataset.theme = theme;
    localStorage.setItem(KEY, theme);
    updateBtn(theme);
  }

  function updateBtn(theme) {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    /* icon shows what you'll switch TO */
    btn.innerHTML = theme === 'dark' ? ICONS.dark : ICONS.light;
    btn.title = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
  }

  /* Apply immediately — before DOMContentLoaded */
  applyTheme(getPreferred());

  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    updateBtn(html.dataset.theme);
    btn.addEventListener('click', function () {
      applyTheme(html.dataset.theme === 'dark' ? 'light' : 'dark');
    });
  });
})();