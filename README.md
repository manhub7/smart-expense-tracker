# 💸 Smart Expense Tracker

A Streamlit-based personal finance tracker with analytics, budget tracking, and export features.

## Features
- 🔐 User authentication (signup/login)
- ➕ Add, edit, delete expenses
- 📊 Interactive analytics (pie, bar, line, monthly charts)
- 💰 Monthly budget tracker with alerts
- 📥 Export to CSV/Excel
- 🎨 Custom animated UI

## Setup
```bash
git clone <your-repo-url>
cd <repo-name>
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py


---

### 🚀 **Quick Git Commands**

```bash
cd your-project-folder
git init
git add .gitignore README.md app.py requirements.txt assets/ .streamlit/config.toml
git commit -m "Initial commit: Smart Expense Tracker"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main