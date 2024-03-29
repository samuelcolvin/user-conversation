
function WebSocketConnection(){
  if (!('WebSocket' in window)) {
    alert('WebSockets are not supported by your browser.');
    return;
  }

  log('connecting...');
  var ws = new WebSocket(django_vars.ws_url);

  ws.onopen = function(){
    log('connected');mkd
    ws.send('sending message on websocket opening');
  };

  ws.onmessage = function (evt) {
    log('received: ' + evt.data);
  };

  ws.onclose = function (evt) {
    log('Connection closed');
  };

  $('#user-input').submit(function (e){
    e.preventDefault();
    var msg = $('#message-box').val();
    log('sending: '+ msg);
    ws.send(msg);
  });
}

var $console = $('#console');

function log(message){
  $console.append(message + '\n');
  console.log(message)
}

$(document).ready(function(){WebSocketConnection()});
