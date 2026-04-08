# python-style-security-linter

This is a lightweight Python command-line linter for style, syntax and security checks using both line-based and AST-based analysis.


## Project goals:

This project was created to practice:

- Python CLI development using argparse
- File and directory processing
- Line-based and AST-based static analysis
- Modular architecture with separate lint rules and data models
- Structured output formatting (text and json)
- Use of dataclasses for structured issue reporting
- Error handling for invalid or unreadable files


## Features:

- Lint single Python files or scan directories recursively
- Detect style issues using line-based checks
- Detect syntax errors using Python AST parsing
- Detect basic security risks using AST-based static analysis
- Output results in text or json format
- Save reports to a file with optional overwrite support


## Project structure:

```text
linter.py      # CLI entry point, file scanning, report saving
rules.py       # Style, syntax and security lint rules implementation
models.py      # Dataclasses for lint issues and per-file results
formatters.py  # Text and json output formatting
test_files     # Example files for manual testing
```

## Implemented checks:

L001 - Line exceeds maximum recommended length (79 characters default)
L002 - Trailing whitespace
L003 - Missing newline at the end of the file
L004 - Multiple consecutive blank lines (default 3+)

P001 - Syntax error detected during AST parsing

S001 - Use of eval()
S002 - Use of exec()
S003 - Use of os.system()
S004 - Use of subprocess calls with shell=True


## Requirements:

Python 3.x

No external dependencies required at this stage.


## Installation and usage:

1. Clone the repository
2. Run the linter:
```text
python linter.py <path>
```
where <path> can be:

- A single Python file
- Multiple files
- One or more directories


### Example input:

Lint a file:
```text
python linter.py example.py
```
Lint multiple files or directories:
```text
python linter.py file1.py file2.py test/
```
Output JSON:
```text
python linter.py test/ --format json
```
Save report to a file:
```text
python linter.py test/ --output report.txt
```
Overwrite an existing file:
```text
python linter.py test/ --output report.txt --overwrite
```
### Example output:

```text
File 1:
C:\linter\test_files\style_issues_example.py
============================================
L002 Line 2, Column 18: Trailing whitespace
L002 Line 3, Column 14: Trailing whitespace
L002 Line 5, Column 4: Trailing whitespace
L004 Line 6, Column 1: Too many consecutive blank lines (3 > 2)
L002 Line 6, Column 4: Trailing whitespace
L004 Line 7, Column 1: Too many consecutive blank lines (4 > 2)
L004 Line 8, Column 1: Too many consecutive blank lines (5 > 2)
L001 Line 10, Column 80: Line too long (111 > 79)
L003 Line 10, Column 112: Missing newline at the end of the file
```


## Possible future improvements:

- Add automated tests with pytest
- Add configurable rule settings
- Support enabling/disabling rules
- Return non-zero exit codes
- Add more lint and security rules
