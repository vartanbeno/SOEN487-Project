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
        fetch('http://localhost:8080/api/notifications', {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
      })
      .then(response => response.json())
      .then(data => this.setState({array: data}))
    }

    render(){
        const { array } = this.state;
        return (
            <div>
                <h1>You have {array.length} notification(s).</h1>
                <ul>
                {array.map(notification =>
                    <li key={notification.id}>
                        <p>{notification.message}</p>
                    </li>
                    )}
                </ul>
            </div>

    )}
}
export default Notifications;