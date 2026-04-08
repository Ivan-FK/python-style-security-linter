from dataclasses import dataclass

@dataclass
class LintIssue:
	line: int
	column: int
	code: str
	message: str

@dataclass
class FileLintResult:
	file_path: str
	issues: list[LintIssue]
	error: str | None = None
