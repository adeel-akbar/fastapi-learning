# Deployment

## Deployment Concepts

Learned the basics of deploying a FastAPI application to production.

### Git & GitHub

- Git prerequisites
- Git installation
- Using GitHub for source control and deployment

### Heroku

- Learned the basic Heroku deployment workflow from the course
- Procfile
- PostgreSQL database
- Environment variables
- Alembic migrations
- Pushing code changes to production

> Heroku was used in the course, but I used Render for my actual deployment because Heroku is now paid.

### Render + Neon

Deployed my FastAPI social API using:

- Render — application hosting
- Neon — PostgreSQL database

Learned:

- Creating a production database on Neon
- Connecting the application to the production database
- Configuring environment variables
- Deploying the FastAPI application through Render
- Running Alembic migrations on the production database
- Pushing changes to the deployed application

## Ubuntu / Linux Server

Started learning Ubuntu and Linux server administration for manual deployment.

### Concepts learned

- Linux filesystem navigation
- Users and groups
- File management
- Package management
- Processes
- Services
- `systemd`
- Using `systemctl` to manage/check services
- Using `journalctl` to view service logs
- Writing a `systemd` service file (`User`, `WorkingDirectory`, `EnvironmentFile`, `ExecStart`, `Restart`)
- `Restart=always` brings a crashed service back automatically
- An env file is read once when the service starts, so changes need a restart
- Environment variables set with `export`/`source` or `.profile` are not visible to systemd services; use `EnvironmentFile=`

### PostgreSQL on Ubuntu

- Postgres roles (database users) are separate from Linux users
- **Peer authentication** applies to `local` (Unix socket) connections: Postgres compares the Linux username with the database role name, and no password is used
- **Password authentication** applies to `host` (network/TCP) connections, which is how the FastAPI app connects (`scram-sha-256` by default)
- `pg_hba.conf` is a list of rules read top to bottom, and the first match wins
- The default rules already work for an app running on the same machine as the database, so no changes are needed
- Don't open Postgres to the internet (no `listen_addresses = '*'`, no `0.0.0.0/0` rule, no public port 5432)
- Use a dedicated limited role and database for the app instead of the `postgres` superuser (least privilege):

```sql
CREATE USER app_user WITH PASSWORD '...';
CREATE DATABASE app_db OWNER app_user;
```

- Admin access: `sudo -u postgres psql`
- Test the same way the app connects: `psql -h localhost -U app_user -d app_db`
- Useful `psql` commands: `\du` (list roles), `\l` (list databases), `\q` (quit)
- Prompt `postgres=#` means superuser, `app_db=>` means a regular user

### Architecture notes

- The app connects to the database over TCP, so it uses a password even when the database is on the same machine
- `127.0.0.1` accepts connections only from the same machine; `0.0.0.0` listens on all network interfaces
- With Nginx in front on the same VM, bind Gunicorn to `127.0.0.1:8000` so the only way in is through Nginx
- `0.0.0.0` is needed on platforms like Render, where the router runs in a separate container

### Differences from the course (to do differently)

- Use an SSH key and a non-root user (`ubuntu` on Oracle Cloud) instead of root with a password
- Create the venv with `python3 -m venv`
- Keep Postgres on localhost and leave the default `pg_hba.conf` alone
- Don't use the `postgres` superuser for the app
- Use fresh production secrets (a new `SECRET_KEY` and DB password)
- Load env vars for the service with `EnvironmentFile=`, not `.profile`
- Protect the env file with `chmod 600`
- Open ports 80 and 443 in both the Oracle console (security list) and the OS firewall

## Deployment Progress

- [x] Git & GitHub
- [x] Deploy with Render
- [x] Neon PostgreSQL
- [x] Production environment variables
- [x] Alembic migrations
- [x] Push changes to production
- [x] Basic Linux commands
- [x] Processes and services
- [x] systemd / systemctl / journalctl
- [x] Postgres roles, peer vs password authentication (practiced on WSL)
- [x] systemd service file with `EnvironmentFile` (practiced on WSL)
- [ ] SSH
- [ ] Ubuntu server deployment
- [ ] Gunicorn
- [ ] Systemd service for the real API (Gunicorn)
- [ ] NGINX
- [ ] Domain
- [ ] SSL/HTTPS
- [ ] Firewall
- [ ] Production deployment through Ubuntu
