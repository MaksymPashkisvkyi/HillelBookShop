# Hillel Book Shop

Django-based bookstore project with catalog browsing, cart management, checkout, payments, user accounts, dashboard CRUD, API endpoints, internationalization, async views, and automated test coverage.

## Features

- Product catalog with categories, authors, filters, and detail pages
- Session-based shopping cart
- Order creation and checkout flow
- Stripe-oriented payment integration
- User registration, login, logout, and profile management
- Dashboard CRUD for products
- REST API for categories and products
- English/Ukrainian localization
- Async views for selected read-heavy pages

## Tech Stack

- Python 3.9
- Django 4.2
- Django REST Framework
- django-filter
- factory_boy
- pytest / pytest-django / pytest-cov

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd HillelBookShop
python manage.py migrate
python manage.py runserver
```

## Running Tests

Run the complete test suite:

```bash
../.venv/bin/pytest -q
```

Run tests with coverage:

```bash
../.venv/bin/pytest --cov=. --cov-report=term-missing --cov-report=html -q
```

The HTML coverage report is generated in `test_coverage/`.

## Test Scope

- Unit tests for models, forms, services, and views
- Integration tests for user flows: auth, catalog, cart, order, checkout, payment confirmation, and API access
- Stripe and email interactions mocked in tests

## AI Usage

AI was used in this project for:

- code review of complex views/serializers
- generating and refining tests
- generating docstrings for all view modules
- preparing project documentation

Artifacts:

- [AI_REVIEW.md](/Users/maksym/Hillel%20Projects/HillelBookShop/HillelBookShop/AI_REVIEW.md)
- [AI_PROMPTS.md](/Users/maksym/Hillel%20Projects/HillelBookShop/HillelBookShop/AI_PROMPTS.md)

### Prompts Used

See the full list in [AI_PROMPTS.md](/Users/maksym/Hillel%20Projects/HillelBookShop/HillelBookShop/AI_PROMPTS.md).

## Coverage

Latest full-suite coverage target achieved:

- Total coverage: `>= 60%`
- Current measured coverage during implementation: `88%`

## Notes

- Some local environments may show an `urllib3` warning related to LibreSSL. This is environment-specific and not caused by the project code.
