<p align="center">
  <img src="vari-mitra.png" alt="Vari Mitra Logo" width="180">
</p>

<h1 align="center">Vari Mitra <sup>వరి మిత్ర</sup></h1>
<p align="center"><em>A digital paddy brokerage management platform connecting farmers, workers,and brokers.</em></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white">
  <img src="https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-EF9421?logo=creativecommons&logoColor=white">
</p>

---

## Overview

Vari Mitra (Telugu for **"Paddy Friend"**) is a Django-based web application that streamlines the paddy (rice) supply chain. It digitizes the entire lifecycle — from a farmer arriving at the mill with their harvest, through packing, pickup, and final transport — with automatic brokerage calculation, Aadhaar-based farmer verification, and real-time business analytics.

Built for regional use in Telugu-speaking areas, the UI is presented in Telugu (వరి మిత్ర) with an earth-toned design language.

---

## Features

- **Aadhaar QR Ticket Booking** — Farmers scan their Aadhaar SecureQR to auto-fill name, UID, and location; manual fallback available.
- **5-Stage Status Lifecycle** — Every ticket progresses through: `Ticket Booked → Ongoing → Packed → Picked → Transported`.
- **Live Paddy Rates** — Dashboard displays government-mandated rates per paddy variety with a live pulse indicator.
- **Ticket Tracking** — Public tracking page with a visual progress bar and timeline for any ticket ID.
- **Auto-Calculated Brokerage** — Brokerage is computed automatically from bag count and worker group fee rates.
- **Worker & Vehicle Management** — Register workers, form groups with leaders, and assign vehicles to consignments.
- **Business Analytics Dashboard** — Real-time admin dashboard showing total bags, worker fees, revenue, and profit.
- **Telugu-Language UI** — Full Telugu branding and Noto Sans Telugu typeface for comfortable regional use.
- **Responsive Design** — Mobile-first layout with hamburger navigation, built with Tailwind CSS.

---

## Tech Stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| **Language**   | Python 3.13                         |
| **Framework**  | Django 6.0.4                        |
| **Database**   | SQLite (development)                |
| **Frontend**   | Tailwind CSS (CDN), html5-qrcode    |
| **Font**       | Noto Sans Telugu (Google Fonts)     |

---

## Data Model

```
┌──────────────┐     ┌────────────────────────┐
│  PaddyInfo   │     │    FarmerTicket         │
│──────────────│     │────────────────────────│
│ paddy_variety│────▶│ paddy_variety (FK)      │
│ paddy_rate   │     │ tracking_id (auto-gen)  │
└──────────────┘     │ farmer_name             │
                     │ mobile_num              │
┌──────────────┐     │ aadhar_num              │
│  Workers     │     │ location                │
│──────────────│     │ moisture                │
│ name         │     │ status (5 stages)       │
│ mobile_num   │     │ created_at              │
│ status       │     └───────────┬────────────┘
└──────┬───────┘                 │
       │ 1:N                1:1  │
       ▼                        ▼
┌──────────────┐     ┌────────────────────────┐
│ WorkersGroup │     │ FarmerConsignmentInfo   │
│──────────────│     │────────────────────────│
│ group_leader │◀────│ workers_group (FK)      │
│ group_members│     │ vehicle (FK)            │
│ group_revenue│     │ num_bags (40kg)         │
└──────────────┘     │ total_brokerage (auto)  │
                     │ consignment_created_by  │
                     └────────────────────────┘

┌──────────────┐     ┌──────────────────────┐
│ VehicleInfo  │     │    AdminSettings      │
│──────────────│     │──────────────────────│
│ vehicle_num  │     │ workers_group_fee     │
│ driver_name  │     │ mill_fee_per_bag      │
│ driver_contact│    └──────────────────────┘
└──────────────┘
```

**7 models** in total: `FarmerTicket`, `FarmerConsignmentInfo`, `PaddyInfo`, `Workers`, `WorkersGroup`, `VehicleInfo`, `AdminSettings` (+ proxy model `AdminDashboard`).

---

## Business Workflow

1. **Ticket Booking** — Farmer arrives with paddy → scans Aadhaar QR or enters details manually → system generates a unique tracking ID (e.g., `VIJA-AF32` from location prefix + UUID).
2. **Processing** — Ticket status advances through 5 stages as the paddy is weighed, dried, packed, picked up, and transported.
3. **Consignment Creation** — When a ticket reaches the `Ongoing` stage, a broker creates a consignment linking bags, workers group, and vehicle.
4. **Brokerage Calculation** — Automatically computed on save:
   ```
   total_brokerage = (num_bags × 40 / 75) × worker_group_fee_per_bag
   ```
5. **Transport** — Final status update marks the consignment as `Transported`, completing the cycle.

---

## Getting Started

### Prerequisites

- Python 3.13+
- pip (or uv/pipenv)

### Setup (pip)

```bash
# Clone the repository
git clone <repo-url>
cd vari-mitra

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install django

# Run database migrations
python3 manage.py migrate

# Create an admin user
python3 manage.py createsuperuser

# Start the development server
python3 manage.py runserver
```

### Setup (uv)

```bash
# Clone the repository
git clone <repo-url>
cd vari-mitra

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install django

# Run database migrations
python3 manage.py migrate

# Create an admin user
python3 manage.py createsuperuser

# Start the development server
python3 manage.py runserver
```

Visit **http://127.0.0.1:8000/** to open the app, and **http://127.0.0.1:8000/admin/** to manage data.

### Helper Scripts

| Script          | Command                                  |
|-----------------|------------------------------------------|
| `run.sh`        | Starts the dev server                    |
| `migrate.sh`    | Runs `makemigrations` then `migrate`     |
| `reset.sh`      | Deletes DB + migrations, re-creates everything |

---

## Project Structure

```
vari-mitra/
├── config/                  # Django project configuration
│   ├── asgi.py              # ASGI entry point
│   ├── settings.py          # Django settings (SQLite, apps, middleware)
│   ├── urls.py              # Root URL routing
│   └── wsgi.py              # WSGI entry point
├── farmers/                 # Core application
│   ├── admin.py             # Admin registrations + analytics dashboard
│   ├── forms.py             # FarmerTicket ModelForm (Aadhaar-readonly fields)
│   ├── models.py            # 7 domain models
│   ├── urls.py              # App URL routes
│   ├── views.py             # Home + book_ticket views
│   ├── migrations/          # Database migrations
│   ├── static/              # Static assets (logo, paddy image)
│   └── templates/farmers/   # Django templates (5 files)
│       ├── layout.html      # Base layout (nav, footer, watermark)
│       ├── index.html       # Home dashboard
│       ├── book_ticket.html # Aadhaar QR + booking form
│       ├── track_ticket.html# Ticket tracking + progress bar
│       └── _status_badge.html # Circular rubber-stamp badges
├── templates/admin/         # Admin template overrides
│   └── analytics_dashboard.html  # Business analytics dashboard
├── manage.py                # Django CLI entry point
├── pyproject.toml           # Project metadata
├── requirements.txt         # Python dependencies
├── .python-version          # Python version (3.13)
└── vari-mitra.png           # Project logo
```

---

## URL Routes

| Route                          | View          | Description                |
|--------------------------------|---------------|----------------------------|
| `/`                            | `home`        | Dashboard + ticket lookup  |
| `/farmers/`                    | `home`        | Dashboard (alternate)      |
| `/farmers/book_ticket/`        | `book_ticket` | Aadhaar QR ticket booking  |
| `/admin/`                      | Django Admin  | Data management + analytics |

---

## Development

```bash
# Run the development server
python3 manage.py runserver

# Create migrations after model changes
python3 manage.py makemigrations farmers
python3 manage.py migrate

# Open Django shell
python3 manage.py shell
```

### Seeding Initial Data

Access the Django admin at `/admin/` to add:
- **Paddy varieties** and their government rates
- **AdminSettings** singleton (worker fee per bag, mill fee per bag)
- **Workers** and **WorkersGroups**
- **VehicleInfo** entries

---

## Roadmap

- [ ] PostgreSQL production database configuration
- [ ] Authentication for farmers (self-service portal)
- [ ] Export reports (PDF/CSV per season)
- [ ] SMS notifications on status changes
- [ ] Docker setup for deployment
- [ ] Test suite implementation

---

## License

Copyright © 2026 Prasad Raju. Some rights reserved.

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).

---

## Acknowledgments

Developed by **Prasad Raju**. Built with Django and Tailwind CSS.

---

<p align="center">
  <sub>Vari Mitra — వరి మిత్ర · Paddy Friend · <code>paddy-broker</code></sub>
</p>
