# Restaurant Web Application - Django

Welcome to the Restaurant Web Application built with Django! This application provides a platform for ordering food near your location, searching for recipes, and connecting with us through chatbot or email. Before using the app, you'll need to authenticate yourself via email. There's also an Admin Dashboard for managing the application's content.

## Getting Started

Follow these steps to set up and run the project locally:

```bash
# Clone the repository
git clone "https://github.com/ketanu0690/resturent-web-application-Django-.git"

# Install and activate a virtual environment
pip install virtualenv
virtualenv myenv
myenv\Scripts\activate

# Install project dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser

# Run the development server
python manage.py runserver

