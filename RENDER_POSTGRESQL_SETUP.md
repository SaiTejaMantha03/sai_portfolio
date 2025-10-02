# Render PostgreSQL Setup Instructions

## The Problem
- SQLite database gets wiped on every Render deployment
- Tables are lost, causing "no such table" errors
- Need persistent PostgreSQL database

## Solution: Add PostgreSQL to Render

### Step 1: Create PostgreSQL Database on Render
1. Go to Render Dashboard
2. Click "New +" button
3. Select "PostgreSQL"
4. Choose:
   - Name: `sai-portfolio-db`
   - Database: `portfolio_db`
   - User: `portfolio_user`
   - Region: Same as your web service
   - Plan: Free tier

### Step 2: Get Database URL
After creating the database, Render will provide:
- Internal Database URL (for connecting from your web service)
- External Database URL (for external connections)

Copy the **Internal Database URL** - it looks like:
```
postgresql://portfolio_user:password@dpg-xxxxx-a.oregon-postgres.render.com/portfolio_db
```

### Step 3: Add Environment Variable to Web Service
1. Go to your Web Service in Render Dashboard
2. Go to "Environment" tab
3. Add environment variable:
   - Key: `DATABASE_URL`
   - Value: [paste the Internal Database URL from step 2]

### Step 4: Deploy
Once you add the DATABASE_URL environment variable, Render will automatically redeploy your service with PostgreSQL.

## Why This Fixes Everything
- PostgreSQL data persists between deployments
- Your Django settings already check for DATABASE_URL
- All migrations will run once and create permanent tables
- No more "no such table" errors

## Current Status
Your code is already configured to use PostgreSQL when DATABASE_URL is present:

```python
elif 'DATABASE_URL' in os.environ:
    # PostgreSQL production database (Render or other providers)
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
```

Just need to add the DATABASE_URL environment variable to use PostgreSQL instead of SQLite.