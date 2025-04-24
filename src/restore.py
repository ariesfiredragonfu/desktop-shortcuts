#!/usr/bin/env python3

import os
import shutil
import json
import logging
from pathlib import Path
import sys

class ShortcutRestore:
    def __init__(self):
        self.backup_dir = Path.home() / 'desktop-shortcuts/backups'
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def get_latest_backup(self):
        """Find the most recent backup directory."""
        try:
            backups = [d for d in self.backup_dir.iterdir() if d.is_dir() and d.name.startswith('backup_')]
            if not backups:
                raise ValueError("No backups found")
            return max(backups, key=lambda x: x.stat().st_mtime)
        except Exception as e:
            self.logger.error(f"Error finding latest backup: {str(e)}")
            raise

    def restore_shortcuts(self, backup_path):
        """Restore shortcuts from the specified backup."""
        try:
            info_file = backup_path / 'backup_info.json'
            if not info_file.exists():
                raise ValueError(f"Backup info file not found in {backup_path}")

            with open(info_file, 'r') as f:
                backup_info = json.load(f)

            for location, details in backup_info['locations'].items():
                location_path = Path(location)
                backup_path = Path(details['backup_path'])

                if not backup_path.exists():
                    self.logger.warning(f"Backup path {backup_path} does not exist, skipping")
                    continue

                # Create destination directory if it doesn't exist
                location_path.mkdir(parents=True, exist_ok=True)

                # Restore files
                for file in backup_path.glob('*.desktop'):
                    try:
                        dest_file = location_path / file.name
                        shutil.copy2(file, dest_file)
                        self.logger.info(f"Restored {file.name} to {location_path}")
                    except Exception as e:
                        self.logger.error(f"Error restoring {file}: {str(e)}")

            self.logger.info("Restore completed successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error during restore: {str(e)}")
            return False

def main():
    restore = ShortcutRestore()
    
    try:
        if len(sys.argv) > 1:
            # Use specified backup path
            backup_path = Path(sys.argv[1])
            if not backup_path.is_absolute():
                backup_path = restore.backup_dir / backup_path
        else:
            # Use latest backup
            backup_path = restore.get_latest_backup()

        if not backup_path.exists():
            raise ValueError(f"Backup path {backup_path} does not exist")

        restore.restore_shortcuts(backup_path)

    except Exception as e:
        logging.error(f"Restore failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 