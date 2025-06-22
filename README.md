# Letraz Discord Bot

A Discord bot that provides announcement webhooks and automated member role assignment functionality.

## Features

- **Automated Role Assignment**: Automatically assigns a specified role to new members when they join the server
- **Announcement Webhooks**: REST API endpoint for sending rich announcements to Discord channels
- **Bearer Token Authentication**: Secure API access with configurable bearer tokens
- **Rich Embeds**: Support for formatted messages with titles, descriptions, links, and images

## Architecture

The codebase has been refactored into a modular structure for better maintainability:

```
letraz-discord-bot/
├── main.py                 # Entry point
├── config.py              # Configuration management
├── bot/                   # Discord bot functionality
│   ├── __init__.py
│   ├── discord_bot.py     # Bot initialization
│   └── events.py          # Event handlers
├── api/                   # Flask web API
│   ├── __init__.py
│   ├── flask_app.py       # Flask app setup
│   ├── routes.py          # API endpoints
│   ├── auth.py            # Authentication
│   └── models.py          # Data models
└── apis/                  # API testing (Bruno)
    └── bruno.json
```

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Environment variables** (create a `.env` file):
   ```env
   DISCORD_BOT_TOKEN=your_discord_bot_token
   BEARER_TOKEN=your_api_bearer_token
   DEFAULT_CHANNEL_ID=your_default_channel_id
   ROLE_ID=your_auto_assign_role_id
   
   # Optional configuration
   FLASK_HOST=0.0.0.0
   FLASK_PORT=4000
   BOT_PREFIX=!
   BOT_ACTIVITY_NAME=with my server 💪
   ```

3. **Run the bot**:
   ```bash
   python main.py
   ```

## API Usage

### Announcement Endpoint

**POST** `/main/announcement`

**Headers**:
```
Authorization: Bearer YOUR_BEARER_TOKEN
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Announcement Title",
  "message_content": "Your announcement message here",
  "channel_id": "123456789012345678",  // Optional, uses DEFAULT_CHANNEL_ID if not provided
  "learn_more": "https://example.com",  // Optional link
  "image_url": "https://example.com/image.png"  // Optional image
}
```

**Response**:
```json
{
  "status": "Success"
}
```

### Health Check

**GET** `/health`

Returns the health status of the API service.

## Development

The modular structure makes it easy to:

- **Add new bot commands**: Extend `bot/discord_bot.py`
- **Add new events**: Add handlers to `bot/events.py`
- **Add new API endpoints**: Add routes to `api/routes.py`
- **Modify authentication**: Update `api/auth.py`
- **Change configuration**: Update `config.py`

## Error Handling

The bot includes comprehensive error handling:
- Configuration validation on startup
- API request validation
- Discord API error handling
- Graceful fallbacks for missing roles/channels
