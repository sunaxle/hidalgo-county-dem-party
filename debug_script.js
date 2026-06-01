window.onerror = function(msg, url, lineNo, columnNo, error) {
  fetch('http://localhost:8003/log', {
    method: 'POST',
    mode: 'no-cors',
    body: JSON.stringify({msg, url, lineNo, columnNo, error: error ? error.stack : ''})
  });
  return false;
};
window.addEventListener('unhandledrejection', function(event) {
  fetch('http://localhost:8003/log', {
    method: 'POST',
    mode: 'no-cors',
    body: JSON.stringify({msg: 'Promise rejection: ' + event.reason})
  });
});
console.log("DEBUG SCRIPT LOADED");
fetch('http://localhost:8003/log', { method: 'POST', mode: 'no-cors', body: 'DEBUG SCRIPT ACTIVE' });
