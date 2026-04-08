import ast

from models import LintIssue

# Lint rule 1: Check if the line is too long

def check_line_length(lines, max_length=79):
	issues = []

	for line_number, line in enumerate(lines, start=1):
		visible_line = line.rstrip("\n")

		if len(visible_line) > max_length:
			issue = LintIssue(
				line=line_number,
				column=max_length + 1,
				code="L001",
				message=f"Line too long ({len(visible_line)} > {max_length})"
			)
			issues.append(issue)

	return issues

# Lint rule 2: Check line for trailing whitespace characters

def check_trailing_whitespace(lines):
	issues = []

	for line_number, line in enumerate(lines, start=1):
		visible_line = line.rstrip("\n")

		if visible_line.endswith(" ") or visible_line.endswith("\t"):
			issue = LintIssue(
				line=line_number,
				column=len(visible_line),
				code="L002",
				message="Trailing whitespace"
			)
			issues.append(issue)

	return issues

# Lint rule 3: Check for missing newline at the end of the file

def check_missing_final_newline(lines):
	issues = []

	if not lines:
		return issues

	last_line = lines[-1]

	if not last_line.endswith("\n"):
		issue = LintIssue(
			line=len(lines),
			column=len(last_line) + 1,
			code="L003",
			message="Missing newline at the end of the file"
		)
		issues.append(issue)

	return issues

# Lint rule 4: Check for 3+ consecutive blank lines

def check_consecutive_blank_lines(lines, max_blank_lines=2):
	issues = []

	blank_streak = 0

	for line_number, line in enumerate(lines, start=1):
		visible_line = line.rstrip("\n")

		if visible_line.strip() == "":
			blank_streak += 1

			if blank_streak > max_blank_lines:
				issue = LintIssue(
					line=line_number,
					column=1,
					code="L004",
					message=f"Too many consecutive blank lines ({blank_streak} > {max_blank_lines})"
				)
				issues.append(issue)
		else:
			blank_streak = 0

	return issues

# Security rule 1: Check eval() usage

def check_eval_usage(tree):
	issues = []

	for node in ast.walk(tree):
		if isinstance(node, ast.Call):
			if isinstance(node.func, ast.Name) and node.func.id == "eval":
				issue = LintIssue(
					line=node.lineno,
					column=node.col_offset + 1,
					code="S001",
					message="Use of eval() detected (potential code injection risk)"
				)
				issues.append(issue)

	return issues

# Security rule 2: Check exec() usage

def check_exec_usage(tree):
	issues = []

	for node in ast.walk(tree):
		if isinstance(node, ast.Call):
			if isinstance(node.func, ast.Name) and node.func.id =="exec":
				issue = LintIssue(
					line=node.lineno,
					column=node.col_offset + 1,
					code="S002",
					message="Use of exec() detected (potential arbitrary code execution risk)"
				)
				issues.append(issue)

	return issues

# Security rule 3: Check os.system() usage

def check_os_system_usage(tree):
	issues = []

	for node in ast.walk(tree):
		if isinstance(node, ast.Call):
			if isinstance(node.func, ast.Attribute):
				if isinstance(node.func.value, ast.Name):
					if node.func.value.id == "os" and node.func.attr == "system":
						issue = LintIssue(
							line=node.lineno,
							column=node.col_offset + 1,
							code="S003",
							message="Use of os.system() detected (potential command injection risk)"
						)
						issues.append(issue)

	return(issues)

# Security rule 4: Check subprocess calls with shell=True

def check_subprocess_shell_true(tree):
	issues = []

	subprocess_functions = {"run", "call", "Popen", "check_call", "check_output"}

	for node in ast.walk(tree):
		if isinstance(node, ast.Call):
			if isinstance(node.func, ast.Attribute):
				if isinstance(node.func.value, ast.Name):
					if node.func.value.id == "subprocess" and node.func.attr in subprocess_functions:
						for keyword in node.keywords:
							if keyword.arg == "shell":
								if isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
									issue = LintIssue(
										line=node.lineno,
										column=node.col_offset + 1,
										code="S004",
										message="Subprocess call with shell=True detected (potential command injection risk)"
									)
									issues.append(issue)

	return(issues)

# Run checks

# Line checks

def run_line_checks(lines):
	all_issues = []
	checks=[
		check_line_length,
		check_trailing_whitespace,
		check_missing_final_newline,
		check_consecutive_blank_lines
	]

	for check in checks:
		issues = check(lines)
		all_issues.extend(issues)

	return all_issues

# AST checks

# Convert file lines into a single source code string for AST parsing

def build_source_code(lines):
	return "".join(lines)

def parse_source_to_ast(lines):
	source_code = build_source_code(lines)

	try:
		tree = ast.parse(source_code)
		return tree, []

	except SyntaxError as error:
		line_number = error.lineno or 1
		column_number = error.offset or 1

		parse_issue = LintIssue(
			line=line_number,
			column=column_number,
			code="P001",
			message=f"Syntax error: {error.msg}"
		)

		return None, [parse_issue]

def run_ast_checks(tree):
	all_issues = []
	checks = [
		check_eval_usage,
		check_exec_usage,
		check_os_system_usage,
		check_subprocess_shell_true,
	]

	for check in checks:
		issues = check(tree)
		all_issues.extend(issues)

	return all_issues

# Run all checks

def run_checks(lines):
	all_issues = []

	line_issues = run_line_checks(lines)
	all_issues.extend(line_issues)

	tree, parse_issues = parse_source_to_ast(lines)
	all_issues.extend(parse_issues)

	if tree is not None:
		ast_issues = run_ast_checks(tree)
		all_issues.extend(ast_issues)

	all_issues.sort(key=lambda issue: (issue.line, issue.column, issue.code))
	return all_issues
