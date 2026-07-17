# Grooming studio chat helper

[![CI](https://github.com/hu553in/grooming-studio-chat-helper/actions/workflows/ci.yml/badge.svg)](https://github.com/hu553in/grooming-studio-chat-helper/actions/workflows/ci.yml)

Telegram bot with reusable message templates for a grooming studio.

## What it does

- Shows an inline menu from `/start`
- Sends booking confirmation text after date and time input
- Sends prepared answers for reviews, prices, nail care, adaptation, and questionnaire links

## Requirements

- Python 3.14+
- `uv`
- Bun for repository tooling
- Telegram bot token
- Optional: Docker for deployment

## Setup

Local checkout:

```bash
make install-deps
```

Docker image:

```bash
docker build -t grooming-studio-chat-helper .
```

CI publishes `ghcr.io/hu553in/grooming-studio-chat-helper`; `latest` follows `main`, while `sha-*`
tags are immutable.

## Configuration

| Name                 | Required | Description        |
| -------------------- | -------- | ------------------ |
| `TELEGRAM_BOT_TOKEN` | Yes      | Telegram bot token |

## Usage

Local:

```bash
TELEGRAM_BOT_TOKEN=123456:replace-me uv run python3 bot.py
```

Docker:

```bash
docker run --rm -e TELEGRAM_BOT_TOKEN=123456:replace-me grooming-studio-chat-helper
```

## Runtime behavior

- Booking draft state is stored in process memory
- Static message templates live in `bot.py`
- Restarting the process clears in-progress booking drafts
- No database or persistent storage is used

## Development

```bash
make install-deps
uv run prek install
make check
make check-fix
```

Focused checks:

```bash
make lint
make lint-fix
make check-types
make check-deps
make check-vulns
make check-unused
make check-security
```
