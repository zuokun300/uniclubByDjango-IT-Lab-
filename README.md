# UniClub Hub

This Django project implements a university club platform with:

- user authentication via Django auth
- database-backed clubs, events, memberships, registrations, and comments
- responsive templates and separate CSS/JavaScript assets
- JavaScript-enhanced event registration and comment posting
- basic unit tests for model and view behaviour

## Run locally in the virtual machine

```bash
cd /home/tianj/IT\ 2/IT
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Open `http://127.0.0.1:8000`.

## Social sign-in options

This project supports two separate third-party sign-in options through `django-allauth`:

- Google sign-in for personal or Google Workspace accounts
- University of Glasgow sign-in through Microsoft 365

The University of Glasgow option is restricted to these email domains by default:

- `glasgow.ac.uk`
- `student.gla.ac.uk`

Set these environment variables before running the server, or place them in a project-level `.env` file for local development:

```bash
export GOOGLE_OAUTH_CLIENT_ID="your-google-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-google-client-secret"
export MICROSOFT_OAUTH_CLIENT_ID="your-microsoft-client-id"
export MICROSOFT_OAUTH_CLIENT_SECRET="your-microsoft-client-secret"
export MICROSOFT_OAUTH_TENANT="organizations"
export DJANGO_SOCIAL_ALLOWED_EMAIL_DOMAINS="glasgow.ac.uk,student.gla.ac.uk"
```

Recommended OAuth redirect URIs:

```text
http://127.0.0.1:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/microsoft/login/callback/
```

When deployed, replace the hostname with your production domain and add the matching callback URLs in Google Cloud and Microsoft Entra.

For local development, the project now auto-loads `.env` from the repository root, so you do not need to run `export` commands each time.

## Run tests

```bash
cd /home/tianj/IT\ 2/IT
source .venv/bin/activate
python3 manage.py test
```

## Notes for coursework evidence

- Accessibility already applied in the UI: skip link, visible focus states, labelled forms, live regions for async status updates, and higher-contrast toggle.
- Sustainability/performance evidence still needs external measurement and screenshots, for example with Lighthouse on the homepage and a club detail page.
- Deployment URL, public repository URL, and PDF report are submission artefacts and are not generated inside this codebase.
