# Azure SQL Server Connection Troubleshooting Guide

## Current Issue: Login Timeout Expired

Based on your Azure SQL Server configuration, here's what we know:

### 🔍 **Azure Server Configuration:**
- **Server**: portfoli.database.windows.net
- **Admin Login**: CloudSAd6e2c7cf
- **Azure AD Only**: TRUE (this is important!)
- **Public Access**: Enabled
- **Your User**: mysterious3115_gmail.com#EXT#@mysterious3115gmail.onmicrosoft.com

### 🚫 **Current Problem:**
Getting `Login timeout expired` error, which typically indicates one of these issues:

## 1. **FIREWALL ISSUE** (Most Likely)
Your IP address `49.43.226.137` is not allowed to connect to the Azure SQL Server.

**Solution**: Add your IP to Azure SQL Server firewall rules:

1. Go to Azure Portal → SQL Servers → portfoli → Security → Networking
2. Under "Firewall rules", click "Add a firewall rule"
3. Add your current IP address: `49.43.226.137`
4. Name: `Local Development`
5. Start IP: `49.43.226.137`
6. End IP: `49.43.226.137`
7. Click "Save"

**OR** Allow Azure services:
- Check "Allow Azure services and resources to access this server"

## 2. **AZURE AD AUTHENTICATION**
Your server is configured for **Azure AD Only Authentication**.

**Current Django Configuration (Correct):**
```python
'OPTIONS': {
    'driver': 'ODBC Driver 18 for SQL Server',
    'extra_params': 'Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=60;Login Timeout=60;Authentication=ActiveDirectoryPassword;'
},
```

**Environment Variables:**
```bash
export DB_HOST="portfoli.database.windows.net"
export DB_NAME="portfolio"
export DB_USER="mysterious3115_gmail.com#EXT#@mysterious3115gmail.onmicrosoft.com"
export DB_PASSWORD="Mantha@2005"
```

## 3. **VERIFY PERMISSIONS**
Make sure your Azure AD user has access to the database:

1. Go to Azure Portal → SQL databases → portfolio → Query editor
2. Login with your Azure AD account
3. Run this SQL to grant permissions:
   ```sql
   CREATE USER [mysterious3115_gmail.com#EXT#@mysterious3115gmail.onmicrosoft.com] FROM EXTERNAL PROVIDER;
   ALTER ROLE db_owner ADD MEMBER [mysterious3115_gmail.com#EXT#@mysterious3115gmail.onmicrosoft.com];
   ```

## 4. **TEST CONNECTION**
Use this script to test your connection:

```python
import pyodbc
server = 'portfoli.database.windows.net'
database = 'portfolio'
username = 'mysterious3115_gmail.com#EXT#@mysterious3115gmail.onmicrosoft.com'
password = 'Mantha@2005'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Authentication=ActiveDirectoryPassword;Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=60;'

try:
    conn = pyodbc.connect(conn_str)
    print('✅ Connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Connection failed: {e}')
```

## Next Steps (In Order):
1. **FIRST**: Fix the firewall issue in Azure Portal (add IP: 49.43.226.137)
2. **THEN**: Verify user permissions in the database
3. **FINALLY**: Test Django migrations

## Common Error Messages:
- `Login timeout expired` → Firewall issue  
- `Login failed` → Authentication/permission issue  
- `Cannot open server` → Wrong server name

## After Fixing Firewall:
Once the firewall is configured, run:
```bash
python manage.py migrate
```