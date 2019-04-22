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
      conversationId: null,
      text: '',
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
        console.log(data)
        this.setState({
          conversation: data,
          conversationId: conversationId
        })
      })
  }

  sendMessage = () => {
    const { conversation, text, myId } = this.state;
    const body = JSON.stringify({
      conversation_id: conversation.id,
      receiver_id: myId == conversation.creator_id ? conversation.creator_id : conversation.participant_id,
      text,
    });
    fetch(`http://localhost:8081/message`, {
      method: 'POST',
      headers:{ 
        'Authorization': "Bearer " + localStorage.getItem('token'),
        'Content-Type': 'application/json',
      },
      body,
    })
      .then((r) => {
        this.setState({text: ''})
        this.syncMessages(conversation.id)
      })
  }

  onChangeInput = (event) => {
    this.setState({ text: event.target.value })
  }

  renderMessages = () => {
    const { conversation, count } = this.state;
    return (
      <React.Fragment>
        {conversation.messages.map((m, index) => <div key={index}>{m.text}</div>)}
        {conversation.messages.length < count ? null : <Button>Load more</Button>}
      </React.Fragment>
    )
  }

  render() {
    const { conversation, text } = this.state;
    return (
      <div id="conversation-content">
        {conversation ? (
          <React.Fragment>
            <Input placeholder="Write here" onChange={this.onChangeInput} value={text} />
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