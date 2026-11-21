# Django E-Commerce

A full-stack e-commerce web application built with Django (MVT architecture) as the final project of the **ITI Web Development Using Python & Generative AI** program.

> **Note:** This is an educational project. It has no online payment system and is not intended for production use.

## Features

- **Authentication:** register and log in with email, logout, and a profile page. Custom user model with Egyptian mobile number validation.
- **Catalog:** categories and products with search, filtering by category and price, and sorting.
- **Shopping cart:** session-based cart (add, increase, decrease, remove, clear).
- **Checkout:** requires login, re-validates stock, creates the order, and decreases stock automatically.
- **Order history:** customers can view only their own orders.
- **Admin panel:** manage categories, products, and orders through Django Admin.

## Project Structure

| App | Responsibility |
|-----|----------------|
| `accounts` | Registration, email login, logout, profile, custom user model |
| `shop` | Categories, products, search, filtering, and sorting |
| `cart` | Session-based shopping cart |
| `orders` | Checkout, order creation, and order history |

## Tech Stack

Python, Django, SQLite, HTML, CSS

## Getting Started

**Requirements:** Python 3.10+ and pip.

### 1. Clone the repository
```bash
git clone https://github.com/youssef-m-ashour/django-ecommerce.git
cd django-ecommerce
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
```
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables (optional for local use)
```bash
cp .env.example .env
```
Edit `.env` and set your own `DJANGO_SECRET_KEY`. If no `.env` file exists, development defaults are used.

### 5. Set up the database
```bash
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
```
`seed_data` adds sample categories and products. `createsuperuser` creates your own admin account.

### 6. Run the server
```bash
python manage.py runserver
```
Open http://127.0.0.1:8000/ in your browser. The admin panel is at http://127.0.0.1:8000/admin/.

## Usage

- Register a customer account at `/accounts/register/`. The mobile number must be a valid Egyptian number (11 digits starting with 010, 011, 012, or 015, e.g. `01012345678`).
- Browse products, search, filter, and add items to the cart.
- Check out (login required) and view your orders under **My Orders**.

## Security Notes

Secrets are loaded from environment variables and `.env` is excluded from version control. For any real deployment, set a strong `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=False`, and configure `DJANGO_ALLOWED_HOSTS`.

## Author

**Youssef Ashour** — AI student at the Faculty of Computers and Information, Suez Canal University.
[LinkedIn](https://www.linkedin.com/in/youssef-m-ashour) · [GitHub](https://github.com/youssef-m-ashour)
