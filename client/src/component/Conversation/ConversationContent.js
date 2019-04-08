import React, { Component } from 'react';
import { Input, Button } from 'reactstrap';
import './ConversationContent.css'

class ConversationContent extends Component {
  constructor (props) {
    super(props);
    this.state = {
      messages: [],
      count: 0,
    }
  }

  componentDidMount() {

  }

  componentWillReceiveProps() {

  }

  render() {
    return (
      <div id="conversation-content">
        <Input placeholder="Write here"/>
        <Button>Send</Button>
        <div className="conversation-body">
          
        </div>
      </div>
    )
  }
}

export default ConversationContent;