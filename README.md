# django_pos

**django_pos** is a Point of Sale (POS) system built with Django, designed **solely for educational purposes**.  
This project demonstrates core concepts of Django web development including models, views, templates, and basic CRUD operations in the context of a retail sales system.

---

## 🚀 Features

- 📊 Dashboard with charts and metrics  
- 📦 Product management (add, update, delete)  
- 🗂️ Category management  
- 💵 Simple sales transaction processing  
- 📑 Basic reporting and transaction history  
- 🔐 User authentication  

---

## 🎯 Purpose

This project is intended for **learning and experimentation** with the Django framework.  
It is **not** meant for production use or handling real transactions.

---

## ⚙️ Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/django_pos.git
cd django_pos
```

---

#### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```
---

#### 3. Install Dependencies

```bash
npm install
pip install -r requirements.txt
```
---

#### 4. Create a Database
```bash
Create a new database (e.g., django_pos_db)
Ensure your database settings are correctly configured in settings.py.
```
---

#### 5. Apply Migrations & Seed Roles
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_roles
```
---

#### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

---

#### 7. Run the Development Server and Tailwind CSS
```bash
python manage.py runserver
npm run tailwind
```

🤝 Contributing
Contributions are welcome for educational improvements and bug fixes.
Feel free to open an issue or submit a pull request.

📄 License
This project is intended for educational use only.
Do not use it in a production environment.
