"""CareerPath: Digital Career Guidance & Scholarship Portal."""
from datetime import date, datetime
import os
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
database_url = os.environ.get("DATABASE_URL", "").strip()
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "local-development-key-change-before-deploying"),
    SQLALCHEMY_DATABASE_URI=database_url or f"sqlite:///{BASE_DIR / 'careerpath.db'}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ENGINE_OPTIONS={"pool_pre_ping": True} if database_url else {},
)
db = SQLAlchemy(app)


class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    stream = db.Column(db.String(40), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    salary = db.Column(db.String(80), nullable=False)
    skills = db.Column(db.Text, nullable=False)
    roadmap = db.Column(db.Text, nullable=False)
    colleges = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(12), default="✦")


class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    organization = db.Column(db.String(120), nullable=False)
    eligibility = db.Column(db.String(40), nullable=False)
    amount = db.Column(db.String(80), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)


class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    interest = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


def seed_data():
    if Career.query.first():
        return
    careers = [
        ("software-engineer", "Software Engineer", "Tech", "Build the products and platforms that shape how people live and work.", "₹8–24 LPA", "Python, problem solving, databases, collaboration", "Learn programming foundations|Build projects and a portfolio|Earn a CS degree or equivalent|Apply for internships|Specialize and grow", "IITs · IIIT Hyderabad · BITS Pilani", "⌘"),
        ("data-scientist", "Data Scientist", "Tech", "Turn complex data into better decisions, useful predictions, and new possibilities.", "₹9–25 LPA", "Statistics, Python, SQL, communication", "Study maths and statistics|Learn Python and SQL|Practice machine learning|Build a project portfolio|Pursue internships", "IISc · IIT Madras · ISI Kolkata", "◉"),
        ("doctor", "Physician / Doctor", "Medicine", "Diagnose, treat, and care for people through a rigorous and rewarding medical journey.", "₹8–20 LPA", "Biology, empathy, clinical reasoning, resilience", "Complete PCB in 10+2|Qualify NEET-UG|Complete MBBS and internship|Register with NMC|Choose postgraduate specialization", "AIIMS · CMC Vellore · JIPMER", "✚"),
        ("biomedical-engineer", "Biomedical Engineer", "Medicine", "Bring engineering and medicine together to improve diagnostics and patient care.", "₹5–14 LPA", "Electronics, biology, CAD, research", "Build a strong science foundation|Study biomedical engineering|Gain lab and hospital experience|Explore regulatory standards|Specialize in devices or imaging", "IIT Bombay · VIT · Manipal", "⌬"),
        ("ux-designer", "UX / Product Designer", "Arts", "Make digital services more intuitive through research, design, and thoughtful iteration.", "₹6–18 LPA", "Visual design, user research, prototyping, storytelling", "Learn design fundamentals|Practice research and wireframing|Build case studies|Master Figma and prototyping|Apply to product teams", "NID Ahmedabad · IDC IIT Bombay · Srishti", "✳"),
        ("chartered-accountant", "Chartered Accountant", "Commerce", "Help organizations make sound financial decisions and meet their obligations.", "₹7–20 LPA", "Accounting, analysis, ethics, attention to detail", "Register with ICAI Foundation|Clear Foundation and Intermediate|Complete articleship|Clear CA Final|Build a practice or join a firm", "SRCC · Shri Ram College · St. Xavier’s", "◈"),
        ("renewable-energy-technician", "Renewable Energy Technician", "Vocational", "Install and maintain clean energy systems that power a more sustainable future.", "₹4–10 LPA", "Electrical fundamentals, safety, troubleshooting", "Complete 10+2 or ITI electrical|Take solar installation training|Earn industry certification|Gain supervised field experience|Advance to system design", "NISE · ITI networks · Skill India centres", "☼"),
        ("architect", "Architect", "Arts", "Shape welcoming spaces that balance culture, function, and the built environment.", "₹5–16 LPA", "Spatial thinking, drawing, CAD, communication", "Qualify NATA or JEE Paper 2|Complete a B.Arch degree|Complete practical training|Register with Council of Architecture|Build a design portfolio", "SPA Delhi · CEPT · IIT Roorkee", "△"),
    ]
    for row in careers:
        slug, title, stream, summary, salary, skills, roadmap, colleges, icon = row
        db.session.add(Career(slug=slug, title=title, stream=stream, summary=summary, salary=salary,
                              skills=skills, roadmap=roadmap, colleges=colleges, icon=icon))
    today = date.today()
    scholarships = [
        ("National Merit Scholars Award", "National Education Foundation", "Merit-based", "Up to ₹1,00,000", 65, "For high-achieving undergraduate students enrolled at an accredited institution.", "Academic transcripts, proof of enrollment, personal statement"),
        ("Bright Futures Need Grant", "Bright Futures Trust", "Need-based", "Up to ₹75,000", 92, "Need-based support for first-generation learners from low-income households.", "Income certificate, transcripts, recommendation letter"),
        ("Women in Computing Fellowship", "CodeForward India", "Women in STEM", "₹1,50,000", 128, "For women pursuing an undergraduate degree in computing or related STEM fields.", "Enrollment proof, project portfolio, short essay"),
        ("Global Citizens Study Fund", "Open Horizons", "International", "Up to $5,000", 180, "For students planning a semester or degree program at an international university.", "Offer letter, academic record, budget statement"),
        ("STEM Pathways Scholarship", "Future Labs Foundation", "Merit-based", "₹50,000", 230, "Merit award for students pursuing science, technology, engineering, or mathematics.", "Transcripts, faculty reference, statement of purpose"),
        ("Rising Women Engineers Award", "TechBridge Collective", "Women in STEM", "₹90,000", 275, "Support for women engineering students with a record of community involvement.", "Enrollment proof, CV, community impact essay"),
    ]
    for title, org, eligibility, amount, days, description, requirements in scholarships:
        db.session.add(Scholarship(title=title, organization=org, eligibility=eligibility,
                                   amount=amount, deadline=today.fromordinal(today.toordinal() + days),
                                   description=description, requirements=requirements))
    db.session.commit()


@app.context_processor
def inject_globals():
    return {"current_year": date.today().year, "today": date.today(),
            "streams": ["Tech", "Medicine", "Arts", "Commerce", "Vocational"]}


@app.get("/")
def home():
    featured = Career.query.order_by(Career.id).limit(4).all()
    q = request.args.get("q", "").strip()
    return render_template("index.html", featured=featured, q=q)


@app.get("/careers")
def careers():
    stream = request.args.get("stream", "All")
    q = request.args.get("q", "").strip()
    query = Career.query
    if stream in ["Tech", "Medicine", "Arts", "Commerce", "Vocational"]:
        query = query.filter_by(stream=stream)
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Career.title.ilike(like), Career.summary.ilike(like), Career.skills.ilike(like)))
    return render_template("careers.html", careers=query.order_by(Career.id).all(), selected=stream, q=q)


@app.get("/scholarships")
def scholarships():
    category = request.args.get("eligibility", "All")
    q = request.args.get("q", "").strip()
    query = Scholarship.query
    if category in ["Merit-based", "Need-based", "Women in STEM", "International"]:
        query = query.filter_by(eligibility=category)
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Scholarship.title.ilike(like), Scholarship.organization.ilike(like), Scholarship.description.ilike(like)))
    return render_template("scholarships.html", scholarships=query.order_by(Scholarship.deadline).all(), selected=category, q=q)


@app.get("/quiz")
def quiz():
    careers = [{"title": c.title, "stream": c.stream, "salary": c.salary, "icon": c.icon}
               for c in Career.query.order_by(Career.id).all()]
    return render_template("quiz.html", careers=careers)


@app.post("/mentorship")
def submit_mentorship():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    interest = request.form.get("interest", "").strip()
    message = request.form.get("message", "").strip()
    if not all([name, email, interest, message]) or "@" not in email:
        flash("Please complete every field with a valid email address.", "error")
        return render_template("mentorship.html", values=request.form), 400
    db.session.add(Inquiry(name=name, email=email, interest=interest, message=message))
    db.session.commit()
    flash("Thanks! Your mentorship request is in. We’ll be in touch soon.", "success")
    return redirect(url_for("mentorship"))


@app.get("/mentorship")
def mentorship():
    return render_template("mentorship.html", values={})


@app.get("/api/careers")
def careers_api():
    return jsonify([{"title": c.title, "stream": c.stream, "salary": c.salary, "url": url_for("careers", q=c.title)}
                    for c in Career.query.order_by(Career.title).all()])


with app.app_context():
    db.create_all()
    seed_data()


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1",
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
    )
