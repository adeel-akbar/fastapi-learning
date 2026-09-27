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
- [ ] SSH
- [ ] Ubuntu server deployment
- [ ] Gunicorn
- [ ] Systemd service configuration
- [ ] NGINX
- [ ] Domain
- [ ] SSL/HTTPS
- [ ] Firewall
- [ ] Production deployment through Ubuntu
