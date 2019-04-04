import React, { Component } from 'react';
import Login from './component/Login';
import Register from './component/Register';
import Verify from './component/Verify';
import { Button } from 'reactstrap';
import {
  BrowserRouter,
  Route
} from 'react-router-dom'
import './App.css';

class App extends Component {

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
  }

  handleRegister(){

    console.log('call handleRegister');
    this.setState({registerClicked: true});
    console.log('login clicked is: '+this.state.loginClicked);

  }


  render() {
    return (
      <BrowserRouter>
         <Route path="/api/auth/verify" component={Verify}/>
      
        <div className="App">
          <header className="App-header">
            {(this.state.loginClicked || this.state.registerClicked) ? null : 
            <div>
              <h1>Welcome to Team Giovanni Prattico</h1>
              <button style={{background: 'light-blue', border: 'light-blue', width: 105, height: 50}} onClick={this.handleLogin}> Login </button>
              <br />
              <br />
              <button style={{background: 'orange', border: 'orange', width: 105, height: 50}}onClick={this.handleRegister}> Register </button>
            </div>
            }
            {this.state.loginClicked ? <Login /> : null}
            {this.state.registerClicked ? <Register /> : null}
          </header>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
