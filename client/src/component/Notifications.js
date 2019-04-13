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
              'Authorization': localStorage.getItem('token'),
              'Access-Control-Allow-Origin': 'http://localhost:8080/'
            }
      })
      .then(response => response.json())
      .then(data => this.printToConsole(data))
      .catch(error => console.error("Inside login promise: " + error));
      console.log('clicked the button')

    }

    printToConsole(data){

        console.log(data);
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