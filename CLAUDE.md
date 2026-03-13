# CLAUDE.md — Twitter Bot Codebase Guide

## Project Overview

A minimal Python Twitter bot deployed on Heroku. It posts the current datetime to Twitter using the Twitter v1.1 API with OAuth1 authentication, and runs a lightweight web server to satisfy Heroku's dyno requirements.

## Repository Structure

```
twitter_bot/
├── tweet.py          # Core bot logic — posts current datetime to Twitter
├── index.py          # Bottle web server — keeps Heroku dyno alive
├── requirements.txt  # Python package dependencies (pinned versions)
├── runtime.txt       # Heroku Python runtime version (python-3.7.3)
├── Procfile          # Heroku process definition (runs index.py)
└── README.md         # Minimal project title
```

## Key Files

### `tweet.py`
The bot script. When executed, it:
1. Creates an OAuth1 session using four environment variables
2. Calls `POST statuses/update` (Twitter API v1.1) with the current datetime as the tweet text
3. Prints `successed` on HTTP 200, otherwise prints the error status code

The tweet content is Japanese: `"現在は{datetime}"` ("Current time is {datetime}").

### `index.py`
A Bottle WSGI app with a single `GET /` route returning `"Hello World!"`. It binds to `0.0.0.0` on `$PORT` (default 5000). This is the process Heroku keeps running (via `Procfile`); `tweet.py` is invoked separately (e.g., via a Heroku Scheduler add-on).

## Environment Variables

All four are required at runtime. Never commit these values.

| Variable          | Description                          |
|-------------------|--------------------------------------|
| `CONSUMER_KEY`    | Twitter app consumer key             |
| `CONSUMER_SECRET` | Twitter app consumer secret          |
| `ACCESS_KEY`      | Twitter OAuth access token           |
| `ACCESS_SECRET`   | Twitter OAuth access token secret    |
| `PORT`            | Web server port (set automatically by Heroku) |

## Dependencies

Pinned in `requirements.txt`:

- `bottle==0.12.16` — lightweight WSGI web framework (web server)
- `requests==2.18.4` — HTTP client (used by tweet.py)
- `requests-oauthlib==1.2.0` — OAuth1 signing for Twitter requests
- `oauthlib==3.0.1` — OAuth library (dependency of requests-oauthlib)
- `python-twitter==3.5` — Twitter API wrapper (imported transitively)
- `future==0.17.1` — Python 2/3 compatibility layer

## Development Workflow

### Local setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running locally

```bash
# Start the web server
PORT=5000 python index.py

# Run the bot once (requires env vars to be set)
CONSUMER_KEY=... CONSUMER_SECRET=... ACCESS_KEY=... ACCESS_SECRET=... python tweet.py
```

### Heroku deployment

```bash
git push heroku master
```

The `Procfile` starts `index.py` as the `web` dyno. Use the **Heroku Scheduler** add-on to run `tweet.py` on a schedule (e.g., every 10 minutes or hourly).

## Branch Conventions

- `master` — stable/production branch deployed to Heroku
- `develop` — integration branch for feature work (merged to master via PRs)
- Feature branches are merged via pull requests

## Important Constraints

- **Python version**: 3.7.3 (specified in `runtime.txt`). Do not upgrade without testing compatibility with all pinned dependencies.
- **Twitter API v1.1**: `tweet.py` uses the now-deprecated `POST statuses/update` endpoint. Any migration to the v2 API (`POST /2/tweets`) requires replacing `requests-oauthlib` OAuth1 flow with OAuth2 Bearer Token or updating the auth flow accordingly.
- **Dependency versions are pinned**: Do not bump versions without verifying compatibility. The pinned versions are old; test thoroughly in a fresh virtualenv before updating.
- **No test suite exists**: There are no automated tests. Be careful when modifying `tweet.py` to avoid accidentally posting to Twitter during development — use environment variable guards or mock the HTTP call.
- **No `.env` file or secret management**: Secrets are passed purely via environment variables. Do not introduce any file-based secret storage.
