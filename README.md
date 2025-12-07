# Warehouse Management System 🏭

Django REST API for warehouse component inventory tracking with Tkinter desktop client.

![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-5.2-green)
![DRF](https://img.shields.io/badge/DRF-3.14-red)

## 📖 Project Background

This project was created to solve a **real workplace problem** at my job. Currently, we manually track component inventory by writing codes on paper and then manually transferring this data to Excel spreadsheets. This process is time-consuming, error-prone, and inefficient.

I designed and implemented this system to automate the entire workflow - from component placement and release tracking to location-based inventory management with business rule enforcement.

**Development Notes:**
- **Backend (Django REST API):** Fully developed by myself from scratch, including architecture design, database modeling, business logic implementation, and API design.
- **Frontend (Tkinter Desktop Client):** Developed with AI assistance. While I designed the user interface and integration logic, I utilized AI tools to help with Tkinter-specific implementation details as I'm less experienced with desktop GUI frameworks.

## 🛠 Tech Stack

**Backend:** Django 5.2 • Django REST Framework • SQLite/PostgreSQL • Python 3.13  
**Frontend:** Tkinter • Requests  
**Testing:** pytest • pytest-django • coverage

## ✨ Features

- REST API with 6 endpoints for inventory management
- Component tracking with location-based organization
- Business rules: max 28 units & 2 component types per location
- Role-based permissions (Admin/User)
- Atomic transactions with row-level locking (race condition prevention)
- Desktop client with real-time API communication
- Comprehensive input validation

## 📡 API Endpoints

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| `GET` | `/api/me/` | Authenticated | Check user credentials & role |
| `POST` | `/api/add_components/` | Authenticated | Add components to location |
| `PATCH` | `/api/release_components/` | Authenticated | Release components from location |
| `GET` | `/api/component/<code>/localizations/` | Authenticated | Show component locations |
| `GET` | `/api/localization/<n>/components/` | Authenticated | Show location contents |
| `DELETE` | `/api/clear_warehouse/` | Admin only | Clear entire warehouse |

## 🚀 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py create_localizations
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd frontend
pip install -r requirements.txt
python GUI_Tkinker.py
```

## 🧪 Testing
```bash
cd backend
pytest
coverage run --source='.' manage.py test
coverage report
```

## 📊 Architecture
```
┌─────────────────┐
│  Tkinter Client │  (Desktop GUI)
└────────┬────────┘
         │ HTTP + Basic Auth
         ▼
┌─────────────────┐
│  Django REST    │  Views → Services → Models
│   Framework     │  (Atomic transactions, validation)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL /   │  (Component + Localization tables)
│    SQLite       │
└─────────────────┘
```

## 📝 Example Request
```bash
# Add components
curl -X POST http://localhost:8000/api/add_components/ \
  -u user:password \
  -H "Content-Type: application/json" \
  -d '{"code":"1234","localization":"A1","quantity":10}'

# Response
{"message": "Adding code 1234 on localization A1 was successful"}
```


## 🔒 Key Implementation Details

- **Transaction Safety:** `select_for_update()` prevents concurrent modification issues
- **Service Layer:** Business logic separated from views (clean architecture)
- **Custom Validators:** Code format, quantity limits, location capacity
- **Permission Classes:** `IsAuthenticated`, `IsAdminUser`
- **Atomic Operations:** Ensures data consistency

## 📁 Project Structure
```
Warehouse/
├── backend/
│   ├── Warehouse_System/    # Main app
│   │   ├── models.py         # Component, Localization models
│   │   ├── serializers.py    # DRF serializers
│   │   ├── views.py          # API endpoints
│   │   ├── services.py       # Business logic
│   │   └── tests/            # Pytest tests
│   └── manage.py
└── frontend/
    └── GUI_Tkinker.py        # Desktop client
```

## 👤 Author

**Kacper Kubiak** 

---

*Portfolio project demonstrating Django REST API development, database management, and full-stack integration. Based on real workplace needs, solving manual inventory tracking inefficiencies.*