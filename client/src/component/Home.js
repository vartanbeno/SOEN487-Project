import React, { Component } from 'react';

class Home extends Component{

    constructor(props){
        super(props);

        this.checkAuthenticated();

    }

    checkAuthenticated(){

        if (!localStorage.getItem('token')){
            
            this.props.history.push(`/`);
        }
            

    }

    render(){
        return (
            
            <h1> Microservices are awesome</h1>

        )
    }



}
export default Home;