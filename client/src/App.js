import React, { Component } from 'react';
import Login from './component/Login';
import Register from './component/Register';
import Landing from './component/Landing';
import Verify from './component/Verify';
import Home from './component/Home';
import {
  BrowserRouter,
  Route,
  Switch
} from 'react-router-dom'
import './App.css';

class App extends Component {


  render() {
    return (
      <BrowserRouter>
        <Switch>
         <Route path="/api/auth/verify" component={Verify}/>
         <Route path="/home" component={Home}/>
         <Route path="/login" component={Login}/>
         <Route path="/register" component={Register}/>
         <Route path="/" component={Landing}/>
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
