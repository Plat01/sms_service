# SMSService

Service for registration and authorization of users via SMS and Telegram codes.
In current version  this service works with [P1SMS](https://admin.p1sms.ru/) as sms provider.

## Run

```bash
cp .env.example .env
docker compose up --build
```

## Technologies Used

- **FastAPI**: Main web framework
- **PostgreSQL**: Primary database (via asyncpg and SQLModel for async ORM)
- **Redis**: In-memory data store used for save SMS codes
- **Docker**: Containerization platform for consistent deployment
- **Poetry**: Python dependency management and packaging
- **JWT**: JSON Web Tokens for secure authentication
- **Alembic**: Database migration tool
- **Pydantic**: Data validation
- **aiohttp**: Asynchronous HTTP client/server framework
- **Gunicorn**: Python WSGI HTTP Server for production

## Project Structure

The service is built using modern async Python with a focus on:
- Clean architecture principles
- Type safety with Pydantic models
- Asynchronous database operations
- Containerized deployment
- Environment-based configuration
