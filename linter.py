import argparse
import os

from models import FileLintResult
from rules import run_checks
from formatters import build_output

# Configuration

DEFAULT_EXTENSIONS = (".py",)

def read_file_lines(file_path):
	with open(file_path, "r", encoding="utf-8") as file:
		return file.readlines()

# Files input

# Error reading file
def lint_file_error_result(file_path, error_message):
	return FileLintResult(
		file_path=file_path,
		issues=[],
		error=error_message,
	)

# Lint single file
def lint_file(file_path):
	try:
		lines = read_file_lines(file_path)
		issues = run_checks(lines)
		return FileLintResult(file_path=file_path, issues=issues)

	except FileNotFoundError:
		return lint_file_error_result(file_path, "File not found.")

	except IsADirectoryError:
		return lint_file_error_result(file_path, "Target path is a directory, not a file.")

	except PermissionError:
		return lint_file_error_result(file_path, "Permission denied.")

	except UnicodeDecodeError:
		return lint_file_error_result(file_path, "File is not a valid UTF-8 text and cannot be linted.")

	except OSError as error:
		return lint_file_error_result(file_path, f"Could not read file: {error}")

def lint_paths(file_paths):
	results = []

	for file_path in file_paths:
		result = lint_file(file_path)
		results.append(result)

	return results

# Collect files from directory

def collect_files_from_directory(directory_path):
	collected_files = []

	for root, _, files in os.walk(directory_path):
		for file_name in files:
			if file_name.endswith(DEFAULT_EXTENSIONS):
				full_path = os.path.abspath(os.path.join(root, file_name))
				collected_files.append(full_path)

	collected_files.sort()
	return collected_files

def normalize_path(file_path):
	return os.path.normcase(os.path.abspath(file_path))

def expand_input_paths(input_paths):
	expanded_file_paths = []
	seen_files = set()
	path_errors = []

	def add_file(file_path):
		normalized_path = normalize_path(file_path)

		if normalized_path not in seen_files:
			expanded_file_paths.append(os.path.abspath(file_path))
			seen_files.add(normalized_path)

	for path in input_paths:
		if os.path.isfile(path):
			add_file(path)

		elif os.path.isdir(path):
			directory_files = collect_files_from_directory(path)

			if directory_files:
				for file_path in directory_files:
					add_file(file_path)

			else:
				path_errors.append(
					lint_file_error_result(path, "Directory contains no Python files.")
				)

		else:
			path_errors.append(
				lint_file_error_result(path, "Path not found.")
			)

	return expanded_file_paths, path_errors


# Save report to a file

def save_report(output_path, report_text, overwrite=False):
	mode = "w" if overwrite else "x"

	try:
		with open(output_path, mode, encoding="utf-8") as file:
			file.write(report_text)
			print(f"Report saved to {output_path}.")
		return True

	except FileExistsError:
		print(
			f"Error: '{output_path}' already exists. "
			"Report not saved. You can use '--overwrite' to overwrite")
		return False

	except OSError as error:
		print(f"Error: Could not save report to '{output_path}': {error}")
		return False

# CLI parser

def parse_args():
	parser = argparse.ArgumentParser(
		description="This is a simple Python linter tool for line-based style checks."
	)

	parser.add_argument(
		"file_paths",
		nargs="+",
		help="One or more files or directories to scan for lint.",
	)

	parser.add_argument(
		"--format",
		choices=["text", "json"],
		default="text",
		help="Output format (default: text).",
	)

	parser.add_argument(
		"--output",
		help="Save the report to a file instead of printing it to terminal."
	)

	parser.add_argument(
		"--overwrite",
		action = "store_true",
		help="Overwrite a file with the same name if it already exists."
	)

	return parser.parse_args()

# Main

def main():
	args = parse_args()

	expanded_file_paths, path_errors = expand_input_paths(args.file_paths)
	results = path_errors + lint_paths(expanded_file_paths)
	output = build_output(results, args.format)

	if args.output:
		save_success = save_report(args.output, output, args.overwrite)

		if not save_success:
			print(output)

	else:
		print(output)

if __name__ == "__main__":
	main()
