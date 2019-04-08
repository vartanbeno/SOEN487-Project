import React, { Component } from 'react';
import ConversationContent from './ConversationContent';
import { Button } from 'reactstrap';
import './ConversationDashboard.css'

class ConversationDashBoard extends Component {

  constructor (props) {
    super(props);
    this.state = {
      conversations: [],
      selectedConversation: null
    }
  }

  componentDidMount() {
    this.getConversations();
  }

  getConversations = () => {
    fetch('http://localhost:8001/conversation', {
      method: 'GET',
      headers: {
        'Authorization': 'application/json'
      }
    })
      .then((r) => {
        this.setState({ conversations: r.data })
      });
  }

  renderConversations = () => {
    const { conversations } = this.state;

    return (
      <table>
        <tr>
          <th><Button>New conversation</Button></th>
        </tr>
        {conversations.map(c =>
          <tr>
            <th className="conversation-item">my title</th>
          </tr>
        )}
      </table>
    );
  }

  render() {
    const { selectedConversation } = this.state;
    return (
      <div id="conversations">
        <h1>Conversations</h1>
        <div className="container">
          <div className="conversation-list">
            {this.renderConversations()}
          </div>
          <ConversationContent conversation={selectedConversation} />
        </div>
      </div>
    )
  }
}

export default ConversationDashBoard;