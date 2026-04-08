import json

# Output

def format_issue(issue):
	return f"{issue.code} Line {issue.line}, Column {issue.column}: {issue.message}"

def format_report_text(results):
	output_lines = []

	for index, result in enumerate(results, start=1):
		output_lines.append(f"File {index}:")
		output_lines.append(result.file_path)
		output_lines.append("=" * len(result.file_path))

		if result.error:
			output_lines.append(f"Error: {result.error}")

		elif result.issues:
			for issue in result.issues:
				output_lines.append(format_issue(issue))

		else:
			output_lines.append("No lint issues found.")

		output_lines.append("")

	return "\n".join(output_lines)

# Output json

# Convert data to dictionary format for json conversion

# Single issue
def issue_to_dict(issue):
	return {
		"line": issue.line,
		"column": issue.column,
		"code": issue.code,
		"message": issue.message,
	}

# Single file result
def result_to_dict(result):
	return {
		"file_path": result.file_path,
		"issues": [issue_to_dict(issue) for issue in result.issues],
		"error": result.error,
	}

# All scanned files
def build_json_data(results):
	return [result_to_dict(result) for result in results]

# Finalize output

def build_output(results, output_format):
	if output_format == "json":
		json_data = build_json_data(results)
		return json.dumps(json_data, indent=4)

	return format_report_text(results)
