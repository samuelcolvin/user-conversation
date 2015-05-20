if (!('WebSocket' in window)) {
  alert('WebSockets are not supported by your browser.');
}

var Message = React.createClass({
  render: function() {
    var rawMarkup = marked(this.props.children.toString(), {sanitize: true});
    return (
      <div className="message">
        <h2 className="messageAuthor">
          {this.props.author}
        </h2>
        <span dangerouslySetInnerHTML={{__html: rawMarkup}} />
      </div>
    );
  }
});

var MessageList = React.createClass({
  render: function() {
    var messageNodes = this.props.data.map(function (message) {
      return (
        <Message author={message.author}>
          {message.text}
        </Message>
      );
    });
    return (
      <div className="messageList">
        {messageNodes}
      </div>
    );
  }
});

var Conversation = React.createClass({
  getInitialState: function() {
    return {data: []};
  },
  //componentDidMount: function() {
  //    this.loadMessagesFromServer();
  //    setInterval(this.loadCommentsFromServer, this.props.pollInterval);
  //
  //    console.log('connecting...');
  //    var ws_url = $('#ws_url').data('value');
  //    var ws = new WebSocket(ws_url);
  //
  //    ws.onopen = function(){
  //      log('connected');
  //      ws.send('get_all:' + stream);
  //    };
  //
  //    ws.onmessage = function (evt) {
  //      log('received: ' + evt.data);
  //    };
  //
  //    ws.onclose = function () {
  //      log('Connection closed');
  //    };
  //
  //    function send_message(){
  //      var msg = 'new_action:' + JSON.stringify({
  //        author: $('#author-input').val(),
  //        message: $('#message-input').val(),
  //        stream: stream
  //      });
  //      log('sending: '+ msg);
  //      ws.send(msg);
  //    }
  //    $('#send-msg').click(send_message);
  //  }
  //},
  render: function() {
    return (
      <div className="Conversation">
        <MessageList data={this.props.data} />
      </div>
    );
  }
});

var data = [
  {author: "Pete Hunt", text: "This is one comment"},
  {author: "Jordan Walke", text: "This is *another* comment"}
];

React.render(
  <Conversation data={data} />,
  document.getElementById('conversation')
);
