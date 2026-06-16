# ML Model Platform 🚀

A FastAPI-based backend platform that allows users to securely upload, manage, and serve their own machine learning models for real-time predictions.

This project combines backend engineering principles with practical machine learning deployment concepts by enabling users to register, authenticate, upload serialized ML models, and generate predictions through REST APIs.

---

## ✨ Features

### 🔐 Authentication & Authorization

* User Registration
* User Login
* JWT-based Authentication
* Password Hashing using Argon2
* Protected Routes
* Current User Endpoint (`/auth/me`)

---

### 👤 User Management

* Update Own Profile
* Delete Own Account
* Secure User-specific Authorization

---

### 👨‍💼 Admin Features

* View All Users
* View Specific User Details
* Delete Users
* View All Uploaded Models
* View Specific Models
* Delete Any Model
* Reset User Prediction Quotas

---

### 🤖 Model Registry

Authenticated users can:

* Create Model Metadata
* View Their Own Models
* Retrieve Specific Models
* Update Model Metadata
* Delete Models

Ownership validation ensures users cannot access or manipulate models belonging to other users.

---

### 📤 Model Uploads

Supported model formats:

* `.pkl`
* `.joblib`

Features:

* User-specific upload directories
* File path persistence in PostgreSQL
* Extension validation
* Secure upload handling


### ⚡ Real-Time Prediction Service

Users can generate predictions using their uploaded machine learning models.

### 🎯 Prediction Quota System

Each user is assigned a prediction quota.

Features:

* Quota decreases by 1 after every successful prediction.
* Predictions are blocked when quota reaches zero.
* Administrators can reset user quotas.

### 🧹 Automatic Cleanup

The platform automatically maintains storage consistency.

Implemented cleanup mechanisms:

* Delete uploaded model files when models are deleted.
* Delete uploaded user directories when users are removed.
* PostgreSQL cascade deletion of model records.

## 🛠️ Tech Stack

### Backend

* FastAPI
* PostgreSQL
* SQLAlchemy 2.0
* Alembic

### Authentication

* JWT (JSON Web Tokens)
* Argon2 Password Hashing

### Machine Learning

* scikit-learn
* joblib

### API Testing & Documentation

* Swagger UI
* Postman

---

## 📌 Key Concepts Demonstrated

This project showcases practical experience with:

* REST API Design
* JWT Authentication
* Role-Based Access Control
* Repository-Service Architecture
* SQLAlchemy ORM Relationships
* Alembic Database Migrations
* PostgreSQL Cascade Deletes
* Multipart File Uploads
* Machine Learning Model Serving
* Ownership Validation
* Resource Usage Controls
* Filesystem Cleanup Strategies

---
## 📚 Summary

ML Model Platform is an end-to-end backend application that bridges backend engineering and machine learning deployment. It enables users to securely upload and serve their own machine learning models while enforcing authentication, authorization, ownership validation, prediction quotas, and administrative controls.

The project demonstrates how traditional machine learning workflows can be transformed into production-style APIs capable of serving predictions to authenticated users in a multi-user environment.
