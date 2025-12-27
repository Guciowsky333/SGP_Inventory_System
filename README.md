# Warehouse Management System 🏭

Django REST API for warehouse component inventory tracking with a Tkinter desktop client.  
The backend is fully containerized using **Docker**, with separate containers for the **Django application** and the **PostgreSQL database**.

![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-5.2-green)
![DRF](https://img.shields.io/badge/DRF-3.14-red)
![Docker](https://img.shields.io/badge/docker-enabled-blue)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue)

## 📖 Project Background

This project was created to solve a **real workplace problem** at my job. Currently, we manually track component inventory by writing codes on paper and then manually transferring this data to Excel spreadsheets. This process is time-consuming, error-prone, and inefficient. I designed and implemented this system to automate the entire workflow - from component placement and release tracking to location-based inventory management with business rule enforcement.

### Development Notes

- **Backend (Django REST API):**
  - Fully designed and implemented by myself
  - Architecture, database schema, business logic, and API design created from scratch
  - Runs inside a **Docker container**
- **Database:**
  - **PostgreSQL**, running in a **separate Docker container**
- **Frontend (Tkinter Desktop Client):**
  - UI and integration logic designed by myself
  - AI assistance used for Tkinter-specific implementation details

---

## 🛠 Tech Stack

**Backend:**  
- Django 5.2  
- Django REST Framework  
- PostgreSQL  
- Python 3.13  

**Infrastructure:**  
- Docker  
- Docker Compose  
- Separate containers for `web` (Django) and `db` (PostgreSQL)

**Frontend:**  
- Tkinter  
- Requests  

**Testing:**  
- pytest  
- pytest-django  
- coverage  

---

## ✨ Features

- REST API with 6 endpoints for inventory management
- Location-based component tracking
- Business rules enforcement:
  - max **28 units per location**
  - max **2 component types per location**
- Role-based permissions (Admin / User)
- Atomic database transactions with row-level locking
- PostgreSQL-backed persistence
- Desktop client with real-time API communication
- Comprehensive input validation

---

## 📡 API Endpoints

| Method | Endpoint | Permission | Description |
|------|---------|------------|------------|
| `GET` | `/api/me/` | Authenticated | Check user credentials & role |
| `POST` | `/api/add_components/` | Authenticated | Add components to location |
| `PATCH` | `/api/release_components/` | Authenticated | Release components from location |
| `GET` | `/api/component/<code>/localizations/` | Authenticated | Show component locations |
| `GET` | `/api/localization/<n>/components/` | Authenticated | Show location contents |
| `DELETE` | `/api/clear_warehouse/` | Admin only | Clear entire warehouse |

---

## 🚀 Quick Start (Docker)

### Requirements
- Docker
- Docker Compose

### Start backend & database
```bash
docker-compose up --build
```


API available at: `http://127.0.0.1:8000/api/`

### Frontend
```bash
cd frontend
pip install -r requirements.txt
python GUI_Tkinker.py
```

## 🧪 Running Tests
```bash
# Run all tests inside web container
docker-compose exec web pytest

# Run tests with verbose output
docker-compose exec web pytest -v

```

## 📊 Architecture
```text
┌─────────────────┐
│ Tkinter Client │ (Desktop GUI)
└────────┬────────┘
         │ HTTP + Basic Auth
         ▼
┌─────────────────┐
│ Django REST    │ (Docker: web)
│ API            │ Views → Services → Models
│                │ Atomic transactions, validation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PostgreSQL     │ (Docker: db)
│                │ Component & Localization tables
└─────────────────┘
```

## 📝 Example Request

```bash
curl -X POST http://localhost:8000/api/add_components/ \
  -u user:password \
  -H "Content-Type: application/json" \
  -d '{"code":"1234","localization":"A1","quantity":10}'
 ```
# Response
```bash
{"message": "Adding code 1234 on localization A1 was successful"}
```

## 🔒 Key Implementation Details
- **Transaction Safety:** select_for_update() prevents concurrent modification issues
- **Service Layer:** Business logic separated from views (clean architecture)
- **Custom Validators:** Code format, quantity limits, location capacity
- **Permission Classes:** IsAuthenticated, IsAdminUser
- **Atomic Operations:** Ensures data consistency

## 📁 Project Structure
```
Warehouse/
├── backend/
│   ├── Dockerfile                 # Django backend container
│   ├── docker-compose.yaml        # Docker Compose (web + PostgreSQL)
│   ├── .env                       # Environment variables
│   ├── requirements.txt           # Backend dependencies
│   ├── manage.py
│   └── Warehouse_System/           # Main app
│       ├── models.py               # Component, Localization models
│       ├── serializers.py          # DRF serializers
│       ├── views.py                # API endpoints
│       ├── services.py             # Business logic
│       └── tests/                  # Pytest tests
│
└── frontend/
    ├── GUI_Tkinker.py              # Desktop client
    └── requirements.txt            # Frontend dependencies
```

## 👤 Author

**Kacper Kubiak**
- GitHub: [Guciowsky333](https://github.com/Guciowsky333/SGP_Inventory_System)