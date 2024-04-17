# FastAPI and Vue.js Application

This project is a test of building a web app using FastAPI for the backend and Vue.js for the frontend.
It is only for testing purposes.
## Overview

The application consists of two main parts:

1. **Backend (FastAPI):** Provides RESTful APIs for CRUD operations and serves as the backend server for the application.
2. **Frontend (Vue.js):** A single-page application (SPA) built using Vue.js to interact with the backend APIs and render the user interface.

## Features

- User registration and authentication (OAuth JWT)
- CRUD operations for managing data entities
- Responsive user interface
- Integration of backend and frontend using RESTful APIs

## Technologies Used

### Backend

- FastAPI
- SQLAlchemy & SQLite
- Pydantic
- JWT (JSON Web Tokens)

### Frontend

- Vue.js
- Vuex
- Vuetify
- Axios

## Running with Docker Compose

To run the project using Docker Compose, make sure you have Docker installed on your system. Then, follow these steps:

1. docker-compose up --build
2. Navigate to localhost:8081


The application is hosted on an Azure Static Website. You can access it at the following URL:

- https://agreeable-glacier-022fe8c03-preview.westeurope.4.azurestaticapps.net

### Note

The application requires SignUp, and there is no email verification as it is just for test purposes.


<!-- ![App Preview](https://github.com/krassykirov/FastAPI-Vue/blob/vue_consolidation/demo.png) -->