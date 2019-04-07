import React, { Component } from 'react';
import '../App.css';

class Landing extends Component{

    constructor(props){

        super(props);
        this.state = {
        
        loginClicked: false,
        registerClicked: false

      };
      
      this.handleLogin = this.handleLogin.bind(this);
      this.handleRegister = this.handleRegister.bind(this);

    }

    

  handleLogin(){

    console.log('call handleLogin')
    this.setState({loginClicked: true});
    console.log('register Clicked is: '+this.state.registerClicked);
    this.props.history.push(`/login`);
  }

  handleRegister(){

    console.log('call handleRegister');
    this.setState({registerClicked: true});
    console.log('login clicked is: '+this.state.loginClicked);
    this.props.history.push(`/register`);

  }



    render(){
        return (
        <div className="App">
        <header className="App-header">
          <div>
            <h1>Welcome to Team Giovanni Prattico</h1>
            <button style={{background: 'light-blue', border: 'light-blue', width: 105, height: 50}} onClick={this.handleLogin}> Login </button>
            <br />
            <br />
            <button style={{background: 'orange', border: 'orange', width: 105, height: 50}}onClick={this.handleRegister}> Register </button>
          </div>
        </header>
      </div>

        )
    }



}

export default Landing;