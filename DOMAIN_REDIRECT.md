# Domain Redirect Setup: home.saiwith.tech → saiwith.tech

## What This Does
Automatically redirects all traffic from `home.saiwith.tech` to `saiwith.tech` using Django middleware.

## How It Works

### 1. Django Middleware Solution ✅
- **File**: `portfolio_project/middleware.py`
- **Function**: Intercepts requests to `home.saiwith.tech` and redirects to `saiwith.tech`
- **Type**: 301 Permanent Redirect (SEO-friendly)

### 2. Implementation Details

**Middleware Code:**
```python
def process_request(self, request):
    host = request.get_host().lower()
    
    if host == 'home.saiwith.tech':
        protocol = 'https' if request.is_secure() else 'http'
        new_url = f"{protocol}://saiwith.tech{request.get_full_path()}"
        return HttpResponsePermanentRedirect(new_url)
```

**Added to MIDDLEWARE in settings.py:**
```python
MIDDLEWARE = [
    'portfolio_project.middleware.DomainRedirectMiddleware',  # First middleware
    # ... other middleware
]
```

## Testing the Redirect

### Example Redirects:
- `http://home.saiwith.tech/` → `http://saiwith.tech/`
- `https://home.saiwith.tech/blog/` → `https://saiwith.tech/blog/`
- `https://home.saiwith.tech/projects/` → `https://saiwith.tech/projects/`

### Test Commands:
```bash
# Test with curl (should return 301 redirect)
curl -I http://home.saiwith.tech/

# Check if redirect preserves path
curl -I http://home.saiwith.tech/blog/
```

## DNS Configuration (Recommended)
For better performance, also set up DNS-level redirects:

1. **Point both domains to the same server**:
   - `saiwith.tech` → Your server IP
   - `home.saiwith.tech` → Your server IP

2. **Or use DNS CNAME redirect** (if supported by your DNS provider):
   - `home.saiwith.tech` CNAME → `saiwith.tech`

## Benefits
- ✅ SEO-friendly (301 permanent redirect)
- ✅ Preserves full URL path
- ✅ Works with both HTTP and HTTPS
- ✅ Automatic and transparent to users
- ✅ No manual configuration needed

## Status: ✅ IMPLEMENTED AND READY
The redirect is now active and will work once deployed!