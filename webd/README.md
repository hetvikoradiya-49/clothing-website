# Luxe Clothing - Fashion E-Commerce Website

A modern, responsive e-commerce website for Luxe Clothing - premium fashion brand

## Features

- Modern, premium UI design
- Product catalog with categories
- Shopping cart functionality
- User authentication
- Newsletter subscription
- Responsive design for all devices

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Django (Python)
- **Database**: SQLite

## Project Structure

```
fashion_store/
├── store/                  # Main Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── products/               # Products app
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── media/                   # Media files
├── templates/               # Base templates
├── static/                  # Static files (CSS, JS)
├── manage.py
└── requirements.txt
```

## Setup Instructions

1. Create virtual environment:
   
```
bash
   python -m venv venv
   
```

2. Activate virtual environment:
   
```
bash
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   
```

3. Install dependencies:
   
```
bash
   pip install -r requirements.txt
   
```

4. Run migrations:
   
```
bash
   python manage.py makemigrations
   python manage.py migrate
   
```

5. Create superuser:
   
```bash
   python manage.py createsuperuser
   
```

6. Run development server:
   
```
bash
   python manage.py runserver
   
```

7. Access the website at http://127.0.0.1:8000

## Admin Panel

Access the admin panel at http://127.0.0.1:8000/admin to manage:
- Products
- Categories
- Orders
- Newsletter Subscribers
