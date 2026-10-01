# Linux Commands

A personal reference for the Linux/Ubuntu commands learned during the deployment chapter.

## Navigation

### `pwd`

Prints the current working directory.

```bash
pwd
```

### `ls`

Lists files and directories in the current directory.

```bash
ls
```

### `ls -la`

Lists all files and directories, including hidden files, with detailed information.

```bash
ls -la
```

- `-l` → long/detailed format
- `-a` → include hidden files

`ls` can also be pointed at an absolute path instead of the current directory:

```bash
ls /path
```

### `ls -l`

Long format without hidden files. Useful for checking permissions.

```bash
ls -l script.sh
```

Example output: `-rwxr-xr-x 1 user user 76 Oct 1 15:53 script.sh`

The `x` characters mean the file is executable.

### `cd`

Changes the current directory.

```bash
cd folder_name
```

Common uses:

```bash
cd ..
cd ~
```

- `cd ..` → go to the parent directory
- `cd ~` → go to the home directory

### Path shortcuts

- `.` → the current directory
- `..` → the parent directory
- `~` → the home directory

### `exit`

Exits the current shell session.

```bash
exit
```

This closes the current shell (or SSH session). It's an important concept when working with remote servers — if you're inside a nested shell (e.g. after `sudo -s`, or an SSH session), `exit` takes you back one level rather than closing the terminal entirely.

### `mkdir`

Creates a directory.

```bash
mkdir folder_name
```

### `touch`

Creates a new empty file.

```bash
touch file.txt
```

## Files & Directories

### `rm`

Removes a file.

```bash
rm file.txt
```

`rm` can take several files at once:

```bash
rm file1.txt file2.txt
```

### `rm -r`

Removes a directory and its contents recursively.

```bash
rm -r folder_name
```

> ⚠️ Be careful with `rm` because deleted files are generally not moved to a recycle bin.

## Users & Permissions

### `whoami`

Shows the currently logged-in user.

```bash
whoami
```

### `sudo`

Runs a command with elevated/superuser privileges.

```bash
sudo command
```

### `sudo -u`

Runs a single command as a different user.

```bash
sudo -u postgres psql
```

This is how you log in to Postgres as admin: the Linux username must match the database role (peer authentication).

### `groups`

Shows the groups that the current user belongs to.

```bash
groups
```

### `chmod`

Changes file permissions (who may read, write, or run a file).

```bash
chmod +x script.sh
chmod 600 .env
```

- `+x` → makes a file executable (a script can't be run directly without it)
- `600` → only the owner can read and write (use this for `.env` files that hold secrets)

## Packages

### `apt`

Ubuntu's package manager, used to install, update, and remove software packages.

```bash
sudo apt update
sudo apt upgrade
sudo apt install package_name
sudo apt remove package_name
```

- `apt update` → updates the package information
- `apt upgrade` → upgrades installed packages
- `apt install` → installs a package (`-y` answers "yes" to the prompt automatically)
- `apt remove` → removes a package

## Processes

### `ps`

Shows running processes.

```bash
ps
```

### `ps aux`

Shows detailed information about running processes for all users.

```bash
ps aux
```

### `kill -9`

Force-kills a process by its PID. The PID can be found with `systemctl status` (the `Main PID` line) or `ps aux`.

```bash
sudo kill -9 <PID>
```

Used to simulate a crash. A service with `Restart=always` is started again by systemd.

## Services & systemd

### `systemctl`

Used to manage and check services controlled by systemd.

```bash
systemctl status service_name
sudo systemctl start service_name
sudo systemctl stop service_name
sudo systemctl restart service_name
sudo systemctl enable service_name
sudo systemctl disable service_name
```

- `status` → checks the current status of a service
- `start` → starts a service
- `stop` → stops a service
- `restart` → restarts a service (needed after editing the env file the service uses)
- `enable` → enables a service to start automatically at boot
- `disable` → disables automatic startup at boot

`enable` can be combined with `--now` to enable a service **and** start it immediately in one command. `disable --now` does the opposite (disable and stop):

```bash
sudo systemctl enable --now service_name
sudo systemctl disable --now service_name
```

Other useful `systemctl` commands:

```bash
sudo systemctl daemon-reload
systemctl cat service_name
```

- `daemon-reload` → makes systemd re-read service files. Run it **every time you create or edit a `.service` file** (not needed when only the env file changes)
- `cat` → prints a service's unit file

Reading the status output:

- `active (running)` → a long-running program that is alive
- `active (exited)` → a wrapper that ran once and finished (normal for `postgresql.service`)
- `Loaded: ... enabled/disabled` → whether it starts on boot

### `journalctl`

Used to view logs collected by systemd.

```bash
journalctl
journalctl -u service_name
journalctl -u service_name -f
journalctl -u service_name -n 20
```

- `-u` → u stands for the unit; shows logs for a specific service/unit
- `-f` → follow: new log lines appear live (stop watching with `Ctrl + C`; this does not stop the service)
- `-n 20` → show only the last 20 lines

This is the first place to look when a service misbehaves.

## Environment Variables

Environment variables store configuration values outside the application code.

They are commonly used for things such as database URLs, secret keys, and other configuration.

Example `.env` file:

```env
DATABASE_URL=...
SECRET_KEY=...
```

Setting and loading them in the shell:

```bash
export NAME=value
source .env
set -o allexport; source .env; set +o allexport
```

- `export NAME=value` → sets a variable for the current shell session
- `source .env` → loads a file whose lines are written as `export NAME=value`
- `set -o allexport; source .env; set +o allexport` → loads a plain `NAME=value` file

Things to remember:

- All of the above last only for the current shell session
- Putting the load command in `~/.profile` loads the variables for your own login shells
- **systemd services don't read `.profile`.** Use `EnvironmentFile=` in the `.service` file instead (plain `NAME=value` lines, no `export`)
- A running service keeps the values it started with. After editing the env file, run `sudo systemctl restart service_name`
- Protect the file: `chmod 600 .env`

## `.service` Files

A `.service` file is a systemd unit file that tells systemd how to run and manage an application as a service (e.g. what command starts it, when it should restart, what it depends on).

Custom service files go in `/etc/systemd/system/`. The file name becomes the service name (`api.service` → `systemctl status api`).

Template:

```ini
[Unit]
Description=Short description of the service
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/project
EnvironmentFile=/path/to/.env
ExecStart=/full/path/to/program
Restart=always

[Install]
WantedBy=multi-user.target
```

- `[Unit]` → description and start order (`After=network.target` = start after the network is up)
- `[Service]` → who runs it, where, with which environment variables, which command, and restart behavior
- `[Install]` → what `systemctl enable` uses to start the service on boot
- `User=` → run as a normal user, never as root
- `WorkingDirectory=` → the folder the program starts in
- `EnvironmentFile=` → file with `NAME=value` lines (a `-` before the path, `EnvironmentFile=-/path`, means "don't fail if the file is missing")
- `ExecStart=` → needs the **full path** to the program; services don't search `PATH`
- `Restart=always` → systemd starts it again if it crashes

After creating or editing the file:

```bash
sudo systemctl daemon-reload
sudo systemctl start service_name
systemctl status service_name
```

This is what `systemctl` and `journalctl` ultimately interact with.

## Text Editors & File Viewing

### `nano`

A simple and beginner-friendly terminal text editor.

```bash
nano file.txt
```

Useful shortcuts:

- `Ctrl + O` → save
- `Enter` → confirm filename
- `Ctrl + X` → exit
- `Ctrl + W` → search
- `Ctrl + K` → cut a line
- `Ctrl + U` → paste a cut line

If you open a file with `nano` and don't make any changes, simply press `Ctrl + X` to exit.

### `vim`

A more powerful terminal text editor.

```bash
vim file.txt
```

Vim has different modes and uses commands such as:

- `:wq` → to save and quit
- `:q` → to quit when there are no unsaved changes
- `:q!` → to quit without saving changes

### `vi`

`vi` is the older/original Unix text editor. Vim (Vi IMproved) was developed as an improved version of `vi`.

Conceptually:

```text
vi  → original editor
vim → improved version of vi
```

They share many of the same basic concepts and commands.

**Which editor will we commonly use?**

During this deployment/Linux journey, we'll commonly use `nano` because it is simpler and more beginner-friendly. It doesn't require learning Vim's different modes just to make a small configuration change.

Vim is still useful to know because we will encounter it on Linux servers and in many tutorials.

### `cat`

Displays the contents of a file directly in the terminal.

```bash
cat file.txt
```

For example:

```bash
cat notes.txt
```

prints the contents of `notes.txt` to the terminal.

### `tail`

Prints the last lines of a file.

```bash
tail -n 25 file.txt
```

- `-n 25` → show the last 25 lines

### `grep` and the pipe `|`

The pipe `|` sends the output of one command into the next command. `grep` keeps only the lines that contain a word.

```bash
ls ~ | grep test
```

This lists your home folder and shows only the entries containing "test" (prints nothing if there are none).

## Quick Reference

| Command | Purpose |
| --- | --- |
| `pwd` | Show current directory |
| `ls` | List files and directories |
| `ls -la` | List all files with detailed information |
| `ls -l` | List files with permissions |
| `ls /path` | List contents of a specific (absolute) path |
| `cd` | Change directory |
| `cd ..` | Go to parent directory |
| `cd ~` | Go to home directory |
| `.` / `..` / `~` | Current / parent / home directory shortcuts |
| `mkdir` | Create a directory |
| `touch` | Create an empty file |
| `exit` | Exit the current shell session |
| `rm` | Remove a file (or several) |
| `rm -r` | Remove a directory and its contents |
| `whoami` | Show current user |
| `sudo` | Run command with elevated privileges |
| `sudo -u <user>` | Run a command as another user |
| `groups` | Show user's groups |
| `chmod +x` | Make a file executable |
| `chmod 600` | Owner-only read/write (for `.env` files) |
| `apt` | Manage Ubuntu packages |
| `ps` | Show running processes |
| `ps aux` | Show detailed running processes |
| `kill -9 <PID>` | Force-kill a process |
| `systemctl` | Manage systemd services |
| `systemctl enable --now` | Enable a service and start it immediately |
| `systemctl disable --now` | Disable a service and stop it immediately |
| `systemctl daemon-reload` | Re-read service files after creating/editing one |
| `systemctl cat` | Show a service's unit file |
| `journalctl` | View systemd logs |
| `journalctl -u <service>` | View logs for a specific service/unit |
| `journalctl -u <service> -f` | Follow a service's logs live |
| `journalctl -u <service> -n 20` | Show the last 20 log lines of a service |
| `nano` | Simple terminal text editor |
| `vim` | Advanced terminal text editor |
| `vi` | Original Unix text editor |
| `cat` | Display file contents |
| `tail -n N` | Show the last N lines of a file |
| `grep` and `\|` | Filter a command's output with a pipe |