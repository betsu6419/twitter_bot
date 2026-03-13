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
1. Creates a `tweepy.Client` using four OAuth 1.0a environment variables
2. Calls `client.create_tweet()` (Twitter API v2 `POST /2/tweets`) with the current datetime as the tweet text
3. Prints the tweet ID on success, otherwise prints the error details

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

- `bottle==0.12.23` — lightweight WSGI web framework (web server)
- `tweepy==4.14.0` — Twitter API v2 client with OAuth 1.0a / OAuth 2.0 support

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

- **Python version**: 3.12.8 (specified in `runtime.txt`).
- **Twitter API v2**: `tweet.py` uses `POST /2/tweets` via `tweepy.Client`. The old v1.1 `statuses/update` endpoint is deprecated as of June 2025 and no longer works.
- **Authentication**: OAuth 1.0a (4-key flow) is used. The same four environment variables (`CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_KEY`, `ACCESS_SECRET`) are required. OAuth 1.0a is supported by Twitter API v2 for user-context write operations.
- **Free tier limits**: 1,500 tweets/month at the app level. Do not exceed this with high-frequency scheduling.
- **No test suite exists**: There are no automated tests. Be careful when modifying `tweet.py` to avoid accidentally posting to Twitter during development — mock `tweepy.Client.create_tweet` in tests.
- **No `.env` file or secret management**: Secrets are passed purely via environment variables. Do not introduce any file-based secret storage.
