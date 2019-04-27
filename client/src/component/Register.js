import React, { Component } from 'react';
import {
    Col, Form,
    FormGroup, Label, Input,
    Button
  } from 'reactstrap';
import '../App.css'

class Register extends Component {

    constructor(props){
        super(props);

        this.state = {

            email: '',
            username: '',
            password: ''
        }

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.postRegister = this.postRegister.bind(this);
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
        }else if(this.state.email.length<1){
          alert('Please enter an email');
        } else{
          console.log('ready to register')
          this.postRegister();
        }
    }

    postRegister(){

        fetch('http://localhost:50001/api/auth/register', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: this.state.email,
                username: this.state.username,
                password: this.state.password
            })
      })
      .then(response => response.json())
      .then(data => data.message)
      .then(message => console.log(message))
      .then(alert('Verify your account by sending a POST with your key to /verify'))
      .then(this.props.history.push(`/`))
      .catch(error => console.error("Inside register promise: " + error));

    }

    render(){

        return (
            <div className="App">
            <header className="App-header">
                <h1>Register</h1>

                <Form className="form" onSubmit={this.handleSubmit}>
                    <Col>
                    <br/>
                    <FormGroup>
                        <Label>Email</Label>
                        <Input
                            type="email"
                            name="email"
                            id="email"
                            onChange={this.handleChange}
                        />
                        <br />
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


                <button onClick={this.handleGoBack}> Go Back </button>
             </header>
            </div>


            
        )
    }




}

export default Register;