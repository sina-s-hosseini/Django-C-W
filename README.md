Django Crypto Wallet
This is a Django-based cryptocurrency wallet platform that allows users to:
•Register and log in securely
•View and manage their ETH balance
•Send ETH to other users
•Purchase mock ETH using IRR
•Edit their profile with bio and picture
•Reset their password via email
•See dashboard analytics like total sent/received



Technologies Used:
Python 3.12
Django 5.1.7
SQLite (for development)
HTML, CSS (custom design with neon-glass effects)
Pillow (for handling profile picture uploads)



How to Run:
Clone the project:
git clone https://github.com/sina-s-hosseini/Django-C-W.git
cd your-repo-name
Set up virtual environment:
python3 -m venv env
source env/bin/activate
Install dependencies:
pip install -r requirements.txt
Run database migrations:
python manage.py makemigrations
python manage.py migrate
Start development server:
python manage.py runserver
Open in browser:
http://localhost:8000


Admin Access:
To create a Django superuser account for admin panel:
python manage.py createsuperuser
