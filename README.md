# Conectio

> **Connect with purpose.**

A professional social networking platform inspired by LinkedIn, built with Django REST Framework and vanilla HTML/CSS/JavaScript.

![Conectio](https://img.shields.io/badge/Conectio-Connect%20with%20purpose-0A66C2?style=for-the-badge)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Authentication** | JWT-based registration, login, logout with token blacklisting |
| 👤 **User Profiles** | Customizable profiles with avatars, bios, headlines, and websites |
| 📝 **Posts** | Create, delete, and view posts with image uploads |
| ❤️ **Likes** | Like/unlike posts with optimistic UI and animations |
| 💬 **Comments** | Comment on posts with real-time rendering |
| 👥 **Follow System** | Follow/unfollow users, follower/following lists with modals |
| 🔍 **Search** | Full-text search across users and posts |
| 🔥 **Explore** | Discover trending posts sorted by engagement |
| 📰 **Personalized Feed** | See posts from people you follow |
| 🔔 **Notifications** | Bell icon with activity dropdown and red dot indicator |
| 🖼️ **Image Lightbox** | Click any post image for full-screen view with Escape to close |
| 📱 **Responsive** | Works beautifully on desktop, tablet, and mobile (375px+) |
| 🛡️ **Security** | Rate limiting, CORS, security headers, env-based secrets |

## 📁 Project Structure

```
conectio/
├── backend/
│   ├── conectio_project/       # Django project settings
│   │   ├── settings.py         # Env-based config, WhiteNoise, security
│   │   ├── urls.py             # API routing
│   │   └── wsgi.py
│   ├── users/                  # User profiles & connections
│   │   ├── models.py           # Custom User, Connection
│   │   ├── serializers.py      # Registration, profile, follow
│   │   ├── views.py            # Auth, profile, follow, avatar
│   │   └── urls.py
│   ├── posts/                  # Posts, likes, comments
│   │   ├── models.py           # Post, Like, Comment
│   │   ├── serializers.py      # Post/comment with time_ago
│   │   ├── views.py            # CRUD, feed, search, explore
│   │   └── urls.py
│   ├── requirements.txt
│   ├── Procfile                # Gunicorn for production
│   ├── render.yaml             # Render deployment config
│   └── manage.py
├── frontend/
│   ├── index.html              # Home feed + post creation
│   ├── login.html              # Sign in with validation
│   ├── register.html           # Sign up with password strength
│   ├── profile.html            # User profile + edit + posts
│   ├── explore.html            # Search + trending posts
│   ├── netlify.toml            # Netlify deployment config
│   └── assets/
│       ├── css/
│       │   ├── main.css        # Design tokens, layout, responsive
│       │   └── components.css  # Buttons, cards, inputs, lightbox, bell
│       └── js/
│           ├── api.js          # Fetch wrapper with JWT + dynamic base URL
│           ├── auth.js         # Token management + user storage
│           └── main.js         # Navbar, toast, lightbox, notifications
├── .gitignore
└── README.md
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 + Django REST Framework |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Auth | JWT via djangorestframework-simplejwt |
| Database | SQLite (dev) / PostgreSQL (production) |
| Static Files | WhiteNoise |
| CORS | django-cors-headers |
| Rate Limiting | django-ratelimit |
| Deployment | Render (backend) + Netlify (frontend) |

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

# 3. Configure environment
# Edit .env with your settings (defaults work for local dev)

# 4. Run migrations
python manage.py makemigrations users posts
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Start the server
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

## 🔧 Environment Variables

Create a `.env` file in `backend/` with:

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | *(insecure default)* | Django secret key — **change in production** |
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated allowed hosts |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database URL (use PostgreSQL in production) |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5500` | Comma-separated allowed frontend origins |
| `CLOUDINARY_CLOUD_NAME` | *(empty)* | Optional Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | *(empty)* | Optional Cloudinary API key |
| `CLOUDINARY_API_SECRET` | *(empty)* | Optional Cloudinary API secret |

## 🔗 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register/` | Create account (rate limited) |
| POST | `/api/users/login/` | Sign in (rate limited) |
| POST | `/api/users/logout/` | Sign out (blacklist token) |
| POST | `/api/token/refresh/` | Refresh access token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/me/` | Get own profile |
| PATCH | `/api/users/me/update/` | Update profile fields |
| POST | `/api/users/me/avatar/` | Upload avatar (max 5MB) |
| GET | `/api/users/<username>/` | Get user's public profile |
| POST | `/api/users/follow/<username>/` | Follow/unfollow user |
| GET | `/api/users/suggested/` | Get suggested users |
| GET | `/api/users/<username>/followers/` | List followers |
| GET | `/api/users/<username>/following/` | List following |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts/` | List all posts |
| POST | `/api/posts/` | Create a post |
| GET | `/api/posts/<id>/` | Get single post |
| DELETE | `/api/posts/<id>/` | Delete own post |
| POST | `/api/posts/<id>/like/` | Like/unlike post |
| GET | `/api/posts/<id>/comments/` | List comments |
| POST | `/api/posts/<id>/comments/` | Add comment |
| DELETE | `/api/posts/<id>/comments/<id>/` | Delete own comment |
| GET | `/api/posts/user/<username>/` | User's posts |

### Global
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feed/` | Personalized feed |
| GET | `/api/search/?q=term` | Search users & posts |
| GET | `/api/explore/` | Trending posts |

## 🎨 Design System

### Colors
| Token | Value | Usage |
|-------|-------|-------|
| Primary Blue | `#0A66C2` | Buttons, links, accents |
| Hover Blue | `#004182` | Hover states |
| Background | `#F3F2EF` | Page background |
| Card Background | `#FFFFFF` | Cards and surfaces |
| Text Primary | `#000000` | Main text |
| Text Secondary | `#666666` | Muted text |
| Border | `#E0DFD8` | Dividers, card borders |
| Success | `#057642` | Success states |
| Warning | `#C37D16` | Warning states |
| Error | `#CC1016` | Error states |

### Components
Pre-built CSS classes: `.btn-primary`, `.btn-secondary`, `.btn-ghost`, `.card`, `.card-shadow`, `.avatar`, `.badge`, `.input-field`, `.input-field--success`, `.input-field--error`, `.textarea-field`, `.divider`, `.alert`, `.spinner`, `.dropdown`, `.lightbox-overlay`, `.notification-bell`, `.password-strength`

## 🚀 Deployment

### Backend (Render)

1. Push your code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repo, select the `backend/` directory
4. Render will auto-detect the `render.yaml` config
5. Add a **PostgreSQL** database and set `DATABASE_URL` env var
6. Update `ALLOWED_HOSTS` to include your Render domain
7. Update `CORS_ALLOWED_ORIGINS` to your Netlify frontend URL

### Frontend (Netlify)

1. Create a new site on [Netlify](https://netlify.com)
2. Connect your GitHub repo, set publish directory to `frontend/`
3. Update `api.js` — replace `YOUR-RENDER-URL` with your Render backend subdomain
4. Deploy!

## 📄 License

This project is for educational and development purposes.

---

<p align="center">
  <strong>Conectio</strong> · Connect with purpose. · Built with ❤️
</p>
