# 📒 Daybook

A command-line tool for managing daily journal entries with encryption. This tool allows you to create, edit, and encrypt your journal entries, ensuring your personal notes remain secure.

## Features ✨

- 📝 Create new journal entries based on a template
- ✏️ Open and edit existing journal entries
- 🔒 Encrypt and decrypt journal entries using the `cryptography` library
- 📚 Automatically update a table of contents with each entry
- 🏷️ Optional titles for entries

## Installation 🛠️

To install Daybook, follow these steps:

### Prerequisites

- 🐍 Python 3.6+
- `pip` (Python package installer)
- `pipx` (Python application installer)

### Using `pipx`

1. **Install `pipx` (if not already installed):**
    ```bash
    sudo pacman -S python-pipx
    ```

2. **Install Daybook using `pipx`:**
    ```bash
    pipx install git+https://github.com/Stephanie-Burns/daybook.git
    ```

### Cloning and Installing Separately

If you prefer to clone the repository and install it manually:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Stephanie-Burns/daybook.git
    cd daybook
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

3. **Activate the virtual environment:**

    - On **Linux/macOS**:
        ```bash
        source .venv/bin/activate
        ```

    - On **Windows**:
        ```bash
        .\.venv\Scripts\activate
        ```

4. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Install the package in editable mode:**
    ```bash
    pip install -e .
    ```

### Uninstalling

If you installed Daybook using `pipx` and want to uninstall it:

1. **Uninstall using `pipx`:**
    ```bash
    pipx uninstall daybook
    ```
## Usage 🚀
### Create or Open Today's Journal Entry

To create or open a journal entry for today, run:
```bash
daybook
```

### Open a Specific Date's Journal Entry
To open a journal entry for a specific date, use the --date option:

```bash
daybook --date YYYY-MM-DD
```

## Configuration ⚙️
### Directory Structure
By default, the journal entries are stored in ~/daybook-entries. You can change this by setting the JOURNAL_DIR environment variable.

Files
- **Template File**: ~/daybook-entries/templates/template.md
- **Table of Contents**: ~/daybook-entries/table_of_contents.md
- **Encryption Key**: ~/daybook-entries/secret.key

### Template File
The template file should contain placeholders for the date and title:

```markdown
# Journal Entry for {{date}}

## Title: {{title}}

## Highlights
- 

## Notes
- 
```

### Example Template 📝
Here is an example template that you can use:

```markdown
# Developer's Journal

## Date: {{date}}
## Title: {{title}}

### Emotional Check-in
- How am I feeling?
  -

### Daily Goal
- What do I want to achieve today?
  -

### Today's Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Problems and Ambiguities
- Problems and uncertainties encountered:
  -
- Hypotheses and approaches:
  -

### Solutions and Learnings
- Solutions found:
  -
- Key learnings:
  -

### Ideas and Todos
- Ideas and tasks for later:
  -

### End of Day Reflection
- Did I achieve my goal?
  -
- What went well?
  -
- What was challenging?
  -
- What will I do differently tomorrow?
  -

### Review and Learnings
- Review of learnings and insights:
  -
```

## Encryption Key 🔑

The encryption key is crucial for securing your journal entries. It is stored in `~/daybook/secret.key` by default.

**Important: Losing the encryption key will result in losing access to all your encrypted journal entries.** Ensure you back up this key securely.

### Auto-Generation of the Encryption Key

If the encryption key does not already exist, it will be automatically generated and saved to the specified key file when you first run the Daybook application. This key is essential for both encrypting and decrypting your journal entries, so treat it with care.

### Environment Variable

The `DAYBOOK_DIR` environment variable can be set to change the default directory where the daybook entries and the encryption key are stored. By default, it is set to `~/daybook`:

```python
DAYBOOK_DIR = Path(os.getenv('DAYBOOK_DIR', Path.home() / 'daybook'))
```

### Default Editor
By default, Daybook uses vim to open and edit journal entries. If you prefer to use a different editor, you can set the EDITOR environment variable to your preferred text editor. For example, to use nano:

```bash
export EDITOR=nano
```

Then, when you run Daybook, it will use nano instead of vim.

## Running Tests 🧪
To run the tests, use the following command:

```shell
python -m unittest discover
```

## Conclusion 🎉

Daybook is designed to help you manage your daily journal entries securely and efficiently. By using encryption, it ensures that your personal notes remain private. Whether you choose to install it using `pipx` for a globally accessible command or prefer to manage your environment manually, Daybook offers flexibility and ease of use. We hope you find it valuable for your journaling needs. If you encounter any issues or have suggestions for improvement, feel free to contribute or open an issue on our GitHub repository.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
