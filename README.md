# SOEN 487 Project

This repository is for the SOEN 487 final project at Concordia University. You can find details about the contributors [here](https://github.com/vartanbeno/SOEN487-Project/wiki).

The project is a full stack microservices application for sending and receiving messages between users. Our project is broken down into 3 services:

 - Authentication Service
 - Notification Service
 - Message Service
 
# Getting Started

### Running

To start the application, we need to run the frontend and each microservice in the backend:

#### Frontend

`cd` into the `client` folder and run:

```
npm install
npm start
```

The frontend will be served at [http://localhost:3000/](http://localhost:3000/).

#### Backend

`cd` into the `server` folder. You will see one folder for each of the microservices. `cd` into each of them and run the `app.py` file:

```
python3 app.py
```

- The authentication service will be served at [http://localhost:5000/](http://localhost:5000/).
- The messaging service will be served at [http://localhost:8081/](http://localhost:8081/).
- The notification service will be served at [http://localhost:8080/](http://localhost:8080/).

# Usage

**Boot** 
After running all the services and frontend, navigate to [http://localhost:3000/](http://localhost:3000/).

**Login/Register**
If you are a new user, navigate the UI to register. Enter a valid email address, username and password. You will be sent a verification email within 3 minutes. Navigate to your emails, click the link in the email, and you will be verified! Proceed to login.

**Messaging**
At the current time of writing, the UI for the messaging service is incomplete. This is because the messaging service was not made compatible with the rest of the project and so much effort was put to get those services working, instead of the UI. The messaging service endpoints are still functional however, and we invite you to test them with [postman](https://www.getpostman.com/downloads/). The endpoints are defined in the [docs](https://docs.google.com/document/d/12_znub5JYVil9Zf0I7VzP__5CKfTM5gdi3BZVDClJDk).

**Notification**
You'll notice after sending some messages with postman, that notifications will have been created.


# Documentation

The project report, which includes more detailed specifications, such as the specific endpoints of each microservice, can be viewed [here](https://docs.google.com/document/d/12_znub5JYVil9Zf0I7VzP__5CKfTM5gdi3BZVDClJDk).

### ER Diagrams

This repository has class diagrams for each service, as well as their respective dependency diagrams. These diagrams can be viewed [here](https://github.com/vartanbeno/SOEN487-Project/tree/master/diagrams).

## Authors

- **Giovanni Prattico** - *ID:* 27316860
- **Andres Augusto Nunez Zegarra** - *ID:* 27194331
- **Joel Dusablon Senécal** - *ID:* 40035704
- **Vartan Benohanian** - *ID:* 27492049


## Task Breakdown

#### Giovanni Prattico
- Login UI, Register UI, Verify UI
- Notification Service
- Notification Servie testing
- Documentation, ReadME documentation
- Services integration debugging


#### Andres Zegarra
- Message service
- Message service UI
- Message service testing
- Powerpoint presentation

#### Vartan Benohanian
- Register email service
- frontend debugging
- project hosting
- JWT implementation across all services
- refactor notification service, refactor message service
- authentication service
- authentication service testing
- Documentation, ReadMe Documentation

#### Joel Senecal
- Image storing service
- Image storing service testing
- Powerpoint presentation

## Known Issues
Notification tests need to be changed so they grab the token from the authentication service before making the tests

## Other Comments
- The UI for the messaging service was not implemented because it required additional work to function. We we're having CORS issues with the backend, and then further work was required to message users by name instead of ID.
-The image storing service was not implemented. The service would've required UI to interact with.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
