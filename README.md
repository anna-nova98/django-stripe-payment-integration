# Django + Stripe Checkout

A Django application that integrates with the Stripe API to create checkout sessions for individual items and multi-item orders.

## Features

- `Item` model with `name`, `description`, `price`, and `currency` fields
- `Order` model combining multiple items into a single Stripe Checkout session
- `Discount` and `Tax` models attachable to orders (reflected in Stripe Checkout)
- Two Stripe keypairs — one for USD, one for EUR — selected automatically based on item currency
- Django Admin panel for all models
- Docker support
- Environment variable configuration

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/item/<id>/` | HTML page with item info and Buy button |
| GET | `/buy/<id>/` | Returns `{"id": "<stripe_session_id>"}` for an Item |
| GET | `/order/<id>/` | HTML page with order summary and Pay button |
| GET | `/buy/order/<id>/` | Returns `{"id": "<stripe_session_id>"}` for an Order |
| GET | `/success/` | Post-payment success page |

## Quick Start (local)

### 1. Clone & set up environment

```bash
git clone https://github.com/<your-username>/django-stripe.git
cd django-stripe
cp .env.example .env
# Fill in your Stripe keys in .env
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start the development server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/admin/` to add items, then open `http://localhost:8000/item/1/`.

---

## Docker

```bash
cp .env.example .env
# Fill in your Stripe keys in .env
docker-compose up --build
```

The app will be available at `http://localhost:8000`.

To create a superuser inside Docker:

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` or `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts |
| `STRIPE_PUBLIC_KEY_USD` | Stripe publishable key for USD |
| `STRIPE_SECRET_KEY_USD` | Stripe secret key for USD |
| `STRIPE_PUBLIC_KEY_EUR` | Stripe publishable key for EUR |
| `STRIPE_SECRET_KEY_EUR` | Stripe secret key for EUR |

---

## Stripe Test Cards

Use `4242 4242 4242 4242` with any future expiry and any CVC for successful test payments.

---

## Admin Access

After running the app and creating a superuser, visit `/admin/` to manage Items, Orders, Discounts, and Taxes.
