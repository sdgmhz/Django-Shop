# 🛍️ Django eCommerce Platform

A full-featured eCommerce web application built with **Django** and **Django REST Framework**.  
Includes product listings, user authentication, shopping cart, discount system, payment gateway integration, inventory management, admin panel, and a fully-documented RESTful API — perfect for learning and real-world use.

---

## 🚀 Features

- ✅ User registration & authentication
- 🛒 Product catalog with categories
- 🧺 Shopping cart & order system
- 💸 Discount codes & price calculation
- 💳 Payment gateway integration (e.g. Zarinpal / Stripe)
- 📦 Inventory & stock management
- 🔐 Admin dashboard
- 📡 RESTful API for all core features (Django REST Framework)

---

## 🛠️ Tech Stack

- Backend: Django, Django REST Framework
- Database: SQLite / PostgreSQL
- Frontend: HTML/CSS (Template-based) 
- Payment: Custom gateway or 3rd-party API (like Zarinpal, Stripe, etc.)

---



## 🐳 Installation (Docker)

Make sure you have **Docker** and **Docker Compose** installed.

```bash
# Clone the repository
git clone https://github.com/sdgmhz/Django-Shop.git
cd Django-Shop

# Build and run the containers
docker-compose up --build

The app will be available at:
http://localhost:8000/


To apply migrations and create a superuser, open a new terminal and run:
# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser


