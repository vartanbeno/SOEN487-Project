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

    render(){
        return (

            <h1> You have many Notifications.</h1>


    )}
}
export default Notifications;