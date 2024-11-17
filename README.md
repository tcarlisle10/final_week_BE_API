# Mechanic Service API

This project is a Flask-based API for managing a mechanic service system. It includes functionality for managing customers, mechanics, and service tickets.

## Project Structure

```
__pycache__/
.env
.pytest_cache/
.vscode/
app/
    __init__.py
    blueprints/
        customer/
            __init__.py
            routes.py
            schemas.py
        mechanic/
            __init__.py
            routes.py
            schemas.py
        serviceTicket/
            __init__.py
            routes.py
            schemas.py
    extensions.py
    models.py
    static/
        swagger.yaml
    utils/
        util.py
app.py
config.py
instance/
requirements.txt
```

## Setup

### Prerequisites

- Python 3.8+
- Virtual environment (optional but recommended)

### Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    Create a 

.env

 file in the root directory and add the following:

    ```env
    DATABASE_URL=sqlite:///mechanic.db
    SECRET_KEY=<your-secret-key>
    ```

5. Initialize the database:

    ```sh
    python app.py
    ```

## Running the Application

To run the application, use the following command:

```sh
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Customers

- **Create Customer**
  - `POST /customers`
  - Request Body: `CreateCustomerPayload`
  - Response: `CreateCustomerResponse`

- **Get All Customers**
  - `GET /customers/all`
  - Response: List of customers

- **Get Customer by ID**
  - `GET /customers/<int:customer_id>`
  - Response: 

CustomerSchema



- **Update Customer**
  - `PUT /customers/<int:customer_id>`
  - Request Body: `UpdateCustomerPayload`
  - Response: `UpdateCustomerResponse`

- **Delete Customer**
  - `DELETE /customers/<int:customer_id>`
  - Response: Success message

### Mechanics

- **Create Mechanic**
  - `POST /mechanics`
  - Request Body: `CreateMechanicPayload`
  - Response: `CreateMechanicResponse`

- **Login Mechanic**
  - `POST /mechanics/login`
  - Request Body: `LoginPayload`
  - Response: `LoginResponse`

- **Get All Mechanics**
  - `GET /mechanics`
  - Response: List of mechanics

- **Get Mechanic by ID**
  - `GET /mechanics/<int:mechanic_id>`
  - Response: 

MechanicSchema



- **Update Mechanic**
  - `PUT /mechanics/<int:mechanic_id>`
  - Request Body: `UpdateMechanicPayload`
  - Response: `UpdateMechanicResponse`

- **Delete Mechanic**
  - `DELETE /mechanics/<int:mechanic_id>`
  - Response: Success message

### Service Tickets

- **Create Service Ticket**
  - `POST /serviceTickets`
  - Request Body: `CreateServiceTicketPayload`
  - Response: `CreateServiceTicketResponse`

- **Get All Service Tickets**
  - `GET /serviceTickets/all`
  - Response: List of service tickets

- **Get Service Ticket by ID**
  - `GET /serviceTickets/<int:service_ticket_id>`
  - Response: 

ServiceTicketSchema



- **Update Service Ticket**
  - `PUT /serviceTickets/<int:serviceTicket_id>`
  - Request Body: `UpdateServiceTicketPayload`
  - Response: `UpdateServiceTicketResponse`

- **Delete Service Ticket**
  - `DELETE /serviceTickets/<int:service_ticket_id>`
  - Response: Success message

## Testing

To run the tests, use the following command:

```sh
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.