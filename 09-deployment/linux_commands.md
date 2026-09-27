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

### `groups`

Shows the groups that the current user belongs to.

```bash
groups
```

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
- `apt install` → installs a package
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
- `restart` → restarts a service
- `enable` → enables a service to start automatically at boot
- `disable` → disables automatic startup at boot
`enable` can be combined with `--now` to enable a service **and** start it immediately in one command:

```bash
sudo systemctl enable --now service_name
```

### `journalctl`

Used to view logs collected by systemd.

```bash
journalctl
journalctl -u service_name
```

- `-u` → u stands for the unit shows logs for a specific service/unit.

## Environment Variables

Environment variables store configuration values outside the application code.

They are commonly used for things such as database URLs, secret keys, and other configuration.

Example:

```env
DATABASE_URL=...
SECRET_KEY=...
```

## `.service` Files

A `.service` file is a systemd unit file that tells systemd how to run and manage an application as a service (e.g. what command starts it, when it should restart, what it depends on).

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

## Quick Reference

| Command | Purpose |
| --- | --- |
| `pwd` | Show current directory |
| `ls` | List files and directories |
| `ls -la` | List all files with detailed information |
| `ls /path` | List contents of a specific (absolute) path |
| `cd` | Change directory |
| `cd ..` | Go to parent directory |
| `cd ~` | Go to home directory |
| `.` / `..` / `~` | Current / parent / home directory shortcuts |
| `mkdir` | Create a directory |
| `touch` | Create an empty file |
| `exit` | Exit the current shell session |
| `rm` | Remove a file |
| `rm -r` | Remove a directory and its contents |
| `whoami` | Show current user |
| `sudo` | Run command with elevated privileges |
| `groups` | Show user's groups |
| `apt` | Manage Ubuntu packages |
| `ps` | Show running processes |
| `ps aux` | Show detailed running processes |
| `systemctl` | Manage systemd services |
| `systemctl enable --now` | Enable a service and start it immediately |
| `journalctl` | View systemd logs |
| `journalctl -u <service>` | View logs for a specific service/unit |
| `nano` | Simple terminal text editor |
| `vim` | Advanced terminal text editor |
| `vi` | Original Unix text editor |
| `cat` | Display file contents |
