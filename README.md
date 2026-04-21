# Django + Stripe Checkout

A Django application that integrates with the Stripe API to create checkout sessions for individual items and multi-item orders.

## 🚀 Live Demo

**Deployed Application:** https://django-stripe-payment-integration.onrender.com

**Admin Panel:** https://django-stripe-payment-integration.onrender.com/admin/
- Username: `admin`
- Password: `Admin2026`

**Test the Payment Flow:**
1. Login to admin panel and create test items
2. Visit `/item/1/` to test single item checkout
3. Use Stripe test card: `4242 4242 4242 4242` (any future expiry, any CVC)

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
| `DJANGO_SUPERUSER_USERNAME` | Auto-created admin username (optional) |
| `DJANGO_SUPERUSER_EMAIL` | Auto-created admin email (optional) |
| `DJANGO_SUPERUSER_PASSWORD` | Auto-created admin password (optional) |

---

## Deployment on Render

This project is deployed on Render using Docker:

### Prerequisites
- GitHub repository
- Render account
- Stripe API keys (test mode)

### Deployment Steps

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push
   ```

2. **Create Web Service on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select "Docker" as environment
   - Configure:
     - **Name:** `django-stripe-payment-integration`
     - **Region:** Choose closest to you
     - **Branch:** `main`
     - **Root Directory:** (leave empty)
     - **Docker Command:** (leave empty - uses entrypoint.sh)

3. **Add Environment Variables:**
   Add all variables from the table above in Render's Environment section.

4. **Deploy:**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Visit your app URL

### Auto-Deploy
The app automatically redeploys when you push to the `main` branch.

### Management Commands
The deployment automatically runs:
- `python manage.py collectstatic --noinput`
- `python manage.py migrate`
- `python manage.py create_default_superuser` (if env vars are set)

---

## Stripe Test Cards

Use these test cards for payment testing:

| Card Number | Description |
|-------------|-------------|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0025 0000 3155` | Requires authentication (3D Secure) |
| `4000 0000 0000 9995` | Declined payment |

Use any future expiry date and any 3-digit CVC.

**More test cards:** https://stripe.com/docs/testing

---

## Admin Access

After running the app and creating a superuser, visit `/admin/` to manage Items, Orders, Discounts, and Taxes.

### Creating Test Data

1. Login to admin panel
2. Add an Item:
   - Name: "Test Product"
   - Description: "A test product for Stripe checkout"
   - Price: 1000 (in cents, = $10.00)
   - Currency: "usd"
3. Visit `/item/1/` to see the checkout page
4. Click "Buy with Stripe" to test the payment flow

### Creating Orders

1. Create multiple items in admin
2. Create an Order and add items to it
3. Optionally add Discount and Tax
4. Visit `/order/1/` to test multi-item checkout

---

## Technical Stack

- **Backend:** Python 3.12, Django 5.1.8
- **Payment:** Stripe API 8.9.0
- **Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Database:** SQLite (development), PostgreSQL-ready
- **Containerization:** Docker
- **Deployment:** Render

---

## Project Structure

```
stripe-django/
├── shop/                          # Main Django app
│   ├── models.py                  # Item, Order, Discount, Tax models
│   ├── views.py                   # Checkout session creation
│   ├── admin.py                   # Admin panel configuration
│   ├── templates/shop/            # HTML templates
│   └── management/commands/       # Custom management commands
├── stripe_project/                # Django project settings
│   ├── settings.py                # Configuration
│   └── urls.py                    # URL routing
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose setup
├── entrypoint.sh                  # Docker entrypoint script
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                      # This file
```
