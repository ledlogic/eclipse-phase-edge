/* ep-daymode.js — Eclipse Phase campaign day/dark mode toggle
   Requires jQuery (already loaded on all session pages via cdnjs). */

(function ($) {
  var KEY = 'ep-day-mode';

  function apply(on) {
    $('body').toggleClass('day-mode', on);
    $('#day-toggle-btn').text(on ? '◈ DARK MODE' : '◈ DAY MODE');
  }

  // Inject a flash-prevention <style> into <head> before body renders
  // so the page doesn't briefly flash dark when day mode is saved.
  if (localStorage.getItem(KEY) === 'true') {
    $('<style id="ep-day-flash">body{--void:#f0f2f5!important;--deep:#e8ecf4!important;--panel:#e0e5ef!important;--border:#c0cad8!important;--accent:#b06000!important;--accent2:#007a6b!important;--warn:#8a5a00!important;--muted:#5a6878!important;--text:#1a2530!important;--textbright:#080f18!important;background:#f0f2f5!important;color:#1a2530!important;}</style>')
      .appendTo('head');
  }

  $(function () {
    // Apply class and remove the flash-prevention stub
    apply(localStorage.getItem(KEY) === 'true');
    $('#ep-day-flash').remove();

    $('#day-toggle-btn').on('click', function () {
      var on = !$('body').hasClass('day-mode');
      apply(on);
      localStorage.setItem(KEY, on);
    });
  });

}(jQuery));
