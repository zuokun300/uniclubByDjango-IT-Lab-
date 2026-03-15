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
