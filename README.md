# Event Management System

A RESTful Event Management System built with **Django** and **Django REST Framework**.

This project was initially developed as an educational project focused on building a real-world event management API. It provides a platform where organizers can create and manage events, while participants can register for and attend them.

## ✨ Features

- 👤 User authentication using Session Authentication
- 🎫 Event creation and management by organizers
- 👥 Event registration for participants
- 📋 Event participation management
- 🔗 Support for event prerequisites
  - An event can require participants to have completed another event before registering.
- ⭐ Event rating
- 💬 Comments and reviews
- 📖 API documentation with Swagger
- 🗄️ PostgreSQL database

## 🛠️ Technologies

- Python
- Django
- Django REST Framework
- PostgreSQL
- Swagger / OpenAPI

## 📌 Project Overview

The system is designed around two main user roles:

### Organizer

Organizers can create and manage events and define requirements such as prerequisites for participation.

For example, an organizer can define that:

> Event B requires participants to have completed Event A.

This allows events to have dependencies and makes it possible to create structured learning or participation paths.

### Participant

Participants can:

- Browse available events
- Register for events
- Participate in events
- Rate events
- Leave comments and reviews

## 🔐 Authentication

The current version of the project uses **Session Authentication**.

JWT-based authentication is planned as part of future improvements.

## 📚 API Documentation

The project includes **Swagger / OpenAPI documentation** for exploring and testing the available API endpoints.

## 🗄️ Database

The project uses **PostgreSQL** as its primary database.

## 🚀 Future Improvements

This project is open to further development and improvements.

Planned improvements include:

- [ ] Replace Session Authentication with JWT Authentication
- [ ] Add API Pagination
- [ ] Dockerize the application
- [ ] Integrate Redis
- [ ] Explore Celery for asynchronous/background tasks
- [ ] Improve overall application architecture and performance

## 🎯 Project Purpose

This project was originally created as part of a Django REST Framework learning process.

The goal is to continue developing the project beyond its initial educational implementation and gradually improve its architecture, performance, scalability, and production readiness.

## 📄 License

This project is for educational and development purposes.
