import React, { Component } from 'react';
import ConversationContent from './ConversationContent';
import { Button, Input } from 'reactstrap';
import './ConversationDashboard.css'

class ConversationDashBoard extends Component {
  constructor (props) {
    super(props);
    this.state = {
      conversations: [],
      selectedConversation: null,
      showNewConversation: false,
      participantId: null,
      myId:null,
    }


    this.checkAuthenticated();

  }
  conversationRef = React.createRef();

  checkAuthenticated(){

      if (!localStorage.getItem('token')){
          
          this.props.history.push(`/`);
      }
          

  }

  componentDidMount() {
    this.getConversations();
  }

  getConversations = () => {
    fetch('http://localhost:8081/conversation', {
      method: 'GET',
      headers: {
        // 'Accept': 'application/json',
        'Authorization': "Bearer " + localStorage.getItem('token')
      },
    })
      .then(r => r.json())
      .then((data) => {
        this.setState({ 
          conversations: data.conversations,
          myId: data.user_id,
         })
      });
  }

  onClickNewConversation = () => {
    this.setState({ showNewConversation: true })
  }

  onChangeInput = (event) => {
    this.setState({ participantId: event.target.value })
  }

  onClickCreateConversation = () => {
    const { participantId } = this.state;
    fetch('http://localhost:8081/conversation', {
      method: 'POST',
      headers: {
        'Authorization': "Bearer " + localStorage.getItem('token'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        participant_id: participantId
      })
    })
      .then(r => r.json())
      .then((data) => {
        this.getConversations();
      })
    this.setState({ showNewConversation: false })
  }

  onClickConversationTab = (conversationId) => {
    this.setState({selectedConversation: conversationId});
    this.conversationRef.current.syncMessages(conversationId)
  }

  renderConversations = () => {
    const { conversations, showNewConversation, myId } = this.state;
    return (
      <table>
        <tbody>
          <tr >
            {!showNewConversation ? (
              <th><Button onClick={this.onClickNewConversation}>New conversation</Button></th>
            ) : (
                <th>
                  Id:
                  <Input onChange={this.onChangeInput}></Input>
                  <Button onClick={this.onClickCreateConversation}>Create Conversation</Button>
                </th>
              )}
          </tr>
          {conversations.map(c =>
            <tr key={c.id}>
              <th className="conversation-item" onClick={() => this.onClickConversationTab(c.id)}>
                {`Conversation with ${parseInt(c.creator_id) === myId ? c.participant_id : c.creator_id}`}
              </th>
            </tr>
          )}
        </tbody>
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
          <ConversationContent conversationId={selectedConversation} ref={this.conversationRef} />
        </div>
      </div>
    )
  }
}

export default ConversationDashBoard;