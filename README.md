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

## Google sign-in for University of Glasgow accounts

This project supports Google OAuth login through `django-allauth`.
Only University of Glasgow email domains are allowed by default:

- `glasgow.ac.uk`
- `student.gla.ac.uk`

Set these environment variables before running the server:

```bash
export GOOGLE_OAUTH_CLIENT_ID="your-google-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-google-client-secret"
export DJANGO_SOCIAL_ALLOWED_EMAIL_DOMAINS="glasgow.ac.uk,student.gla.ac.uk"
```

Recommended Google OAuth redirect URI:

```text
http://127.0.0.1:8000/accounts/google/login/callback/
```

When deployed, replace the hostname with your production domain and add the same callback URL in the Google Cloud console.

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
