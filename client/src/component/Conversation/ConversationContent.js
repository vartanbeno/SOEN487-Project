import React, { Component } from 'react';
import { Input, Button } from 'reactstrap';
import './ConversationContent.css'

class ConversationContent extends Component {
  constructor (props) {
    super(props);
    this.state = {
      messages: [],
      count: 0,
      conversation: null
    }
  }

  componentDidMount() {
    console.log(localStorage.getItem('token'));
  }

  componentWillReceiveProps() {

  }

  syncMessages = () => {
    fetch('http://localhost:8081/message/', {
      method: 'GET',
      headers: {
        'Content-type': 'application/json',
        'Authorization': localStorage.getItem('token')
      }
    })
      .then((r) => {
        this.setState({ conversations: r.data })
      });
  }

  sendMessage = () => {

  }

  render() {
    return (
      <div id="conversation-content">
        <Input placeholder="Write here"/>
        <Button onClick={this.sendMessage}>Send</Button>
        <div className="conversation-body">
        </div>
      </div>
    )
  }
}

export default ConversationContent;