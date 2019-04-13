import React, { Component } from 'react';

class Notifications extends Component{
    constructor(props){
        super(props);
        this.checkAuthenticated();
    }

    checkAuthenticated(){

        if(!localStorage.getItem('token')){

            this.props.history.push(`/`);
        }

    }

    fetchMessages(){

        fetch('http://localhost:8080/api/notifications/', {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Authorization': 'Bearer '+localStorage.getItem('token')
            }
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error("Inside login promise: " + error));
      console.log('clicked the button')

    }

    render(){
        return (
            <div>
            <h1> You have many Notifications.</h1>
            <button onClick={this.fetchMessages}>Fetch Messages</button>
            </div>

    )}
}
export default Notifications;