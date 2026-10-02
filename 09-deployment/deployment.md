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
>
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

### Gunicorn with Uvicorn workers

- Uvicorn is a single process; Gunicorn is a process manager that runs several Uvicorn workers
- Needs the `uvicorn-worker` package (the worker class moved out of Uvicorn itself)
- Command:

```bash
gunicorn -w 4 -k uvicorn_worker.UvicornWorker main:app --bind 127.0.0.1:8000
```

- One **master** process manages the **workers**; only workers handle requests
- If a worker dies, the master starts a replacement
- If the master dies, systemd (`Restart=always`) replaces the whole group, so there are two layers of protection
- Bind to `127.0.0.1:8000` once Nginx is in front
- Practiced on WSL with a tiny app that returns its worker PID; different requests were answered by different workers
- On the real Oracle VM (1 GB RAM), used 1 worker instead of 4 to fit the small server:

```bash
gunicorn -w 1 -k uvicorn_worker.UvicornWorker app.main:app --bind 127.0.0.1:8000
```

- Tested the real application manually before putting it behind systemd and Nginx

### systemd service for Gunicorn

Practiced on WSL with a practice app. Template (same shape as the real one):

```ini
[Unit]
Description=Gunicorn practice app
After=network.target
[Service]
User=your_user
WorkingDirectory=/home/your_user/project
ExecStart=/home/your_user/project/.venv/bin/gunicorn -w 4 -k uvicorn_worker.UvicornWorker main:app --bind 127.0.0.1:8000
Restart=always
[Install]
WantedBy=multi-user.target
```

- `ExecStart` needs the full path to the venv's `gunicorn`, because a service doesn't activate the venv
- For the real API, also add `EnvironmentFile=` pointing to the production `.env` (without a `-`, so a missing file fails loudly), and use the real app path (for example `app.main:app`)
- After creating the file: `daemon-reload`, `start`, check `status`, and `enable` so it starts on boot
- A service that isn't `enabled` will not come back after a reboot
- On the real server, created `/etc/systemd/system/fastapi.service` using the `ubuntu` user, the real project directory, production `.env`, and the venv's Gunicorn executable
- Enabled the service and confirmed it automatically started again after a full VM reboot

### Nginx as a reverse proxy

Practiced on WSL in front of the practice service.

- Nginx listens on port 80 (and 443 for HTTPS) and forwards requests to Gunicorn on `127.0.0.1:8000`
- The browser never talks to Gunicorn directly
- Real config files live in `sites-available/`; Nginx only reads `sites-enabled/`, which holds shortcuts (symlinks) to them
- The default welcome-page site should be disabled so it doesn't answer instead of the app
- Test the config with `sudo nginx -t`, then apply it with `sudo systemctl reload nginx`
- The key line is `proxy_pass http://127.0.0.1:8000;`
- **502 Bad Gateway** means Nginx is fine but the app behind it isn't answering; check `systemctl status` and `journalctl -u` for the API service
- Two ways to configure it: the tutor's (edit the `default` file) or a separate file named after the app; both work
- On the real server, created `/etc/nginx/sites-available/fastapi`, enabled it with a symlink in `sites-enabled/`, and removed the default site
- Verified the config with `sudo nginx -t`, reloaded Nginx, and confirmed `curl http://localhost\` reached the FastAPI app through Nginx
- Confirmed Nginx automatically started again after a full VM reboot
Minimal config:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Domain and DNS (concept)

- A domain is a name rented yearly from a registrar, so people can use a name instead of an IP address
- DNS turns the name into an IP address; it knows nothing about ports
- To point the domain at the server, add **one A record** in the registrar's DNS page: name `@`, value = the VM's public IP, then wait for it to take effect
- A CNAME (for example `www` → the main domain) is optional
- A domain is only needed for HTTPS; without one the API works at `http://<VM-IP>`

### HTTPS with Certbot (concept)

- A certificate proves "this public key belongs to this domain"; Let's Encrypt issues them for free and browsers trust it
- Certbot automates getting the certificate and edits the Nginx config for me
- It adds a `listen 443 ssl` block with the certificate paths, and turns the port 80 block into a redirect (301) to HTTPS
- Needs: a real domain already pointing at the server, and port 80 open for the verification step
- Certificates last 90 days; Certbot sets up automatic renewal (check with `sudo certbot renew --dry-run`)
- Nginx handles HTTPS and forwards plain HTTP to Gunicorn on localhost, so the app needs no certificate handling

### Firewall (concept)

- A firewall decides which ports the outside world can reach; block everything, then allow only what is needed
- Allow: `22` (SSH), `80` (HTTP), `443` (HTTPS)
- Don't allow `8000` (Gunicorn) or `5432` (Postgres): only Nginx and the app use them, over `localhost`
- Allow SSH **before** enabling UFW, or I can lock myself out
- Ubuntu's firewall tool is UFW (commands are in `linux_commands.md`)
- Oracle Cloud has **two layers**: the Oracle console (security list / network rules) and the firewall rules inside the VM. Ports 80 and 443 must be opened in both
- The Ubuntu image on Oracle ships with restrictive rules of its own, so opening a port only in the console may not be enough
- On the real server, enabled UFW with ports `22`, `80`, and `443` allowed; ports `8000` and `5432` remained private
- Added Oracle Security List ingress rules for ports `80` and `443`
- Public HTTP initially still timed out even though Nginx, UFW, the Oracle Security List, route table, and public subnet were correct
- `iptables` showed an Oracle Ubuntu image `REJECT` rule before the UFW chains, so HTTP/HTTPS traffic was rejected before reaching the UFW allow rules
- Added accept rules for ports `80` and `443` before that reject rule, then installed `iptables-persistent` so the rules survive reboot
- The exact `iptables` syntax is troubleshooting/reference material, not something I need to memorize

### Oracle Cloud VM and SSH

- Created an Oracle Cloud Always Free-eligible Ubuntu 24.04 VM for the manual deployment
- Initially tried the Ampere A1 Flex shape, but it had no available capacity; used `VM.Standard.E2.1.Micro` instead (1 OCPU / 1 GB RAM)
- Created a VCN, public subnet, Internet Gateway, and a route to `0.0.0.0/0`
- The VM has a public IP for internet access and a private IP for communication inside the cloud network
- Connected from Windows using an SSH private key:

```bash
ssh -i <private-key> ubuntu@<public-ip>
```

- Oracle's Ubuntu image uses the normal `ubuntu` user with `sudo`; direct root SSH is not needed
- Installed/updated the required server packages: Python/venv, PostgreSQL, Nginx, and project dependencies

### Real PostgreSQL setup

- Created a dedicated PostgreSQL role and database for the real FastAPI application instead of using the `postgres` superuser
- Verified the application-style TCP/password connection with `psql -h localhost ...`
- Kept PostgreSQL local to the VM; port `5432` was never opened publicly
- The production database URL in `.env` points to this local PostgreSQL database
- Ran `alembic upgrade head` on the server to create/update the production schema
- During migration, a PostgreSQL driver mismatch (`psycopg2` vs the project's Psycopg 3 setup) had to be corrected in the database URL/configuration

### Production application setup

- Cloned the real FastAPI social API repository onto the VM
- Created a project `.venv` and installed `requirements.txt`
- Installed Gunicorn and `uvicorn-worker` for production serving
- Created a fresh production `.env` with the database URL and a new secret key
- Protected the `.env` with `chmod 600`
- Pydantic Settings can read the `.env` directly; systemd uses `EnvironmentFile=` to provide the same values to the service
- Verified the application manually before creating the permanent service

### Architecture notes

- The browser talks to the VM's IP on port 80/443; Nginx owns those ports
- Nginx forwards to Gunicorn on `127.0.0.1:8000`, and the app talks to Postgres on `localhost:5432`
- `127.0.0.1` accepts connections only from the same machine; `0.0.0.0` listens on all network interfaces
- `0.0.0.0` is needed on platforms like Render, where the router runs in a separate container
- The app connects to the database over TCP, so it uses a password even when the database is on the same machine
- Final real-server request path: Internet → Oracle network rules → VM firewall/iptables → Nginx on port 80 → Gunicorn/FastAPI on `127.0.0.1:8000` → PostgreSQL on `localhost:5432`
- A successful full VM reboot confirmed that systemd, Nginx, and the persisted firewall rules restore the deployment automatically

### Differences from the course (to do differently)

- Use an SSH key and a non-root user (`ubuntu` on Oracle Cloud) instead of root with a password
- Create the venv with `python3 -m venv`
- Keep Postgres on localhost and leave the default `pg_hba.conf` alone
- Don't use the `postgres` superuser for the app
- Use fresh production secrets (a new `SECRET_KEY` and DB password)
- Load env vars for the service with `EnvironmentFile=`, not `.profile`
- Protect the env file with `chmod 600`
- Bind Gunicorn to `127.0.0.1`, not `0.0.0.0`
- Use `uvicorn-worker` for the Gunicorn worker class
- Open ports 80 and 443 in both the Oracle console (security list) and the OS firewall
- Don't open port 5432 to the internet

### Plan for the real server

1. Create the Oracle VM and connect with SSH
2. Install Python, venv, Postgres and Nginx
3. Create the app's database role and database
4. Clone the repo, create the venv, install requirements
5. Create the production `.env` (`chmod 600`) and run `alembic upgrade head`
6. Create the systemd service with `EnvironmentFile=`, then `enable --now`
7. Create the Nginx config, enable it, `nginx -t`, reload
8. Open the firewall (OS and Oracle console)
9. Optional: point a domain at the VM's IP, then run Certbot for HTTPS (not implemented because no domain was purchased)
10. Redeploy flow: `git pull`, `pip install -r requirements.txt` if needed, `alembic upgrade head` if the schema changed, `sudo systemctl restart <service>`

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
- [x] Gunicorn with Uvicorn workers (practiced on WSL)
- [x] systemd service for a Gunicorn app (practiced on WSL)
- [x] Nginx reverse proxy (practiced on WSL)
- [x] DNS A record and HTTPS/Certbot concepts (not implemented because no domain was purchased)
- [x] SSH into the Oracle Ubuntu VM with an SSH key
- [x] Create and configure the Oracle VM
- [x] Real PostgreSQL role/database on the Ubuntu server
- [x] Clone the real API, create venv, install dependencies and production `.env`
- [x] Run Alembic migrations on the Oracle VM
- [x] Real Gunicorn + systemd service for the FastAPI API
- [x] Real Nginx reverse proxy
- [x] UFW + Oracle Security List firewall configuration
- [x] Diagnose Oracle Ubuntu `iptables` REJECT rule and persist the fix
- [x] Public HTTP deployment through the VM's public IP
- [x] Reboot verification (FastAPI/systemd, Nginx and firewall rules returned automatically)
- [ ] Domain — intentionally skipped (no domain purchased)
- [ ] SSL/HTTPS with Certbot — intentionally skipped because it requires a domain
