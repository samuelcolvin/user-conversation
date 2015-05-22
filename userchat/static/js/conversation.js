function WebsocketWrapper(){
  if (!('WebSocket' in window)) {
    alert('WebSockets are not supported by your browser.');
  }

  console.log('connecting...');
  var conn = new WebSocket(django_vars.ws_url);

  conn.onopen = function(){
    console.log('connected');
    ws.send('join', JSON.stringify(django_vars));
  };

  this.send = function(action, data){
    conn.send(action + ':' + data);
  };

  function Actions(){
    this.msgs = function(operator, messages){
      console.log('on_msgs:', operator, messages, 'nothing attached');
    };
  };
  this.actions = new Actions();

  conn.onmessage = function(evt){
    var action = evt.data.split(':', 1)[0];
    var operator = evt.data.substr(action.length + 1, 1);
    var text = evt.data.substr(action.length + 2);
    console.log(action, operator, text);
    ws.actions[action](operator, text);
  };

  conn.onclose = function () {
    console.log('Connection closed');
  };
}

var ws;

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
    var messageNodes = this.props.data.map(function (message, i) {
      return (
        <Message author={message.author} key={i}>
          {message.text}
        </Message>
      );
    });
    var style = {height: ($(window).height() - 150) + 'px'};
    return (
      <div className="message-list" style={style}>
        {messageNodes}
      </div>
    );
  }
});

var MessageForm = React.createClass({
  handleSubmit: function(e) {
    e.preventDefault();
    var text = React.findDOMNode(this.refs.text).value.trim();
    if (!text) {
      return;
    }
    console.log(text)
    ws.send('msg', text);
    React.findDOMNode(this.refs.text).value = '';
  },
  render: function() {
    return (
      <form className="message-form" onSubmit={this.handleSubmit}>
        <div className="input-group">
          <input type="text" className="form-control" ref="text" placeholder="ask away..."/>
          <span className="input-group-btn">
            <button className="btn btn-default" type="button">
                &nbsp;<span className="glyphicon glyphicon-send"></span>&nbsp;
            </button>
          </span>
        </div>
      </form>
    );
  }
});

var Conversation = React.createClass({
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    ws = new WebsocketWrapper();
    ws.actions.msgs = function(operator, text) {
      messages = JSON.parse(text);
      if (operator === '+'){
        Array.prototype.push.apply(this.state.data, messages);
      } else{
        this.state.data = messages;
      }

      this.setState({data: this.state.data});
    }.bind(this);
  },
  render: function() {
    return (
      <div className="Conversation">
        <MessageList data={this.state.data} />
        <MessageForm />
      </div>
    );
  }
});

React.render(
  <Conversation />,
  document.getElementById('conversation')
);
