import React, { Component } from 'react';
import '../App.css'
import {
    Col, Form,
    FormGroup, Label, Input
  } from 'reactstrap';

class Login extends Component {

    constructor(props){
        super(props);

        this.state = {
            username: '',
            password: ''

        }

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.postLogin = this.postLogin.bind(this);
        this.handleGoBack = this.handleGoBack.bind(this);
    }

    handleGoBack(){

      this.props.history.push(`/`);

    }

    handleChange(event){
        const target = event.target;
        const value = target.value;
        const id = target.id;
    
        this.setState({[id]: value});
    }

    handleSubmit(event){

        event.preventDefault();
        
        if(this.state.username.length<1){
          alert('Please enter a username');
        } else if(this.state.password.length<1){
          alert('Please enter a password');
        }else{
          //this.postLogin();
          console.log('Ready to submit')
          this.postLogin();
        }
    }

    postLogin(){

        fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: this.state.username,
                password: this.state.password
            })
      })
      .then(response => response.json())
      .then(data => data.token)
      .then(token => this.processToken(token))
      .catch(error => console.error("Inside login promise: " + error));

    }

    processToken(token){

      if (!token){
        console.log('token undefined!');
        alert('Incorrect Crendentials!')
      } else {
  
        this.saveToken(token);
        this.props.history.push(`home`);
      }

    }

    saveToken(token){
      console.log('saving token to local storage');
      localStorage.setItem('token', token);

    }


    render(){

        return (
            
        <div className="App">
        <header className="App-header">
            <h1>Enter your credentials to Login</h1>
            
            <Form className="form" onSubmit={this.handleSubmit}>
                <Col>
                <br/>
                <FormGroup>
                    <Label>Username</Label>
                    <Input
                        type="username"
                        name="username"
                        id="username"
                        onChange={this.handleChange}
                />
                <br/>
                    <Label>Password</Label>
                    <Input
                        type="password"
                        name="password"
                        id="password"
                        placeholder=""
                        onChange={this.handleChange}
                    />
                <br/>
                <button style={{textAlign: 'right',alignSelf: 'stretch'}} type="submit" value="Submit">Submit</button>
              </FormGroup>
            </Col>
            <br/>
            </Form>
            <button onClick={this.handleGoBack}> Go Back </button>
          </header>
          </div>
            




            
        )
    }




}

export default Login;
