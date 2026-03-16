# UniClub Hub

UniClub Hub is a Django web application for university societies and student clubs. It gives students one place to browse clubs, check upcoming events, join activities, and take part in discussions. Club founders can manage their own club pages and events through the same system.

## What it does

- user registration, login, and logout with Django authentication
- Google sign-in for general accounts
- Microsoft sign-in for University of Glasgow email accounts
- club, event, membership, registration, and comment management
- responsive templates with separate CSS and JavaScript assets
- JavaScript-enhanced interactions for event registration and comments
- Django tests covering core model and view behaviour

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Apply migrations.
4. Start the development server.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Social login setup

For local development, copy `.env.example` to `.env` and fill in your OAuth credentials:

```bash
cp .env.example .env
```

The project loads `.env` automatically when Django starts, so you do not need to export the variables manually every time.

### Required variables

- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `MICROSOFT_OAUTH_CLIENT_ID`
- `MICROSOFT_OAUTH_CLIENT_SECRET`
- `MICROSOFT_OAUTH_TENANT`
- `DJANGO_SOCIAL_ALLOWED_EMAIL_DOMAINS`
- `DJANGO_ALLOWED_HOSTS`

By default, the Microsoft sign-in flow accepts these University of Glasgow domains:

- `glasgow.ac.uk`
- `student.gla.ac.uk`

### Local OAuth callback URLs

Configure these callback URLs in Google Cloud and Microsoft Entra for local testing:

```text
http://127.0.0.1:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/microsoft/login/callback/
```

For deployment, replace `127.0.0.1:8000` with your production domain and register the matching HTTPS callback URLs with both providers.

## Running tests

```bash
source .venv/bin/activate
python3 manage.py test
```

## Deployment

The project is deployed at [https://kzbyzk.it.com](https://kzbyzk.it.com).

If you want to deploy your own copy, make sure the following are configured correctly:

- production `ALLOWED_HOSTS`
- HTTPS and reverse proxy settings
- Google and Microsoft OAuth callback URLs
- environment variables for secrets and provider credentials
