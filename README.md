# Tech Challenge - Backend
## Introduction
This is a backend application that provides a RESTful
API to manage a Monetary Converter. The application is written in Python using
the Django framework and uses a MongoDB database to store the conversion data. 
The application provides the following endpoints **->**
### Conversion:
- `GET /api/rates/`: Returns a list of all the currency rates.
- `GET /api/rates/{rateId}`: Returns the currency rate with the specified ID.
- `POST /api/convert/`: Converts an amount from one currency to another 
provide the following JSON payload:
```json
{
  "from_currency": "EUR",
  "to_currency": "USD",
  "amount": 100.0
}
```
- 'GET /api/conversions/': Returns a list of all the conversions made.

### Authentication:
- 'POST /api/login/': Authenticates the user with the provided credentials of 
this JSON payload:
```json
{
  "username": "user",
  "password": "password"
}
```
- 'POST /api/logout/': Logs out the user.
- 'POST /api/users/': Registers a new user with the provided credentials of
this JSON payload:
```json
{
    "first_name": "Test",
    "last_name": "Last",
    "username": "test",
    "password": "test123",
    "email": "test@gmail.com"
}
```

## Requirements
- Python
- MongoDB
- Any REST client (e.g. Postman), the collection is provided in the 
repository on the file `Tech Challenge.postman_collection.json` and the
environment file `Tech Challenge.postman_environment.json`.

## How to run
1. Run the following command to start the application:
```bash
python manage.py runserver
```
2. The application will be available at `http://localhost:8080`
3. Use the REST client to test the endpoints.

## Author
- [Nuno Proença Santos Oliveira](https://www.linkedin.com/in/nuno-oliveira-x/)
