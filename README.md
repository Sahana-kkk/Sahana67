# CareerPath

CareerPath is the existing Flask website for exploring career paths, scholarships, a short career quiz, and mentorship requests. This setup keeps the current pages and local SQLite database while adding deployment support for Render.

## Project files

```text
CareerPath/
├── app.py                 # Flask routes, SQLAlchemy models, and sample data
├── requirements.txt       # Python packages for local and hosted use
├── render.yaml            # Render free web service and database setup
├── .python-version        # Python version for Render
├── .env.example           # Names of optional local environment settings
└── templates/             # Existing HTML pages
```

The website has routes for `/`, `/careers`, `/scholarships`, `/quiz`, and `/mentorship`. It does not currently include login pages, user accounts, or authentication. The site uses sample career and scholarship records. A submitted mentorship request is saved in the database.

## Run locally on Windows

Open PowerShell in this folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>. The first run creates `careerpath.db` beside `app.py` and adds sample records. That local database file is ignored by Git so it is not accidentally uploaded.

## Upload the project to GitHub

1. Sign in to GitHub and create a new empty repository, for example `careerpath-portal`. Do not select options to add a README, license, or `.gitignore`.
2. In PowerShell, open this project folder. Initialize Git and add only the project source files:

   ```powershell
   git init
   git add app.py templates requirements.txt render.yaml .python-version .env.example .gitignore README.md
   git commit -m "Prepare CareerPath for deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/careerpath-portal.git
   git push -u origin main
   ```

3. Replace `YOUR_USERNAME` with your GitHub username. GitHub may open a browser sign-in window the first time you push.

Do not use `git add .` for this project. The sample database, local environment, generated presentation, and temporary build files should stay out of the website repository.

## Deploy to Render

Render currently offers free web services. This repository includes a `render.yaml` Blueprint that defines the Flask service and a free PostgreSQL database.

1. Sign in at <https://dashboard.render.com> and connect your GitHub account if prompted.
2. Choose **New** → **Blueprint**.
3. Select the `careerpath-portal` repository and its `main` branch.
4. Review the resources in `render.yaml`, then choose **Apply**. Render installs `requirements.txt` and starts the app with Gunicorn.
5. Wait for the deploy to finish. Open the service's `onrender.com` URL from its Render page.

The Blueprint generates a secret key and connects the app to PostgreSQL. Locally, the app continues using SQLite unless `DATABASE_URL` is set.

## Free-tier database and service limits

Render free web services can sleep after 15 minutes without traffic, so the first page load after a quiet period may take about a minute. Render can restart a free service, and its local filesystem is temporary. The Blueprint uses PostgreSQL for mentorship requests instead of relying on the temporary web-service filesystem.

Render's free PostgreSQL databases expire 30 days after creation. Upgrade the database or export any requests you need before expiry; after the expiration grace period, Render deletes the database and its data. Do not use this free setup to collect sensitive or important real-world student information.

## Check the deployed site

On desktop and on a phone-sized browser window, check these routes:

- `/` — home page and search
- `/careers` — stream filter and career cards
- `/scholarships` — eligibility filter and scholarship details modal
- `/quiz` — answer all five questions and review the suggestions
- `/mentorship` — submit a test request and confirm the success message

Use only a test name and email while checking the form. In Render, open the PostgreSQL database page to confirm the database is connected. The current project has no login feature, so there is no login flow to test.

## Notes

- Tailwind CSS, AOS, GSAP, and Google Fonts load from CDNs, so visitors' browsers need internet access for styling, fonts, and animations.
- Career salaries, colleges, award amounts, scholarship descriptions, and deadlines are illustrative sample content. Verify them with the relevant organizations before real use.
- The mentorship form has basic validation but the current project does not implement user login, an administrator dashboard, or CSRF protection.
