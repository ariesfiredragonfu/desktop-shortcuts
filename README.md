# Desktop Shortcuts Backup Tool

A tool for backing up and restoring desktop shortcuts in Linux systems. This tool helps you maintain consistent desktop configurations across different machines or after system reinstalls.

## Directory Structure

```
desktop-shortcuts/
├── scripts/         # Backup and restore scripts
├── src/            # Source code for the main functionality
└── config/         # Configuration files and templates
```

## Features

- Backup desktop shortcuts (.desktop files) from common locations
- Restore shortcuts from backup
- Preserve shortcut metadata and icon paths
- Support for both system-wide and user-specific shortcuts

## Requirements

- Linux-based operating system
- Python 3.6 or higher
- Basic command line knowledge

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ariesfiredragonfu/desktop-shortcuts.git
cd desktop-shortcuts
```

2. Make the scripts executable:
```bash
chmod +x scripts/*.sh
```

## Usage

### Backing up shortcuts

To backup your desktop shortcuts:
```bash
./scripts/backup-shortcuts.sh
```

The backup will be stored in the `backups` directory with a timestamp.

### Restoring shortcuts

To restore your shortcuts from the most recent backup:
```bash
./scripts/restore-shortcuts.sh
```

To restore from a specific backup:
```bash
./scripts/restore-shortcuts.sh [backup-file]
```

### Restoring the Howell Forge website template

This repository also includes a website restore script used by
`howell-forge-restore.desktop`.

Restore into the project root (creates/updates `index.html`):
```bash
./scripts/restore-website.sh
```

Restore into a custom directory:
```bash
./scripts/restore-website.sh /path/to/target/site
```

If an `index.html` already exists in the target directory, the script creates
an `index.html.backup.<timestamp>` file before restoring.

## Backup Locations

The tool will backup shortcuts from:
- `~/.local/share/applications/` (User-specific shortcuts)
- `/usr/share/applications/` (System-wide shortcuts)
- `~/Desktop/` (Desktop-specific shortcuts)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 