import React, { Component } from 'react';
import { Input, Button } from 'reactstrap';
import './ConversationContent.css'

class ConversationContent extends Component {
  constructor (props) {
    super(props);
    this.state = {
      messages: [],
      count: 5,
      conversation: null,
      myId: null,
    }
  }

  syncMessages = (conversationId) => {
    const { count } = this.state;
    fetch(`http://localhost:8081/conversation/${conversationId}/${count}`, {
      method: 'GET',
      headers: { 'Authorization': "Bearer " + localStorage.getItem('token') }
    })
      .then(r => r.json())
      .then((data) => {
        console.log(data);
        this.setState({conversation: data})
        // console.log(data)
      })
  }

  sendMessage = () => {
    
  }

  renderMessages = () => {
    const { conversation, count } = this.state;
    return (
      <React.Fragment>
        {conversation.messages.map((m,index) => <div key={index}>{m.text}</div>)}
        {conversation.messages.length < count ? null : <Button>Load more</Button>}
      </React.Fragment>
    )
  }

  render() {
    const { conversation } = this.state;
    return (
      <div id="conversation-content">
        {conversation ? (
          <React.Fragment>
            <Input placeholder="Write here" />
            <Button onClick={this.sendMessage}>Send</Button>
          </React.Fragment>
        ) : null}
        <div className="conversation-body">
          {conversation ? this.renderMessages() : null}
        </div>
      </div>
    )
  }
}

export default ConversationContent;