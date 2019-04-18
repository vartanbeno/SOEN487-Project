import React, { Component } from 'react';
import { row } from 'reactstrap';
import '../App.css';

class Home extends Component{

    constructor(props){
        super(props);

        this.checkAuthenticated();
        this.handleLogout = this.handleLogout.bind(this);
        this.handleNotifications = this.handleNotifications.bind(this);

    }

    checkAuthenticated(){

        if (!localStorage.getItem('token')){
            
            this.props.history.push(`/`);
        }
            

    }

    handleNotifications(){

        this.props.history.push(`/notifications`);

    }

    handleLogout(){

        localStorage.removeItem('token', null)
        this.props.history.push(`/`);
        
    }
    goToConversations =() =>{
        this.props.history.push(`/conversations`);
    }

    render(){
        return (
        <div className="App">
            <header className="App-header">
            <h1> Microservices are awesome</h1>
            <div>
                <button onClick={this.goToConversations} style={{marginRight: 40, background: 'CornflowerBlue', border: 'CornflowerBlue', width: 125, height: 50}}>Send Messages</button>
                <button onClick={this.handleNotifications} style={{background: 'white', border: 'white', width: 105, height: 50}}>Notifications</button>
            </div>
            <button style={{marginTop: 20,background: 'green', border: 'green', width: 105, height: 50}} onClick={this.handleLogout}> Logout </button>
        </header>
        </div>
        )
    }



}
export default Home;