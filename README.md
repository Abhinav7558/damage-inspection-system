# Damage Inspection System

A modular Flask-based backend API simulating a vehicle damage inspection workflow.

---

## Features

- User authentication with JWT
- Create and manage vehicle inspection reports
- MySQL database integration
- Role-based access: users can only view their own inspections
- Status filtering (`pending`, `reviewed`, `completed`)
- Input validations (e.g., image URL format)

---

## Project Structure

```
.
├── app/
│ ├── auth/
│ │ ├── routes.py
│ │ ├── services.py
│ │ ├── utils.py
│ │ └── validators.py
│ ├── inspection/
│ │ ├── routes.py
│ │ └── validators.py
│ └── models/
│ ├── inspection.py
│ └── user.py
├── migrations/
├── main.py
├── run.py
├── .env
├── sample.env
├── pyproject.toml
├── README.md
├── uv.lock
└── .pre-commit-config.yaml
```

---

### Installation

#### Clone the Repository

```bash
git clone https://github.com/Abhinav7558/damage-inspection-system.git
cd damage-inspection-system
```

#### Setup Environment

```bash
cp sample.env .env
```

Update `.env` with your MySQL connection details and JWT secret.

#### Install Dependencies

```bash
uv sync
```

#### Apply Migrations

```bash
uv run flask db upgrade
```

---

### Run the Application

```bash
uv run python run.py
```

App runs at: `http://127.0.0.1:5000`

---

## API Endpoints

### Auth Routes

- `POST /signup` – Register new user
- `POST /login` – Authenticate and receive JWT token

### Protected Inspection Routes (JWT required)

- `POST /inspection` – Create a new inspection
- `GET /inspection/<id>` – View inspection (only if created by you)
- `PATCH /inspection/<id>` – Update status to `reviewed` or `completed`
- `GET /inspection?status=pending` – Filter inspections by status

---

## Security & Validation

- Passwords hashed with `bcrypt`
- JWT-based authentication using `flask-jwt-extended`
- `image_url` validated for file extensions (`.jpg`, `.jpeg`, `.png`)

---

## Logging & Error Handling

- All requests are logged with timestamps and route info
- Handles edge cases like:
  - Unauthorized access
  - Missing or invalid data
  - DB failures

---

## Live Demo

https://damage-inspection-system.onrender.com
