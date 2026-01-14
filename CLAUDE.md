# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

使用中文回复
我叫Viking

## Project Overview

This is a minimal Flask web application for a personal watchlist. The project is in early development stages with only a basic welcome page implemented.

## Development Environment

- **Python Version**: 3.13.0
- **Virtual Environment**: `watchlist-venv/`
- **Main Framework**: Flask 3.1.2

## Common Commands

### Running the Application
```bash
flask run
```
or
```bash
python app.py
```

The `.flaskenv` file is available for Flask-specific environment variables.

### Testing
```bash
python test.py
```

## Project Structure

- `app.py` - Main Flask application entry point with routes and view functions
- `test.py` - Simple test script for development purposes
- `.flaskenv` - Flask environment configuration file
- `.env` - Environment variables (not committed to git)
- `watchlist-venv/` - Python virtual environment (not committed to git)

## Code Comments

The codebase includes Chinese comments for learning purposes. When modifying or adding code, maintain consistency with existing comment style.
