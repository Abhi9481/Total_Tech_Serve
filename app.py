from flask import Flask, render_template, request, jsonify, Response, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
import os
import hashlib

OWNER_EMAIL    = 'totaltechserve@totaltechserve.com'
OWNER_PHONE    = '+91 98869 99575 / +91 96866 34787'
OWNER_WHATSAPP = '919886999575'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'TotalTech@2024'

app = Flask(__name__)
app.config['SECRET_KEY']                  = 'totaltech-admin-secret-2024-xyz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME']  = timedelta(hours=8)

database_url = os.environ.get('DATABASE_URL', '')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url if database_url else 'sqlite:///totaltech.db'

db = SQLAlchemy(app)

class Contact(db.Model):
    __tablename__ = 'contacts'
    id               = db.Column(db.Integer, primary_key=True)
    full_name        = db.Column(db.String(100), nullable=False)
    email            = db.Column(db.String(120), nullable=False)
    phone            = db.Column(db.String(20),  nullable=False)
    company          = db.Column(db.String(100))
    designation      = db.Column(db.String(100))
    service_interest = db.Column(db.String(100))
    message          = db.Column(db.Text)
    city             = db.Column(db.String(60))
    submitted_at     = db.Column(db.DateTime, default=datetime.utcnow)
    status           = db.Column(db.String(20), default='new')
    notes            = db.Column(db.Text)
    follow_up_date   = db.Column(db.String(20))
    last_contacted   = db.Column(db.String(30))
    priority         = db.Column(db.String(10), default='normal')
    history          = db.relationship('ContactHistory', backref='contact', lazy=True, cascade='all, delete-orphan')
    def to_dict(self):
        return {'id':self.id,'full_name':self.full_name,'email':self.email,'phone':self.phone,
                'company':self.company or '','designation':self.designation or '',
                'service_interest':self.service_interest or '','message':self.message or '',
                'city':self.city or '','submitted_at':self.submitted_at.strftime('%d %b %Y, %I:%M %p'),
                'status':self.status,'notes':self.notes or '','follow_up_date':self.follow_up_date or '',
                'last_contacted':self.last_contacted or '','priority':self.priority or 'normal',
                'history':[h.to_dict() for h in self.history]}

class ContactHistory(db.Model):
    __tablename__ = 'contact_history'
    id         = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    action     = db.Column(db.String(50))
    detail     = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def to_dict(self):
        return {'action':self.action,'detail':self.detail,'created_at':self.created_at.strftime('%d %b %Y, %I:%M %p')}

class ManualLead(db.Model):
    __tablename__ = 'manual_leads'
    id               = db.Column(db.Integer, primary_key=True)
    full_name        = db.Column(db.String(100), nullable=False)
    email            = db.Column(db.String(120))
    phone            = db.Column(db.String(20), nullable=False)
    company          = db.Column(db.String(100))
    designation      = db.Column(db.String(100))
    service_interest = db.Column(db.String(100))
    city             = db.Column(db.String(60))
    notes            = db.Column(db.Text)
    status           = db.Column(db.String(20), default='new')
    follow_up_date   = db.Column(db.String(20))
    last_contacted   = db.Column(db.String(30))
    priority         = db.Column(db.String(10), default='normal')
    source           = db.Column(db.String(50), default='Manual Entry')
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    def to_dict(self):
        return {'id':f"m{self.id}",'full_name':self.full_name,'email':self.email or '',
                'phone':self.phone,'company':self.company or '','designation':self.designation or '',
                'service_interest':self.service_interest or '','message':self.notes or '',
                'city':self.city or '','submitted_at':self.created_at.strftime('%d %b %Y, %I:%M %p'),
                'status':self.status,'notes':self.notes or '','follow_up_date':self.follow_up_date or '',
                'last_contacted':self.last_contacted or '','priority':self.priority or 'normal',
                'source':self.source,'history':[]}

class AdminMeta(db.Model):
    __tablename__ = 'admin_meta'
    id             = db.Column(db.Integer, primary_key=True)
    last_login_at  = db.Column(db.DateTime)

class PageView(db.Model):
    __tablename__ = 'page_views'
    id         = db.Column(db.Integer, primary_key=True)
    page       = db.Column(db.String(100))
    ip_hash    = db.Column(db.String(64))
    user_agent = db.Column(db.String(200))
    referrer   = db.Column(db.String(200))
    viewed_at  = db.Column(db.DateTime, default=datetime.utcnow)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

def track_view(page):
    try:
        ip  = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr or '')
        iph = hashlib.sha256(ip.encode()).hexdigest()[:16]
        ua  = (request.user_agent.string or '')[:200]
        ref = (request.referrer or '')[:200]
        db.session.add(PageView(page=page,ip_hash=iph,user_agent=ua,referrer=ref))
        db.session.commit()
    except: pass

@app.route('/favicon.ico')
def favicon():
    from flask import send_from_directory
    return send_from_directory(os.path.join(app.root_path,'static','images'),'favicon.ico',mimetype='image/x-icon')

@app.route('/')
def index():
    track_view('home')
    return render_template('index.html')

@app.route('/services')
def services():
    track_view('services')
    return render_template('services.html')

@app.route('/about')
def about():
    track_view('about')
    return render_template('about.html')

@app.route('/contact')
def contact():
    track_view('contact')
    return render_template('contact.html',owner_email=OWNER_EMAIL,owner_phone=OWNER_PHONE,owner_whatsapp=OWNER_WHATSAPP)

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    data=request.form
    errors={}
    if not data.get('full_name','').strip(): errors['full_name']='Full name is required.'
    if not data.get('email','').strip():     errors['email']='Email is required.'
    if not data.get('phone','').strip():     errors['phone']='Phone is required.'
    if not data.get('message','').strip():   errors['message']='Message is required.'
    if errors: return jsonify({'success':False,'errors':errors}),400
    c=Contact(full_name=data.get('full_name','').strip(),email=data.get('email','').strip(),
              phone=data.get('phone','').strip(),company=data.get('company','').strip() or None,
              designation=data.get('designation','').strip() or None,
              service_interest=data.get('service_interest','').strip() or None,
              message=data.get('message','').strip(),city=data.get('city','').strip() or None)
    db.session.add(c); db.session.commit()
    db.session.add(ContactHistory(contact_id=c.id,action='Lead Created',detail='Contact form submitted on website'))
    db.session.commit()
    print(f"[LEAD] {c.full_name} | {c.email} | {c.phone}")
    return jsonify({'success':True,'message':'Thank you! We will reach out within 24 hours.',
                    'contact_data':{'name':c.full_name,'email':c.email,'phone':c.phone,
                                    'company':c.company or '','city':c.city or '',
                                    'service':c.service_interest or '','message':c.message}})

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    error=None
    if request.method=='POST':
        if request.form.get('username','').strip()==ADMIN_USERNAME and request.form.get('password','').strip()==ADMIN_PASSWORD:
            session.permanent=True
            session['admin_logged_in']=True
            session['admin_user']=ADMIN_USERNAME

            meta=AdminMeta.query.first()
            now=datetime.utcnow()
            new_since_last_visit=0
            if meta and meta.last_login_at:
                new_since_last_visit=Contact.query.filter(Contact.submitted_at>meta.last_login_at).count()
            if not meta:
                meta=AdminMeta(last_login_at=now); db.session.add(meta)
            else:
                meta.last_login_at=now
            db.session.commit()

            if new_since_last_visit>0:
                session['new_leads_popup']=new_since_last_visit

            return redirect(url_for('admin_dashboard'))
        error='Invalid username or password.'
    return render_template('admin_login.html',error=error)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_leads  = Contact.query.count()+ManualLead.query.count()
    new_leads    = Contact.query.filter_by(status='new').count()+ManualLead.query.filter_by(status='new').count()
    won_leads    = Contact.query.filter_by(status='closed').count()+ManualLead.query.filter_by(status='closed').count()
    total_views  = PageView.query.count()
    today        = datetime.utcnow().date()
    today_views  = PageView.query.filter(db.func.date(PageView.viewed_at)==today).count()
    today_leads  = Contact.query.filter(db.func.date(Contact.submitted_at)==today).count()
    page_stats   = db.session.query(PageView.page,db.func.count(PageView.id).label('cnt')).group_by(PageView.page).all()
    week_ago     = datetime.utcnow()-timedelta(days=7)
    weekly_views_raw = db.session.query(db.func.date(PageView.viewed_at).label('day'),db.func.count(PageView.id).label('cnt')).filter(PageView.viewed_at>=week_ago).group_by(db.func.date(PageView.viewed_at)).order_by(db.func.date(PageView.viewed_at)).all()
    weekly_views = []
    for row in weekly_views_raw:
        day_val = row.day
        if isinstance(day_val, str):
            try: day_val = datetime.strptime(day_val, '%Y-%m-%d').date()
            except ValueError: pass
        weekly_views.append({'day': day_val, 'cnt': row.cnt})
    recent_leads = Contact.query.order_by(Contact.submitted_at.desc()).limit(5).all()
    service_stats= db.session.query(Contact.service_interest,db.func.count(Contact.id).label('cnt')).filter(Contact.service_interest!=None).group_by(Contact.service_interest).order_by(db.func.count(Contact.id).desc()).limit(5).all()
    recent_activity = ContactHistory.query.order_by(ContactHistory.created_at.desc()).limit(6).all()
    new_leads_popup = session.pop('new_leads_popup', 0)
    return render_template('admin_dashboard.html',total_leads=total_leads,new_leads=new_leads,
                           won_leads=won_leads,total_views=total_views,today_views=today_views,
                           today_leads=today_leads,page_stats=page_stats,weekly_views=weekly_views,
                           recent_leads=recent_leads,service_stats=service_stats,
                           recent_activity=recent_activity,new_leads_popup=new_leads_popup,
                           admin_user=session.get('admin_user','Admin'),now=datetime.utcnow())


@app.route('/admin/crm')
@login_required
def admin_crm():
    return render_template('crm.html')

@app.route('/crm')
def crm():
    """Public, read-only CRM pipeline overview — counts only, no lead/customer
    details. Adding, editing and deleting leads remains admin-only."""
    track_view('crm')
    return render_template('crm_public.html')

@app.route('/crm-stats-json')
def crm_stats_json():
    """Public JSON feed of pipeline counts only. Never expose contact fields
    (name, phone, email, message) here — this endpoint has no login check."""
    def count(status):
        return Contact.query.filter_by(status=status).count() + ManualLead.query.filter_by(status=status).count()
    stats = {
        'new':       count('new'),
        'contacted': count('contacted'),
        'proposal':  count('proposal'),
        'won':       count('closed'),
        'lost':      count('lost'),
    }
    stats['total'] = sum(stats.values())
    return jsonify(stats)

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    contacts=Contact.query.order_by(Contact.submitted_at.desc()).all()
    recent_activity=ContactHistory.query.order_by(ContactHistory.created_at.desc()).limit(6).all()
    return render_template('admin.html',contacts=contacts,recent_activity=recent_activity,
                           admin_user=session.get('admin_user','Admin'))

@app.route('/admin/contacts-json')
@login_required
def contacts_json():
    c=Contact.query.order_by(Contact.submitted_at.desc()).all()
    m=ManualLead.query.order_by(ManualLead.created_at.desc()).all()
    return jsonify([x.to_dict() for x in c]+[x.to_dict() for x in m])

@app.route('/admin/update/<contact_id>', methods=['POST'])
@login_required
def update_contact(contact_id):
    data=request.form
    if str(contact_id).startswith('m'):
        lead=ManualLead.query.get_or_404(int(contact_id[1:]))
        old=lead.status
        for f in ['company','designation','city','service_interest','notes','follow_up_date','priority']:
            v=data.get(f); 
            if v is not None: setattr(lead,f,v)
        ns=data.get('status',lead.status)
        if ns!=old:
            lead.status=ns
            if ns in ('contacted','proposal','closed','won'): lead.last_contacted=datetime.utcnow().strftime('%d %b %Y, %I:%M %p')
        db.session.commit(); return jsonify({'success':True})
    lead=Contact.query.get_or_404(int(contact_id))
    old=lead.status
    for f in ['company','designation','city','service_interest','follow_up_date','priority']:
        v=data.get(f)
        if v is not None: setattr(lead,f,v)
    nn=data.get('notes','').strip()
    if nn and nn!=(lead.notes or ''):
        db.session.add(ContactHistory(contact_id=lead.id,action='Note Added',detail=nn))
        lead.notes=nn
    ns=data.get('status',lead.status)
    if ns!=old:
        db.session.add(ContactHistory(contact_id=lead.id,action='Status Changed',detail=f'{old} → {ns}'))
        lead.status=ns
        if ns in ('contacted','proposal','closed','won'): lead.last_contacted=datetime.utcnow().strftime('%d %b %Y, %I:%M %p')
    db.session.commit(); return jsonify({'success':True})

@app.route('/admin/add-lead', methods=['POST'])
@login_required
def add_manual_lead():
    data=request.form
    if not data.get('full_name','').strip() or not data.get('phone','').strip():
        return jsonify({'success':False,'error':'Name and phone required.'}),400
    lead=ManualLead(full_name=data.get('full_name','').strip(),email=data.get('email','').strip() or None,
                    phone=data.get('phone','').strip(),company=data.get('company','').strip() or None,
                    designation=data.get('designation','').strip() or None,
                    service_interest=data.get('service_interest','').strip() or None,
                    city=data.get('city','').strip() or None,notes=data.get('notes','').strip() or None,
                    status=data.get('status','new'),priority=data.get('priority','normal'),
                    source=data.get('source','Manual Entry'))
    db.session.add(lead); db.session.commit()
    return jsonify({'success':True,'id':f"m{lead.id}"})

@app.route('/admin/delete-lead/<contact_id>', methods=['POST'])
@login_required
def delete_lead(contact_id):
    if str(contact_id).startswith('m'): lead=ManualLead.query.get_or_404(int(contact_id[1:]))
    else: lead=Contact.query.get_or_404(int(contact_id))
    db.session.delete(lead); db.session.commit()
    return jsonify({'success':True})

@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    import urllib.request as _u, json as _j
    data=request.get_json(silent=True) or {}
    messages=data.get('messages',[]); system=data.get('system','')
    api_key=os.environ.get('ANTHROPIC_API_KEY','').strip()
    if not api_key:
        user_msg=messages[-1]['content'].lower() if messages else ''
        if any(w in user_msg for w in ['amc','maintenance','annual']): reply="Our IT AMC includes quarterly visits, 24/6 support, antivirus, backup & 3 on-site visits/month — 12 months coverage!"
        elif any(w in user_msg for w in ['repair','fix','broken']): reply="We repair laptops, desktops, servers, printers & networking equipment with certified engineers."
        elif any(w in user_msg for w in ['cctv','camera','surveillance']): reply="We design, install & monitor CCTV systems plus biometric access control."
        elif any(w in user_msg for w in ['contact','phone','email']): reply=f"📞 +91 98869 99575 / +91 96866 34787 | ✉️ {OWNER_EMAIL} | 📍 Bengaluru. 24/6 support!"
        elif any(w in user_msg for w in ['price','cost','how much']): reply="Contact us for a free customised quote!"
        else: reply="Hi! I'm TechBot for Total Tech Serve. Ask about IT AMC, repair, CCTV, network, hardware or insurance. 😊"
        return jsonify({'reply':reply})
    payload=_j.dumps({'model':'claude-haiku-4-5-20251001','max_tokens':300,'system':system,'messages':messages}).encode()
    req=_u.Request('https://api.anthropic.com/v1/messages',data=payload,
                   headers={'Content-Type':'application/json','x-api-key':api_key,'anthropic-version':'2023-06-01'},method='POST')
    try:
        with _u.urlopen(req,timeout=25) as resp: return jsonify({'reply':_j.loads(resp.read())['content'][0]['text']})
    except: return jsonify({'reply':'Call us at +91 98869 99575!'})

@app.route('/robots.txt')
def robots():
    return Response("User-agent: *\nAllow: /\nDisallow: /admin\nSitemap: https://totaltechserve.com/sitemap.xml\n",mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    xml="""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://totaltechserve.com/</loc><priority>1.0</priority></url>
  <url><loc>https://totaltechserve.com/services</loc><priority>0.9</priority></url>
  <url><loc>https://totaltechserve.com/about</loc><priority>0.8</priority></url>
  <url><loc>https://totaltechserve.com/contact</loc><priority>0.8</priority></url></urlset>"""
    return Response(xml,mimetype='application/xml')

with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(debug=True,port=5000, use_reloader=False)
