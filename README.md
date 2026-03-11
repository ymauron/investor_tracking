# Investor Tracking

Healthcare-focused LP/GP investor intelligence platform for tracking individual investor backgrounds, firm hierarchies, deal flow, and movement events.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.12+ (for local backend development)

### Run with Docker

```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env with your own values

# Start all services
docker compose up --build

# Run database migrations
docker compose exec backend alembic upgrade head

# Seed mock data
docker compose exec backend python -m app.seed.seed_data
```

The app will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

Default credentials: `admin` / value of `ADMIN_PASSWORD` in `.env`

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL 16
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, react-force-graph-2d
- **Infrastructure:** Docker Compose, Nginx, GitHub Actions CI/CD

## Deployment

Configure these GitHub Secrets for CI/CD:
- `EC2_HOST` — your EC2 public IP or hostname
- `EC2_USER` — SSH username (e.g., `ubuntu`)
- `EC2_SSH_KEY` — private SSH key for EC2 access
