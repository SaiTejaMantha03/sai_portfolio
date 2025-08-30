# Django Portfolio Project

A modern portfolio website built with Django featuring blog, projects showcase, and contact functionality.

## Features

- **Portfolio Showcase**: Display your skills, experience, and education
- **Blog System**: Create and manage blog posts with categories
- **Projects Gallery**: Showcase your projects with detailed descriptions
- **Photo Gallery**: Display your photography work
- **Contact Form**: Allow visitors to get in touch
- **Responsive Design**: Mobile-friendly interface

## Tech Stack

- **Backend**: Django 4.2.7
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: Pillow
- **Deployment**: Gunicorn, WhiteNoise

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/portfolio_project.git
cd portfolio_project
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**
- Update database settings in `portfolio_project/settings.py`
- Create MySQL database named `portfolio_db`

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the website.

## Project Structure

```
portfolio_project/
├── apps/                 # Main portfolio app
├── blog/                 # Blog functionality
├── projects/             # Projects showcase
├── static/               # Static files (CSS, JS, images)
├── media/                # User uploaded files
├── portfolio_project/    # Django project settings
└── requirements.txt      # Python dependencies
```

## Usage

1. **Admin Panel**: Access `/admin/` to manage content
2. **Add Content**: Create profiles, skills, projects, and blog posts
3. **Customize**: Modify templates in each app's `templates/` folder
4. **Styling**: Update CSS in `static/css/style.css`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).