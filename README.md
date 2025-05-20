django_pos

django_pos is a Point of Sale (POS) system built with Django, designed solely for educational purposes. 
This project demonstrates core concepts of Django web development, including models, views, templates, and basic CRUD operations in the context of a retail sales system.

Features
- Dashboard (Charts and Metrics)

- Product management (add, update, delete)

- Category management

- Simple sales transaction processing

- Basic reporting and transaction history

- User authentication


Purpose
This project is intended for learning and experimentation with Django framework. It is not meant for production use or handling real transactions.

Installation
1. Clone the repository:
  git clone https://github.com/yourusername/django_pos.git
  cd django_pos

2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install dependencies:
    npm install
    pip install -r requirements.txt

4. Apply migrations & Seed Roles Data:
  python manage.py migrate
  python manage.py seed_roles

5. Create superuser:
   python manage.py creasuperuser

6. Run the development server & Tailwind for design:
   python manage.py runserver
   npm run tainwild

Contributing
Contributions are welcome for educational enhancements and bug fixes. Please create issues or pull requests as needed.

License
This project is for educational use only. Do not use it in a production environment.
