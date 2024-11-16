# Changelog Manager

A Python script to manage version updates and changelog entries in a standardized way. This tool helps maintain consistent changelog formatting while automating version increments and reference management.

## AI Assistance Notice

This project was developed with the assistance of Claude (Anthropic's AI). The AI helped with:
- Initial script structure and logic
- Error handling and edge cases
- Documentation and examples
- Best practices implementation

While the core requirements and testing were human-driven, the AI contributed significantly to the code implementation and documentation.

## Features

- Interactive CLI interface
- Automatic version increment for hotfixes
- Git branch detection for ticket IDs
- Standardized changelog entry formatting
- Automatic version reference management
- Duplicate removal and version sorting
- Repository URL agnostic

## Demo
![Demo](https://github.com/user-attachments/assets/eec36f0d-027f-4833-9501-044a0a1d26a9)

**You can see a complete example of the changes this script produces in [Pull Request](https://github.com/antonioeloi/changelog_updater/pull/1) where I run the demo.**

## Prerequisites

- Python 3.x
- `inquirer` package

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd changelog-manager
```

2. Install required packages:

```bash
pip install inquirer
```

3. Make the script executable:

```bash
chmod +x script.py
```

## Usage

### File Structure
Your project should have:
- A `VERSION` file containing the current version number (e.g., "7.1.3.2")
- A `CHANGELOG.md` file following the Keep a Changelog format

### Running the Script

```bash
./script.py
```


### Interactive Prompts

1. The script will detect your current git branch and extract a ticket ID
2. Choose between:
   - Hotfix
   - Nope (cancels operation)
3. If Hotfix selected, choose the type of change:
   - Change
   - Feature
   - Fix
   - Remove
4. Enter your changelog message

### What the Script Does

1. Increments the last number in your VERSION file
2. Adds a new changelog entry with:
   - New version number
   - Today's date
   - Selected change type
   - Your message with ticket ID link
3. Updates version references at the bottom of the changelog
4. Sorts and removes duplicate references

## Configuration

The script uses these constants that you can modify:

```python
TICKET_PREFIX = "RAILS-" # Your ticket prefix
DEFAULT_TICKET = f"{TICKET_PREFIX}XXXX" # Default ticket format
CLICKUP_URL = "https://app.clickup.com/t/2477891/" # Your ticket system URL
```

## Contributing

Feel free to submit issues and enhancement requests!
Feel also free to email me at contact@antonioeloi.tech for questions or suggestions.

## License

MIT License

Copyright (c) 2024 António Eloi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
