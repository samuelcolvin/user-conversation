
function WebSocketConnection(){
  if (!('WebSocket' in window)) {
    alert('WebSockets are not supported by your browser.');
    return;
  }

  log('connecting...');
  var ws_url = $('#ws_url').data('value');
  var stream = 123; // parseInt($('#stream-ref').data('value'));
  var ws = new WebSocket(ws_url);

  ws.onopen = function(){
    log('connected');
    ws.send('get_all:' + stream);
  };

  ws.onmessage = function (evt) {
    log('received: ' + evt.data);
  };

  ws.onclose = function () {
    log('Connection closed');
  };

  function send_message(){
    var msg = 'new_action:' + JSON.stringify({
      author: $('#author-input').val(),
      message: $('#message-input').val(),
      stream: stream
    });
    log('sending: '+ msg);
    ws.send(msg);
  }

  $('#send-msg').click(send_message);
}

var $console = $('#console');

function log(message){
  $console.prepend(message + '\n');
}

$(document).ready(function(){WebSocketConnection()});
