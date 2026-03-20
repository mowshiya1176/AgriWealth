# 🌿 AgriWealth — Farm Waste to Wealth Platform

AgriWealth is a Django-based web platform that helps farmers convert agricultural waste into valuable products and earn income. Farmers can list waste, discover conversion ideas, and connect with buyers — all in one place.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🔐 Authentication | Farmer & Buyer registration, login, profile |
| 🛒 Marketplace | List, browse, search & filter waste items |
| 🤖 AgriBot | AI chatbot (OpenAI GPT-3.5 + rule-based fallback) |
| 💬 Real-time Chat | WebSocket-powered Farmer ↔ Buyer messaging |
| 🔍 Search | Full-text search + filter by category & status |
| ⚙️ Admin Dashboard | Full Django admin for users, listings, messages |

---

## 📁 Project Structure

```
agriwealth/
├── agriwealth/               # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py               # Django Channels ASGI config
│   └── wsgi.py
│
├── accounts/                 # Custom User model & auth
│   ├── models.py             # User (farmer/buyer roles)
│   ├── views.py              # register, login, profile
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── core/                     # Home & About pages
│   ├── views.py
│   └── urls.py
│
├── marketplace/              # Waste listings
│   ├── models.py             # WasteItem, WasteCategory
│   ├── views.py              # CRUD + search
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── chat/                     # Real-time chat
│   ├── models.py             # ChatRoom, Message
│   ├── consumers.py          # WebSocket consumer
│   ├── routing.py            # WebSocket URL routing
│   ├── views.py
│   └── urls.py
│
├── chatbot/                  # AI chatbot
│   ├── views.py              # OpenAI + fallback logic
│   └── urls.py
│
├── templates/                # HTML templates
│   ├── base.html
│   ├── core/
│   ├── accounts/
│   ├── marketplace/
│   ├── chat/
│   └── chatbot/
│
├── static/                   # CSS, JS, Images
├── manage.py
├── requirements.txt
├── setup.sh
└── .env.example
```

---

## 🗄️ Database Schema

### `accounts_user`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| username | VARCHAR | Unique |
| email | VARCHAR | |
| role | VARCHAR(10) | `farmer` or `buyer` |
| phone | VARCHAR | |
| location | VARCHAR | |
| bio | TEXT | |
| profile_image | ImageField | |

### `marketplace_wastecategory`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| name | VARCHAR(100) | |
| slug | SlugField | Unique |
| icon | VARCHAR(50) | Emoji icon |

### `marketplace_wasteitem`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| farmer_id | FK → User | |
| category_id | FK → WasteCategory | |
| title | VARCHAR(200) | |
| description | TEXT | |
| quantity | Decimal | |
| unit | VARCHAR(10) | kg/ton/liter/bundle |
| price_per_unit | Decimal | Optional |
| location | VARCHAR | |
| possible_products | TEXT | Comma-separated |
| image | ImageField | Optional |
| status | VARCHAR(10) | available/sold/pending |
| is_featured | Boolean | |
| views_count | Integer | |
| created_at | DateTime | |

### `chat_chatroom`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| farmer_id | FK → User | |
| buyer_id | FK → User | |
| waste_item_id | FK → WasteItem | Optional |
| created_at | DateTime | |

### `chat_message`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| room_id | FK → ChatRoom | |
| sender_id | FK → User | |
| content | TEXT | |
| is_read | Boolean | |
| created_at | DateTime | |

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- pip

### 1. Clone & Setup

```bash
# Navigate into project folder
cd agriwealth

# Run the setup script (handles everything)
bash setup.sh
```

### 2. Manual Setup (if preferred)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env from example
cp .env.example .env
# Edit .env and update SECRET_KEY and OPENAI_API_KEY

# Run migrations
python manage.py makemigrations accounts
python manage.py makemigrations marketplace
python manage.py makemigrations chat
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run dev server
python manage.py runserver
```

### 3. Seed Waste Categories

```bash
python manage.py shell
```

```python
from marketplace.models import WasteCategory

categories = [
    ('Crop Residues',   'crop-residues',   '🌾'),
    ('Animal Manure',   'animal-manure',   '🐄'),
    ('Vegetable Waste', 'vegetable-waste', '🥦'),
    ('Husk & Shells',   'husk-shells',     '🥥'),
    ('Forestry Waste',  'forestry-waste',  '🪵'),
    ('Oilseed Cake',    'oilseed-cake',    '🌻'),
]

for name, slug, icon in categories:
    WasteCategory.objects.get_or_create(
        slug=slug, defaults={'name': name, 'icon': icon}
    )
print("Done!")
```

---

## 🤖 AI Chatbot Setup

1. Get an API key from [https://platform.openai.com](https://platform.openai.com)
2. Add it to your `.env`:
   ```
   OPENAI_API_KEY=sk-...your-key-here...
   ```
3. The chatbot uses **GPT-3.5-turbo** with a farming-focused system prompt.
4. If no API key is set, it falls back to a **built-in rule-based** response engine that handles common farming questions.

---

## 💬 Real-Time Chat Architecture

```
Browser (WebSocket)
      ↓
Django Channels (ASGI)
      ↓
ChatConsumer (consumers.py)
      ↓
Channel Layer (InMemoryChannelLayer in dev / Redis in prod)
      ↓
Broadcast to room group → All connected clients
```

### Production: Switch to Redis

```bash
pip install channels-redis redis
```

Update `settings.py`:
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('127.0.0.1', 6379)]},
    }
}
```

---

## 🏭 Production Deployment Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Set a strong `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Switch database to PostgreSQL
- [ ] Switch channel layer to Redis
- [ ] Run `python manage.py collectstatic`
- [ ] Serve with **Daphne** (ASGI): `daphne agriwealth.asgi:application`
- [ ] Set up Nginx as reverse proxy
- [ ] Configure media file serving

---

## 🌐 URLs Reference

| URL | View | Description |
|---|---|---|
| `/` | `core:home` | Landing page |
| `/about/` | `core:about` | About page |
| `/accounts/register/` | `accounts:register` | Sign up |
| `/accounts/login/` | `accounts:login` | Sign in |
| `/accounts/profile/` | `accounts:profile` | User profile |
| `/marketplace/` | `marketplace:marketplace` | Browse listings |
| `/marketplace/add/` | `marketplace:add_waste` | Add listing |
| `/marketplace/item/<id>/` | `marketplace:waste_detail` | Item detail |
| `/chat/` | `chat:chat_list` | Message inbox |
| `/chat/room/<id>/` | `chat:chat_room` | Chat room |
| `/chat/start/<item_id>/` | `chat:start_chat` | Start chat with farmer |
| `/chatbot/` | `chatbot:chatbot` | AI chatbot UI |
| `/chatbot/api/` | `chatbot:chatbot_api` | Chatbot API endpoint |
| `/admin/` | Django Admin | Admin dashboard |

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2 |
| Real-time | Django Channels + WebSocket |
| Frontend | HTML5 + Bootstrap 5 + Vanilla JS |
| Database | SQLite (dev) / PostgreSQL (prod) |
| AI Chatbot | OpenAI GPT-3.5 (+ rule-based fallback) |
| Static Files | WhiteNoise |
| Image Handling | Pillow |
| Config | python-decouple (.env) |

---

*Built with ❤️ for sustainable agriculture.*
