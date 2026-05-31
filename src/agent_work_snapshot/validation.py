from __future__ import annotations

import json
import re
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

SECRET_KEY_PARTS = (
    "secret",
    "token",
    "password",
    "passwd",
    "credential",
    "private_key",
    "api_key",
    "access_key",
    "client_secret",
    "cookie",
    "session",
)

ABSOLUTE_LOCAL_PATH_PATTERNS = (
    re.compile(r"^/Users/"),
    re.compile(r"^/home/"),
    re.compile(r"^file:///Users/"),
    re.compile(r"^[A-Za-z]:\\Users\\"),
)


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return not self.errors


def load_schema() -> dict[str, Any]:
    schema_path = files("agent_work_snapshot").joinpath("schema.json")
    return json.loads(schema_path.read_text(encoding="utf-8"))


def _format_json_path(parts: Iterable[object]) -> str:
    path = "$"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path


def _find_secret_like_keys(value: Any, path: tuple[object, ...] = ()) -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower()
            compact = re.sub(r"[^a-z0-9]", "", normalized)
            if any(candidate in normalized or candidate.replace("_", "") in compact for candidate in SECRET_KEY_PARTS):
                findings.append(f"{_format_json_path((*path, key))}: secret-like key is forbidden")
            findings.extend(_find_secret_like_keys(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_find_secret_like_keys(child, (*path, index)))
    return findings


def _find_absolute_local_paths(value: Any, path: tuple[object, ...] = ()) -> list[str]:
    findings: list[str] = []
    if isinstance(value, str):
        if any(pattern.search(value) for pattern in ABSOLUTE_LOCAL_PATH_PATTERNS):
            findings.append(
                f"{_format_json_path(path)}: absolute local path detected; use a relative path or artifact reference"
            )
    elif isinstance(value, dict):
        for key, child in value.items():
            findings.extend(_find_absolute_local_paths(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_find_absolute_local_paths(child, (*path, index)))
    return findings


def _progress_errors(snapshot: dict[str, Any]) -> list[str]:
    progress = snapshot.get("progress")
    if not isinstance(progress, dict):
        return []
    total = progress.get("total")
    completed = progress.get("completed")
    blocked = progress.get("blocked")
    if not all(isinstance(value, int) and not isinstance(value, bool) for value in (total, completed, blocked)):
        return []

    errors: list[str] = []
    if completed > total:
        errors.append("$.progress.completed: must be less than or equal to total")
    if blocked > total:
        errors.append("$.progress.blocked: must be less than or equal to total")
    if completed + blocked > total:
        errors.append("$.progress: completed + blocked must be less than or equal to total")
    return errors


def validate_snapshot(snapshot: Any, *, strict_paths: bool = False) -> ValidationResult:
    schema = load_schema()
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    errors = [
        f"{_format_json_path(error.absolute_path)}: {error.message}"
        for error in sorted(validator.iter_errors(snapshot), key=lambda item: list(item.absolute_path))
    ]
    errors.extend(_find_secret_like_keys(snapshot))
    if isinstance(snapshot, dict):
        errors.extend(_progress_errors(snapshot))

    path_findings = _find_absolute_local_paths(snapshot)
    if strict_paths:
        errors.extend(path_findings)
        warnings: list[str] = []
    else:
        warnings = path_findings

    return ValidationResult(tuple(errors), tuple(warnings))


def validate_file(path: Path, *, strict_paths: bool = False) -> ValidationResult:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    return validate_snapshot(snapshot, strict_paths=strict_paths)
