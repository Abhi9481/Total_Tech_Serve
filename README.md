# Total Tech Serve — Company Website

## Project Structure
```
totaltech/
├── app.py                  # Flask application + database models
├── generate_logo.py        # Generate SVG logo
├── requirements.txt        # Python dependencies
├── run_mac_linux.sh        # Start script for Mac/Linux
├── run_windows.bat         # Start script for Windows
├── instance/
│   └── totaltech.db        # SQLite database (auto-created)
├── static/
│   ├── css/style.css       # Main stylesheet
│   └── images/logo.svg     # Generated logo
└── templates/
    ├── base.html           # Layout with navbar + footer
    ├── index.html          # Homepage
    ├── services.html       # Services page
    ├── about.html          # About Us page
    ├── contact.html        # Contact form (saves to DB)
    └── admin.html          # HR Admin panel
```

## Setup & Run

### 1. Install dependencies
```bash
pip install flask flask-sqlalchemy
```

### 2. Generate the logo
```bash
python generate_logo.py
```

### 3. Run the website
```bash
python app.py
```
Visit: http://localhost:5000

---

## Pages

| URL | Page |
|-----|------|
| / | Homepage |
| /services | All Services |
| /about | About Us |
| /contact | Contact Form |
| /admin | HR Admin Panel |

---

## HR Admin Panel — /admin

The admin panel shows all contact form submissions with:
- **Required fields**: Name, Email, Phone, Message
- **Editable fields** (HR can fill in): Company, Designation, City, Service Interest
- **Status tracking**: New → Contacted → Closed
- Click any editable cell to type in it, then click Save

---

## Database

SQLite database at `instance/totaltech.db`. Fields in the Contact table:
- `full_name`, `email`, `phone`, `message` — required
- `company`, `designation`, `city`, `service_interest` — optional (fillable by HR)
- `status` — new / contacted / closed
- `submitted_at` — timestamp

---

## ================================================
## HOW TO GET YOUR WEBSITE ON GOOGLE
## ================================================

### Step 1: Choose Your Domain Name

**Recommended: totaltechserve.com** (or totaltechserve.in for India-specific)

Comparison:
| | .com | .in |
|-|-|-|
| Global reach | ✅ Best | ⚠️ Limited |
| India trust | ✅ Trusted globally | ✅ Stronger local signal |
| Price | ~₹800–1200/year | ~₹600–900/year |
| Recommendation | **Use .com** | Good backup/redirect |

**Best practice**: Buy both `totaltechserve.com` AND `totaltechserve.in`.
- Host on `.com` (primary)
- Redirect `.in` → `.com`

Where to buy: GoDaddy, Namecheap, Hostinger, BigRock (India)

---

### Step 2: Choose Web Hosting

For a Flask/Python website, use:
- **PythonAnywhere** (easiest, free tier available): pythonanywhere.com
- **Render.com** (free tier, good for Flask): render.com
- **DigitalOcean App Platform** (~$5/month): digitalocean.com
- **AWS / Google Cloud** (scalable, more complex)

Recommendation for starting out: **Render.com** or **PythonAnywhere**

---

### Step 3: Deploy Your Website

#### Option A: PythonAnywhere
1. Create account at pythonanywhere.com
2. Upload your project files
3. Set up a WSGI file pointing to your `app.py`
4. Add your custom domain in the dashboard

#### Option B: Render.com
1. Push code to GitHub
2. Connect GitHub to Render
3. Select "Web Service" → Python
4. Set start command: `gunicorn app:app`
5. Add `gunicorn` to requirements.txt

---

### Step 4: Submit to Google Search Console

1. Go to: https://search.google.com/search-console
2. Click "Add Property" → enter your domain (e.g. totaltechserve.com)
3. Verify ownership (add a DNS TXT record via your registrar)
4. Click "Request Indexing" on your homepage URL
5. Submit your sitemap: https://totaltechserve.com/sitemap.xml

Add a sitemap route to app.py:
```python
@app.route('/sitemap.xml')
def sitemap():
    from flask import Response
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://totaltechserve.com/</loc><priority>1.0</priority></url>
  <url><loc>https://totaltechserve.com/services</loc><priority>0.9</priority></url>
  <url><loc>https://totaltechserve.com/about</loc><priority>0.8</priority></url>
  <url><loc>https://totaltechserve.com/contact</loc><priority>0.8</priority></url>
</urlset>"""
    return Response(xml, mimetype='application/xml')
```

---

### Step 5: Local SEO (Show in Google Maps & Local Search)

1. Go to: https://business.google.com
2. Create a **Google Business Profile** for Total Tech Serve
3. Add:
   - Business name, address, phone
   - Category: "Computer Repair Service" or "IT Services"
   - Service area: Bengaluru
   - Photos of your office/team
   - Business hours
4. Ask clients to leave Google Reviews — this greatly boosts local ranking

---

### Step 6: SEO Already Built Into This Website

Your website already has:
✅ Meta title and description on every page
✅ JSON-LD structured data (LocalBusiness schema)
✅ Open Graph tags (for sharing on WhatsApp, LinkedIn)
✅ Semantic HTML (proper h1, h2, nav, main, footer tags)
✅ Canonical URLs
✅ Mobile-responsive design (Google ranks mobile-first)
✅ Fast-loading (no heavy JS frameworks)
✅ Keyword-rich content matching search terms

---

### .com vs .in — Final Answer

**Use totaltechserve.com** as your primary domain.
- More professional for enterprise clients
- Works globally if you ever expand
- Equally trusted in India
- Buy totaltechserve.in as a backup and redirect it to .com
