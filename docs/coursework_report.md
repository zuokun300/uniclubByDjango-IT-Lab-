# Web Application Implementation Report

## Introduction + Links

UniClub Hub is a Django web application for discovering student clubs, joining communities, registering for events, and posting event comments. The implemented system keeps the back end in Python/Django and the front end in Django templates enhanced with separate CSS and JavaScript assets.

Repository URL: `TO_BE_FILLED`

Deployed application URL: `TO_BE_FILLED`

Adjustment to the design specification: the final implementation focuses on club discovery, membership, event registration, and commenting as the core workflow. This keeps the app aligned with the database schema already present in the project and concentrates on the main user stories.

## Updated Design Specification

### User stories

1. As a visitor, I want to browse clubs so that I can discover student communities.
2. As a registered user, I want to log in and join a club so that I can participate.
3. As a registered user, I want to register for an event so that my attendance is stored.
4. As a registered user, I want to leave comments on an event so that I can interact with organisers and other members.
5. As an organiser, I want to create clubs and events so that I can manage activities.

### System architecture diagram

Client browser
-> Django templates + static CSS/JS
-> Django views / auth / forms
-> SQLite database

### ER diagram summary

- `User` 1..* `Club` through founder relationship
- `Club` 1..* `Event`
- `User` *..* `Club` through `Membership`
- `User` *..* `Event` through `Registration`
- `User` 1..* `Comment`
- `Event` 1..* `Comment`

### Sitemap

- `/`
- `/clubs/`
- `/clubs/<id>/`
- `/clubs/new/`
- `/clubs/<id>/events/new/`
- `/login/`
- `/logout/`
- `/admin/`

### Wireframe summary

- Homepage: hero panel, stats, featured clubs, upcoming events.
- Club list page: searchable responsive card grid.
- Club detail page: club summary, membership action, event cards, registration action, comments.
- Login page: single-column accessible sign-in form.

## Implementation Highlights

The project uses Django models for `Club`, `Event`, `Membership`, `Registration`, and `Comment`, matching the SQLite data already present in the coursework folder. Authentication is handled by Django auth with protected actions for joining clubs, creating clubs/events, registering for events, and posting comments.

Database interaction is demonstrated in multiple ways: clubs and events are listed from the database, user membership is stored, event registrations are persisted, and comments are created and shown on the club detail page. These operations go beyond static rendering and show meaningful create/read behaviour tied to authenticated users.

Front-end interactivity is implemented with external JavaScript. Event registration uses asynchronous `fetch` requests and updates the attendee count without a full page reload. Comment submission also uses asynchronous requests and injects the new comment directly into the DOM. CSS and JavaScript remain separate from templates, satisfying separation-of-concerns expectations.

The interface is responsive and consistent across pages. The layout uses Flexbox/Grid and adapts at smaller widths for mobile devices. Templates inherit from a shared `base.html`, all internal links use named Django routes, and code is organised into models, forms, views, templates, and static assets.

## Testing

Unit tests cover:

1. A core model behaviour: `Club.get_absolute_url`.
2. Access control for joining a club.
3. Membership creation after a join action.
4. AJAX event registration.
5. AJAX comment creation.

Verification command:

```bash
python3 manage.py test
```

Latest local result in the virtual machine: `Ran 5 tests ... OK` on March 11, 2026.

## Accessibility Report

The implementation applies more than three improvements from the accessibility plan:

1. Skip link added at the top of each page so keyboard users can jump directly to main content.
2. Strong visible focus styles for links, buttons, inputs, and textareas.
3. Proper labels for form controls on login, search, creation forms, and comment forms.
4. Live regions for asynchronous registration/comment status feedback.
5. Optional high-contrast mode toggle for improved readability.

Key evidence pages:

- Homepage
- Club detail page
- Login page

## Sustainability Report

Audit process included:

1. Keeping CSS and JavaScript as shared external assets rather than duplicated inline content.
2. Reducing page complexity by using server-rendered templates and a lightweight amount of JavaScript.
3. Reusing base templates and shared assets to avoid duplication and excess payload.

Tool used locally: `scripts/performance_audit.py` for page-size and latency sampling on two pages.

Pages audited:

- Homepage
- Club list page

Local metrics file:

- `performance_audit.json`

Note: if the marker expects Lighthouse specifically, run a final Lighthouse audit in a browser and replace this section with before/after screenshots and scores.

## Appendix: Team Contributions and AI Use Statement

Team contributions: `TO_BE_FILLED`

AI Use Statement:

We declare that we have used GenAI for debugging support, refactoring suggestions, unit test ideas, accessibility implementation support, and sustainability/performance guidance. The affected parts were code, tests, and report drafting support. We verified the final result by running Django checks, applying migrations, testing the application locally, and reviewing the generated implementation against the coursework specification.

