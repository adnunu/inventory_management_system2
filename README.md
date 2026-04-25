# Inventory Management System

A Flask-based REST API for managing inventory with full CRUD operations and OpenFoodFacts API integration.

## Features

- **Full CRUD Operations**: Create, Read, Update (PUT/PATCH), Delete inventory items
- **External API Integration**: Fetch real-time product data from OpenFoodFacts API
- **CLI Interface**: User-friendly command-line tool for all operations
- **Unit Testing**: Comprehensive test suite for all endpoints
- **In-memory Storage**: Simulated database using Python array

## Technologies

- Python 3.8+
- Flask 2.3.3
- Requests 2.31.0
- unittest

## Installation

```bash
# Clone the repository
git clone https://github.com/adnunu/inventory_management_system2.git
cd inventory_management_system2

# Install dependencies
pip install -r requirements.txt