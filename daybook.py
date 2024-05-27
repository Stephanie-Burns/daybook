#!/usr/bin/env python3

import os
import sys
import datetime
from pathlib import Path
from cryptography.fernet import Fernet
import argparse
from typing import Optional, Tuple

DAYBOOK_DIR = Path(os.getenv('DAYBOOK_DIR', Path.home() / 'daybook'))
TEMPLATE_FILE = DAYBOOK_DIR / 'templates/template.md'
TOC_FILE = DAYBOOK_DIR / 'table_of_contents.md'
KEY_FILE = DAYBOOK_DIR / 'secret.key'


class CryptoManager:
    def __init__(self, key_file: Path = KEY_FILE):
        self.key_file = key_file

        if not self.key_file.exists():
            self.generate_key()

        self.key = self.load_key()

    def generate_key(self) -> None:
        """Generate a new encryption key and save it to the specified key file."""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as kf:
            kf.write(key)

    def load_key(self) -> bytes:
        """Load the encryption key from the specified key file."""
        with open(self.key_file, 'rb') as kf:
            return kf.read()

    def encrypt_file(self, file_path: Path) -> None:
        """Encrypt the specified file using the provided key."""
        fernet = Fernet(self.key)

        with open(file_path, 'rb') as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

    def decrypt_file(self, file_path: Path) -> None:
        """Decrypt the specified file using the provided key."""
        try:
            fernet = Fernet(self.key)

            with open(file_path, 'rb') as enc_file:
                encrypted = enc_file.read()

            decrypted = fernet.decrypt(encrypted)

            with open(file_path, 'wb') as dec_file:
                dec_file.write(decrypted)

        except Exception as e:
            print(f"Error decrypting file {file_path}: {e}", file=sys.stderr)


class DaybookManager:
    def __init__(self, daybook_dir: Path = DAYBOOK_DIR, template_file: Path = TEMPLATE_FILE, toc_file: Path = TOC_FILE, crypto_manager: Optional[CryptoManager] = None):
        self.daybook_dir = daybook_dir
        self.template_file = template_file
        self.toc_file = toc_file
        self.crypto_manager = crypto_manager if crypto_manager else CryptoManager()

    def get_today_file(self) -> Tuple[Path, Path]:
        """Get the file path and directory for today's daybook entry."""
        today = datetime.date.today()
        year_month_dir = self.daybook_dir / f'{today.year}/{today.month:02d}'
        today_file = year_month_dir / f'{today}.md'

        return today_file, year_month_dir

    @staticmethod
    def get_specific_file(date: datetime.date, daybook_dir: Path = DAYBOOK_DIR) -> Tuple[Path, Path]:
        """Get the file path and directory for a specific date's daybook entry."""
        year_month_dir = daybook_dir / f'{date.year}/{date.month:02d}'
        specific_file = year_month_dir / f'{date}.md'

        return specific_file, year_month_dir

    @staticmethod
    def create_today_file(template: str, today_file: Path, date_str: str) -> None:
        """Create a new daybook entry file for today using the provided template."""
        try:
            content = template.replace('{{date}}', date_str).replace('{{title}}', '')
            today_file.parent.mkdir(parents=True, exist_ok=True)

            with open(today_file, 'w') as f:
                f.write(content)

        except Exception as e:
            print(f"Error creating today's file: {e}", file=sys.stderr)

    def update_table_of_contents(self, today_file: Path, date_str: str, title: Optional[str]) -> None:
        """Update the table of contents with the new daybook entry."""
        try:
            relative_path = today_file.relative_to(self.daybook_dir)
            new_entry = f'- [{date_str}]({relative_path}){" - " + title if title else ""}\n'

            # Create a dictionary to store existing entries
            toc_entries = {}
            if self.toc_file.exists():
                with open(self.toc_file, 'r') as toc:
                    for line in toc:
                        if line.startswith('- ['):
                            entry_date = line.split(']')[0][2:]
                            toc_entries[entry_date] = line

            # Update or add the new entry
            toc_entries[date_str] = new_entry

            # Write updated entries back to the TOC file
            with open(self.toc_file, 'w') as toc:
                for entry in sorted(toc_entries.values()):
                    toc.write(entry)

        except Exception as e:
            print(f"Error updating table of contents: {e}", file=sys.stderr)

    @staticmethod
    def extract_title(file_path: Path) -> Optional[str]:
        """Extract the title from the daybook entry file."""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                if line.startswith('## Title:'):
                    title = line[len('## Title:'):].strip()
                    return title

        except Exception as e:
            print(f"Error extracting title: {e}", file=sys.stderr)

        return None

    def process_daybook_entry(self) -> Path:
        """Process the daybook entry for today, including creating, decrypting, and encrypting the file."""
        try:
            today_file, year_month_dir = self.get_today_file()
            date_str = today_file.stem

            if today_file.exists():
                self.crypto_manager.decrypt_file(today_file)

            year_month_dir.mkdir(parents=True, exist_ok=True)

            if not today_file.exists():
                with open(self.template_file, 'r') as template_file:
                    template = template_file.read()
                self.create_today_file(template, today_file, date_str)

            title = self.extract_title(today_file)
            self.crypto_manager.encrypt_file(today_file)
            self.update_table_of_contents(today_file, date_str, title)

            return today_file

        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)

    def open_entry_in_editor(self, file_path: Path) -> None:
        """Open the daybook entry file in the editor, and handle decryption and encryption."""
        try:
            self.crypto_manager.decrypt_file(file_path)

        except Exception as e:
            print(f"Error decrypting file {file_path}: {e}")

        editor = os.getenv('EDITOR', 'vim')
        os.system(f'{editor} {file_path}')

        title = self.extract_title(file_path)

        try:
            self.crypto_manager.encrypt_file(file_path)

        except Exception as e:
            print(f"Error encrypting file {file_path}: {e}")

        date_str = file_path.stem
        self.update_table_of_contents(file_path, date_str, title)


def main() -> None:
    """Main function to handle command-line arguments and process the daybook entry."""
    parser = argparse.ArgumentParser(description="Daybook Manager")
    parser.add_argument('--date', type=str, help='Date of the daybook entry to read (format: YYYY-MM-DD)')
    args = parser.parse_args()

    daybook_manager = DaybookManager()

    if args.date:
        try:
            date = datetime.datetime.strptime(args.date, '%Y-%m-%d').date()
            specific_file, _ = daybook_manager.get_specific_file(date)
            daybook_manager.open_entry_in_editor(specific_file)

        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")

    else:
        today_file = daybook_manager.process_daybook_entry()
        daybook_manager.open_entry_in_editor(today_file)


if __name__ == '__main__':
    main()
