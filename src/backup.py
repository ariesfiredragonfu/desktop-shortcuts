#!/usr/bin/env python3

import os
import shutil
import datetime
import logging
from pathlib import Path
import json

class ShortcutBackup:
    def __init__(self):
        self.backup_locations = [
            Path.home() / '.local/share/applications',
            Path('/usr/share/applications'),
            Path.home() / 'Desktop'
        ]
        
        self.backup_dir = Path.home() / 'desktop-shortcuts/backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def create_backup_name(self):
        """Create a unique backup directory name with timestamp."""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        return self.backup_dir / f'backup_{timestamp}'

    def copy_shortcuts(self, source_dir, dest_dir):
        """Copy .desktop files from source to destination directory."""
        try:
            if not source_dir.exists():
                self.logger.warning(f"Source directory {source_dir} does not exist")
                return []

            copied_files = []
            for file in source_dir.glob('*.desktop'):
                try:
                    shutil.copy2(file, dest_dir)
                    copied_files.append(str(file))
                    self.logger.info(f"Copied {file.name}")
                except Exception as e:
                    self.logger.error(f"Error copying {file}: {str(e)}")

            return copied_files

        except Exception as e:
            self.logger.error(f"Error accessing {source_dir}: {str(e)}")
            return []

    def create_backup(self):
        """Create a complete backup of all desktop shortcuts."""
        backup_path = self.create_backup_name()
        backup_path.mkdir(parents=True, exist_ok=True)

        backup_info = {
            'timestamp': datetime.datetime.now().isoformat(),
            'locations': {},
        }

        for location in self.backup_locations:
            location_name = location.name
            backup_subdir = backup_path / location_name
            backup_subdir.mkdir(parents=True, exist_ok=True)

            copied_files = self.copy_shortcuts(location, backup_subdir)
            backup_info['locations'][str(location)] = {
                'files': copied_files,
                'backup_path': str(backup_subdir)
            }

        # Save backup metadata
        with open(backup_path / 'backup_info.json', 'w') as f:
            json.dump(backup_info, f, indent=4)

        self.logger.info(f"Backup completed successfully at {backup_path}")
        return backup_path

def main():
    backup = ShortcutBackup()
    backup.create_backup()

if __name__ == '__main__':
    main() 