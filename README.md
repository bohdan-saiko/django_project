# Silly little tests

A short description.

## Stack

- **Backend:** Python 3.12, Django 5.x
- **Database:** PostgreSQL 16
- **Dependency management:** pip + `requirements.txt`

---

## Requirements

- Python 3.10+
- PostgreSQL 14+
- pip

---

## Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:bohdan-saiko/django_project.git
cd django_project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 5. Create the database

```bash
psql -U postgres -c "CREATE DATABASE db_name;"
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

The server will be available at [http://localhost:8000](http://localhost:8000)

---

