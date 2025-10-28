# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KRU Community is a bilingual (Korean/Russian) community platform for Russians/Russian speakers in Korea. The platform includes social features, business directory, automated translation, and OAuth integration.

## Architecture

### Tech Stack
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, next-intl
- **Backend**: FastAPI, SQLAlchemy, Alembic, PostgreSQL, Redis
- **Infrastructure**: Docker, Docker Compose, Nginx
- **External Services**: Google Cloud Translation, OAuth (Google, Kakao, VK), AWS S3

### Project Structure
```
kru-community/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── api/      # API routes (auth, users, posts, comments, etc.)
│   │   ├── core/     # Configuration, security, dependencies
│   │   ├── db/       # Database connection and utilities
│   │   ├── models/   # SQLAlchemy models (User, Post, Partner, etc.)
│   │   ├── schemas/  # Pydantic schemas for validation
│   │   ├── services/ # Business logic (email, translation)
│   │   └── utils/    # Utilities (logger, validators)
│   ├── migrations/   # Alembic database migrations
│   └── requirements.txt
├── frontend/         # Next.js application
│   ├── app/          # App Router pages and layouts
│   ├── components/   # React components organized by feature
│   ├── i18n/         # Internationalization setup
│   ├── locales/      # Translation files (ko.json, ru.json)
│   └── package.json
└── docker-compose.yml
```

## Development Commands

### Local Development Setup
```bash
# Backend setup
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend setup
cd frontend
npm install
npm run dev

# Database migrations
cd backend
alembic upgrade head
```

### Docker Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Database migrations in Docker
docker-compose run backend alembic upgrade head

# Restart specific service
docker-compose restart backend
```

### Testing & Quality
```bash
# Frontend
cd frontend
npm run lint
npm run build

# Backend tests (if test files exist)
cd backend
pytest
```

## Key System Components

### Authentication & Authorization
- Multi-provider OAuth (Google, Kakao, VK) implemented in `backend/app/api/auth.py`
- JWT tokens with refresh mechanism
- User model supports social login metadata

### Internationalization
- Frontend uses next-intl for Korean/Russian translation
- Backend integrates Google Cloud Translation API for automatic content translation
- Translation service in `backend/app/services/translation.py`

### Database Models
- **User**: Core user model with social login support
- **Post**: Community posts with category relationships
- **Partner**: Business directory entries
- **Admin**: Administrative user management
- All models use SQLAlchemy with Alembic migrations

### API Structure
- RESTful APIs under `/api` prefix
- Modular route organization by feature (auth, users, posts, comments, categories, partners, admin)
- Consistent error handling and validation using Pydantic

### Configuration Management
- Environment-based configuration in `backend/app/core/config.py`
- Settings for database, OAuth providers, AWS S3, email, rate limiting
- Docker environment variables in docker-compose.yml

## Development Guidelines

### Database Changes
1. Create migration: `alembic revision --autogenerate -m "description"`
2. Review generated migration file
3. Apply: `alembic upgrade head`
4. For Docker: `docker-compose run backend alembic upgrade head`

### Adding New Features
1. Backend: Add model → migration → schema → API route → service logic
2. Frontend: Add component → integrate with API → add translations
3. Update both Korean and Russian locales for any user-facing text

### Environment Variables
- Backend requires `.env` file (see DEPLOYMENT.md for full list)
- Frontend requires `.env.local` with API URL configuration
- Docker uses environment variables from docker-compose.yml

### Code Organization
- Follow existing patterns: models in `models/`, APIs in `api/`, business logic in `services/`
- Frontend components organized by feature areas (layout, home, auth, etc.)
- Maintain separation between data models, API schemas, and business logic

## Troubleshooting

### Common Issues
- **Database connection**: Check PostgreSQL container status and DATABASE_URL
- **Translation errors**: Verify Google Cloud credentials and project ID
- **OAuth issues**: Confirm client IDs and secrets are properly configured
- **CORS errors**: Update CORS_ORIGINS in backend configuration
- **Build failures**: Check Node.js version compatibility (requires 18+)

### Debugging
- Backend logs: `docker-compose logs -f backend`
- Database access: `docker exec -it kru_postgres psql -U kru_user -d kru_community`
- Redis access: `docker exec -it kru_redis redis-cli`