# SportHub

**SportHub** is a full-featured sports club management system built with **Django** and **Django REST Framework (DRF)**.  
It provides role-based authentication, training and nutrition plans, class booking, online payments, and secure APIs following RESTful standards.  
The project also integrates **Celery + Redis** for background task scheduling, such as automatically deactivating inactive users.  

---

## Features

- **Authentication & Security**
  - JWT authentication (DRF + SimpleJWT)
  - Password reset via email
  - Role-based permissions and access control
  - Public IDs with **ShortUUID**
  - Secured user addresses
  - Support for Jalali (Persian) dates

- **User & Role Management**
  - Custom user model with roles (Manager, Coach, Receptionist, Athlete, Admin)
  - Profile info: address, Iranian phone validation, father name, age, profile image
  - Account balance tracking in Rial
  - Status management (Active, Inactive, Expired)
  - Automatic deactivation of users inactive for more than one month (Celery Beat)

- **Training & Nutrition**
  - Personalized training programs for athletes
  - Editable by coaches
  - Diet plans & meal logging

- **Booking & Payments**
  - Reservation system for classes/sessions with limited capacity
  - Cancel/modify reservations by users or receptionists
  - Waiting list support
  - Online payments via **Iranian payment gateway**
  - Invoice generation and membership renewals

- **Background Tasks**
  - **Celery + Redis** for asynchronous jobs
  - Scheduled tasks (Celery Beat) for weekly checks & notifications
  - Signals for automating internal workflows

- **Dashboard & Reports**
  - Manager dashboard with active/inactive members statistics
  - Sales, payment, and booking reports
  - Ongoing coach program tracking

- **Other Highlights**
  - **RESTful APIs** built with Django REST Framework
  - API documentation with **drf-spectacular (Swagger/OpenAPI)**
  - Image handling via **Pillow**
  - Responsive design, PWA-ready
  - Best practices in Django project structure and modular design
  - Multi-language support (i18n)

---

## Tech Stack

- **Python**
- **Django**
- **Django REST Framework**
- **Celery + Celery Beat**
- **Redis**
- **PostgreSQL**
- **Docker**
- **shortuuidfield**
- **django-phonenumber-field**
- **drf-spectacular**
- **Pillow**
- **django-filter**
---

## Installation

```bash
git clone https://github.com/MohammadSadeghiyan/sporthub.git
cd sporthub

# Create virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
