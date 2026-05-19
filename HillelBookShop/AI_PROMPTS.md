# AI Prompts

## Prompt 1

Review these Django components for correctness, maintainability, security, and performance:

- `payments.views.PaymentViewSet.confirm`
- `shop.orders.views.order_create`
- `shop.api.views.ProductViewSet`

Focus on:

- exception handling
- ownership / authorization checks
- unnecessary queries
- bulk operations
- readability improvements

Return:

1. issues found
2. concrete recommendations
3. example improved code

## Prompt 2

Generate pytest-django tests for these Django models:

- `accounts.models.UserProfile`
- `shop.models.Product`
- `payments.models.Payment`

Constraints:

- use `factory_boy`
- keep tests small and readable
- cover validations, computed properties, managers, and string behavior
- include only realistic assertions

## Prompt 3

Generate integration tests with pytest-django for these user flows:

- registration
- login
- profile update
- product list/detail
- cart add/update/remove/clear
- order creation
- checkout
- payment intent and payment confirmation

Mock Stripe and email sending where appropriate.

## Prompt 4

Generate concise but useful docstrings for all Django views in this project.

Rules:

- one or two sentences
- describe the responsibility of the view
- no redundant wording

## Prompt 5

Help write an `AI_REVIEW.md` file for a Django project.

For each reviewed component include:

- original code snippet
- AI recommendations
- final code snippet
- why the recommendation was accepted

## Prompt 6

Help write a project README for a Django bookstore application with sections for:

- overview
- features
- setup
- testing
- AI Usage
- coverage
