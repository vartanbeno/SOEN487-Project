# SOEN 487 Project

This repository is for the SOEN 487 final project at Concordia University. You can find details about the contributors [here](https://github.com/vartanbeno/SOEN487-Project/wiki).

## Getting Started

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

### ER Diagrams

// todo

### Documentation

The project report, which includes more detailed specifications, such as the specific endpoints of each microservice, can be viewed //todo

## Authors

- **Giovanni Prattico** - *ID:* 27316860
- **Andres Augusto Nunez Zegarra** - *ID:* 27194331
- **Joel Dusablon Senécal** - *ID:* 40035704
- **Vartan Benohanian** - *ID:* 27492049

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
