# Migrations How-to

<br>

### 1. Autogenerate a migration from ORM models

```
$ alembic revision --autogenerate -m "Add table foo"
```

### 2. Run migration on database

```
$ DATABASE_URL="sqlite:///path/to/db.sqlite" alembic upgrade head
```