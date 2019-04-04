import React, { Component } from 'react';
import {
    Col, Form,
    FormGroup, Label, Input,
    Button,
    Container,
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
      .then(token => this.saveToken(token))
      .catch(error => console.error("Inside login promise: " + error));

    }

    saveToken(token){

      if (!token){
        console.log('token undefined!');
        alert('Incorrect Crendentials!')
      }

      console.log('the token is: '+token);
    }


    render(){

        return (
            <div>
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
                <Button style={{textAlign: 'right',alignSelf: 'stretch'}}type="submit" value="Submit">Submit</Button>
              </FormGroup>
            </Col>
            <br/>
            </Form>
            </div>
            




            
        )
    }




}

export default Login;
