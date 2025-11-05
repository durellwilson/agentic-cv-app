# Railway Deployment Guide

## Quick Deploy Steps:

1. **Login to Railway:**
   ```bash
   railway login
   ```

2. **Initialize Project:**
   ```bash
   railway init
   ```

3. **Deploy:**
   ```bash
   railway up
   ```

## Alternative: One-Click Deploy

Click this button to deploy directly:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/agentic-cv-app)

## Manual Setup:

1. Go to https://railway.app
2. Connect your GitHub account
3. Import repository: `durellwilson/agentic-cv-app`
4. Railway will auto-detect the Dockerfile
5. Deploy automatically

## Environment Variables:
- `PORT`: Auto-set by Railway
- `FLASK_ENV`: production

Your app will be live at: `https://your-app-name.railway.app`
