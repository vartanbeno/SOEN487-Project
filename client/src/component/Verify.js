import { Component } from 'react';

class Verify extends Component {

    constructor(props){
        super(props);
    }


    componentDidMount(){
        this.parseRequest();
    }

    parseRequest(){

        const search = this.props.location.search;
        const params = new URLSearchParams(search);
        const verifyKey = params.get('key');
        this.forwardRequest(verifyKey);
    }

    forwardRequest(verifyKey){

        fetch(`http://localhost:5000/api/auth/verify?key=${verifyKey}`, {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            }
      })
      .then(response => response.json())
      .then(data => data.message)
      .then(message => alert('success! Your account has been verified'))
      .catch(error => alert('Error verifying your account '+ error));

    }

    render() {
        return null;
    }

}

export default Verify;
