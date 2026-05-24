# Conectio

> **Connect with purpose.**

A professional social networking platform inspired by LinkedIn, built with Django REST Framework and vanilla HTML/CSS/JavaScript.

![Conectio](https://img.shields.io/badge/Conectio-Connect%20with%20purpose-0A66C2?style=for-the-badge)

---

## 🚀 Features

- **User Authentication** — JWT-based registration, login, and session management
- **User Profiles** — Customizable profiles with avatars, bios, and headlines
- **Social Feed** — Create, like, and comment on posts
- **Follow System** — Follow/unfollow users and build your network
- **Explore** — Discover people and content across the community
- **Responsive Design** — Works beautifully on desktop and mobile

## 📁 Project Structure

```
conectio/
├── backend/
│   ├── conectio_project/       # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/                  # User profiles & connections
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── posts/                  # Posts, likes, comments
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── index.html              # Home / landing page
│   ├── login.html              # Sign in
│   ├── register.html           # Sign up
│   ├── profile.html            # User profile
│   ├── explore.html            # Explore page
│   └── assets/
│       ├── css/
│       │   ├── main.css        # Global styles & design tokens
│       │   └── components.css  # Reusable UI components
│       └── js/
│           ├── api.js          # API client with JWT
│           ├── auth.js         # Token management
│           └── main.js         # Page logic & utilities
├── .gitignore
└── README.md
```

## 🛠️ Tech Stack

| Layer      | Technology                                |
|------------|------------------------------------------|
| Backend    | Django 4.2 + Django REST Framework       |
| Frontend   | Vanilla HTML, CSS, JavaScript            |
| Auth       | JWT via djangorestframework-simplejwt    |
| Database   | SQLite (development)                     |
| CORS       | django-cors-headers                      |

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- pip

### Backend Setup

```bash
# 1. Create and activate virtual environment
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py makemigrations users posts
python manage.py migrate

# 4. Create superuser (optional)
python manage.py createsuperuser

# 5. Start the server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

### Frontend Setup

Simply open `frontend/index.html` in your browser, or use a local server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 5500
```

Then visit `http://localhost:5500`

## 🔗 API Endpoints

### Authentication
| Method | Endpoint              | Description          |
|--------|-----------------------|----------------------|
| POST   | `/api/token/`         | Obtain JWT tokens    |
| POST   | `/api/token/refresh/` | Refresh access token |

### Users
| Method | Endpoint                        | Description              |
|--------|---------------------------------|--------------------------|
| POST   | `/api/users/register/`          | Register new account     |
| GET    | `/api/users/profile/`           | Get my profile           |
| PATCH  | `/api/users/profile/`           | Update my profile        |
| GET    | `/api/users/profile/<username>/`| Get user's profile       |
| POST   | `/api/users/follow/<username>/` | Follow/unfollow user     |
| GET    | `/api/users/suggested/`         | Get suggested users      |

### Posts
| Method | Endpoint                         | Description             |
|--------|----------------------------------|-------------------------|
| GET    | `/api/posts/`                    | List all posts (feed)   |
| POST   | `/api/posts/`                    | Create a post           |
| GET    | `/api/posts/<id>/`               | Get single post         |
| DELETE | `/api/posts/<id>/`               | Delete own post         |
| POST   | `/api/posts/<id>/like/`          | Like/unlike post        |
| GET    | `/api/posts/<id>/comments/`      | List comments           |
| POST   | `/api/posts/<id>/comments/`      | Add comment             |
| GET    | `/api/posts/user/<username>/`    | User's posts            |

## 🎨 Design System

### Colors
| Token              | Value     | Usage                    |
|--------------------|-----------|--------------------------|
| Primary Blue       | `#0A66C2` | Buttons, links, accents  |
| Hover Blue         | `#004182` | Hover states             |
| Background         | `#F3F2EF` | Page background          |
| Card Background    | `#FFFFFF` | Cards and surfaces       |
| Text Primary       | `#000000` | Main text                |
| Text Secondary     | `#666666` | Muted text               |
| Border             | `#E0DFD8` | Dividers, card borders   |
| Success            | `#057642` | Success states           |
| Error              | `#CC1016` | Error states             |

### Components
Pre-built CSS classes: `.btn-primary`, `.btn-secondary`, `.btn-ghost`, `.card`, `.card-shadow`, `.avatar`, `.badge`, `.input-field`, `.textarea-field`, `.divider`, `.alert`, `.spinner`, `.dropdown`, `.page-layout`

## 📄 License

This project is for educational and development purposes.

---

<p align="center">
  <strong>Conectio</strong> · Connect with purpose. · Built with ❤️
</p>
