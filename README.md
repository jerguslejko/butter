# _butter_

So your local development goes like po masle.

## What is this?

Think of this as `docker-compose` without `docker` (_butter_ manages local processes). But also with a task runner (you can do `butter run ...` like in yarn/npm). And built on `supervisor`.

## Example

```yaml
name: seagull 
programs:
  - name: backend
    command: source venv/bin/activate && python manage.py runserver
    working-directory: backend 
    env:
      DJANGO_SETTINGS_MODULE: seagull.config.local
  - name: frontend
    command: yarn dev
    working-directory: app-frontend
commands:
  - name: fresh
    command: source venv/bin/activate && psql -c "drop database seagull" && psql -c "create database seagull" && python manage.py migrate
    mode: downtime
    working-directory: backend 
```
