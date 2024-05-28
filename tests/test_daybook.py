import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
import shutil
import datetime

from src.daybook.daybook import CryptoManager, DaybookManager


class TestDaybook(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.daybook_dir = Path(self.test_dir)
        self.template_file = self.daybook_dir / 'templates/template.md'
        self.toc_file = self.daybook_dir / 'table_of_contents.md'
        self.today = datetime.date.today()
        self.year_month_dir = self.daybook_dir / f'{self.today.year}/{self.today.month:02d}'
        self.today_file = self.year_month_dir / f'{self.today}.md'
        self.date_str = self.today_file.stem

        # Create test template file
        self.template_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.template_file, 'w') as f:
            f.write("# Journal Entry for {{date}}\n\n## Title: {{title}}\n\n## Highlights\n- \n\n## Notes\n- ")

        # Initialize CryptoManager and DaybookManager
        self.crypto_manager = CryptoManager(key_file=self.daybook_dir / 'secret.key')
        self.daybook_manager = DaybookManager(daybook_dir=self.daybook_dir, template_file=self.template_file, toc_file=self.toc_file, crypto_manager=self.crypto_manager)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_today_file(self):
        expected_today_file, expected_year_month_dir = self.daybook_manager.get_today_file()
        self.assertEqual(expected_today_file, self.today_file)
        self.assertEqual(expected_year_month_dir, self.year_month_dir)

    def test_create_today_file(self):
        self.daybook_manager.create_today_file("# Journal Entry for {{date}}\n\n## Title: {{title}}\n\n## Highlights\n- \n\n## Notes\n- ", self.today_file, self.date_str)
        self.assertTrue(self.today_file.exists())
        with open(self.today_file, 'r') as f:
            content = f.read()
        self.assertIn("# Journal Entry for", content)

    def test_update_table_of_contents(self):
        self.year_month_dir.mkdir(parents=True, exist_ok=True)
        self.today_file.touch()  # Create the file to avoid file not found error
        self.daybook_manager.update_table_of_contents(self.today_file, self.date_str, "Test Title")
        self.assertTrue(self.toc_file.exists())
        with open(self.toc_file, 'r') as f:
            content = f.read()
        expected_entry = f'- [{self.date_str}]({self.year_month_dir.relative_to(self.daybook_dir)}/{self.today_file.name}) - Test Title\n'
        self.assertIn(expected_entry, content)

    def test_directory_creation(self):
        # Ensure the directory does not exist before running the process_daybook_entry function
        self.assertFalse(self.year_month_dir.exists())

        # Run the process_daybook_entry function with the test directory
        self.daybook_manager.process_daybook_entry()

        # Check if the year/month directory was created
        self.assertTrue(self.year_month_dir.exists())

    def test_table_of_contents_generation(self):
        # Run the process_daybook_entry function with the test directory
        self.daybook_manager.process_daybook_entry()

        # Check if the table of contents was updated correctly
        self.assertTrue(self.toc_file.exists())
        with open(self.toc_file, 'r') as f:
            content = f.read()
        expected_entry = f'- [{self.date_str}]({self.year_month_dir.relative_to(self.daybook_dir)}/{self.today_file.name})\n'
        self.assertIn(expected_entry, content)

    def test_encryption_and_decryption(self):
        # Ensure directory exists before creating the file
        self.year_month_dir.mkdir(parents=True, exist_ok=True)

        # Create and encrypt a test file
        test_content = "This is a test."
        with open(self.today_file, 'w') as f:
            f.write(test_content)
        self.crypto_manager.encrypt_file(self.today_file)
        self.assertTrue(self.today_file.exists())

        encrypted_file = self.today_file

        # Decrypt the test file
        self.crypto_manager.decrypt_file(encrypted_file)
        self.assertTrue(self.today_file.exists())
        with open(self.today_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, test_content)

    @patch('os.system')
    def test_open_entry_in_editor(self, mock_system):
        # Ensure directory exists before creating the file
        self.year_month_dir.mkdir(parents=True, exist_ok=True)

        # Create a test file
        self.daybook_manager.create_today_file("# Journal Entry for {{date}}\n\n## Title: {{title}}", self.today_file, self.date_str)
        self.crypto_manager.encrypt_file(self.today_file)
        encrypted_file = self.today_file

        # Decrypt and open the test file
        self.crypto_manager.decrypt_file(encrypted_file)
        with open(self.today_file, 'r') as f:
            content = f.read()
        self.assertIn("# Journal Entry for", content)

        # Ensure Vim was called
        self.daybook_manager.open_entry_in_editor(self.today_file)
        mock_system.assert_called_with(f'vim {self.today_file}')


if __name__ == '__main__':
    unittest.main()
