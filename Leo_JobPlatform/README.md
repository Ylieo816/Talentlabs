# Job Platform Backend

## Getting Started

1. Copy the environment variables:
```bash
cp backend/.env.local.example backend/.env
```

2. Build and run the project:
```bash
docker-compose up --build
```

3. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

4. Visit API docs:
```
http://localhost:8000/api/docs
```
