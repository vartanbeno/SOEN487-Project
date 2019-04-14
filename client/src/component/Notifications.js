import React, { Component } from 'react';

class Notifications extends Component{
    constructor(props){
        super(props);
        this.checkAuthenticated();

        this.state = {
            array: []
        }
        
    }

    checkAuthenticated(){

        if(!localStorage.getItem('token')){

            this.props.history.push(`/`);
        }

    }

    componentDidMount(){

        fetch('http://localhost:8080/api/notifications/', {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Authorization': 'Bearer '+localStorage.getItem('token')
            }
      })
      .then(response => response.json())
      .then(data => this.setState({array: data}))
    }

    render(){
        const { array } = this.state;
        return (
            <div>
            <h1> You have many Notifications.</h1>
            <ul>
            {array.map(array =>
                <li key={array.id}>
                    <p>Message from {array.senderID} to {array.receiverID}</p>
                </li>
                )}
            </ul>

            </div>

    )}
}
export default Notifications;