# Azure Web App Deployment Guide

## Prerequisites
1. Azure SQL Managed Instance or Azure SQL Database set up
2. Azure Web App created (Python 3.11 runtime)
3. Virtual Network configured (if using Managed Instance)

## Azure Web App Configuration

### 1. Application Settings (Environment Variables)
Add these in Azure Portal -> Web App -> Configuration -> Application Settings:

```
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=False
DJANGO_SETTINGS_MODULE=portfolio_project.settings

# Azure SQL Configuration
AZURE_SQL_SERVER=your-managed-instance-name.your-region.database.windows.net
AZURE_SQL_DATABASE=portfolio_db
AZURE_SQL_USER=your-sql-admin-user
AZURE_SQL_PASSWORD=your-sql-admin-password
AZURE_SQL_PORT=1433

# Azure Web App Specific
WEBSITE_HOSTNAME=your-webapp-name.azurewebsites.net
ALLOWED_HOSTS=your-webapp-name.azurewebsites.net,.azurewebsites.net
```

### 2. Startup Command
Set this in Azure Portal -> Web App -> Configuration -> General Settings -> Startup Command:
```
startup.sh
```

### 3. Deployment
#### Option A: GitHub Actions (Recommended)
1. Connect your GitHub repository to Azure Web App
2. Azure will automatically create a GitHub Action workflow
3. Push changes to trigger deployment

#### Option B: Local Git Deployment
1. Set up local Git deployment in Azure Portal
2. Add Azure remote: `git remote add azure <azure-git-url>`
3. Deploy: `git push azure main`

#### Option C: ZIP Deployment
1. Create ZIP of your project
2. Use Azure CLI: `az webapp deployment source config-zip --resource-group myResourceGroup --name myAppName --src project.zip`

## Network Configuration (for Managed Instance)

### 1. Virtual Network Integration
- Enable VNet integration in Azure Web App
- Configure subnet delegation for Web Apps
- Ensure NSG rules allow Web App to SQL Managed Instance communication

### 2. Private DNS (if using private endpoints)
- Configure private DNS zone for SQL Managed Instance
- Link private DNS zone to Web App VNet

## Database Setup

### 1. Initial Setup
After first deployment, run these commands in Azure Cloud Shell or local Azure CLI:

```bash
# Connect to your Web App
az webapp ssh --resource-group your-resource-group --name your-webapp-name

# Run migrations
python manage.py migrate

# Import GitHub projects
python manage.py import_github_projects

# Create superuser (optional)
python manage.py createsuperuser
```

### 2. SQL Managed Instance Firewall
- Add Web App's outbound IPs to SQL Managed Instance NSG
- Or use VNet integration for private connectivity

## Monitoring and Troubleshooting

### 1. Application Insights
- Enable Application Insights for monitoring
- Check logs in Azure Portal -> Web App -> Monitoring -> Log stream

### 2. Common Issues
- **500 Errors**: Check application logs for Django errors
- **Database Connection**: Verify connection strings and firewall rules
- **Static Files**: Ensure STATIC_ROOT is configured correctly
- **CORS Issues**: Check ALLOWED_HOSTS configuration

### 3. Performance Optimization
- Enable Always On for production
- Scale up App Service Plan as needed
- Consider Azure CDN for static files

## Security Considerations

1. **Environment Variables**: Store sensitive data in Azure Key Vault
2. **HTTPS**: Enable HTTPS-only mode
3. **Authentication**: Consider Azure AD integration
4. **Network Security**: Use VNet integration and private endpoints
5. **Database Security**: Enable encryption at rest and in transit

## Cost Optimization

1. **App Service Plan**: Choose appropriate tier (B1, S1, P1V2, etc.)
2. **Auto-scaling**: Configure based on usage patterns
3. **SQL Database**: Use appropriate service tier and compute size
4. **Monitoring**: Set up alerts for resource usage and costs

## Post-Deployment Checklist

- [ ] Verify application loads correctly
- [ ] Test database connectivity
- [ ] Check all pages work (home, projects, blog, admin)
- [ ] Verify static files load properly
- [ ] Test form submissions and user interactions
- [ ] Monitor application performance and errors
- [ ] Set up backup strategy for database
- [ ] Configure domain and SSL certificate (if custom domain)