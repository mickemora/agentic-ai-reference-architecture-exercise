import re
from pathlib import Path

import yaml
from pydantic import ValidationError

from src.retrieval.policy_contracts import (
    PolicyDocument,
    PolicyManifest,
    PolicyMetadata,
)


class PolicyDocumentLoadError(ValueError):
    """Raised when a policy document cannot be parsed or validated."""


def validate_policy_structure(
    body: str,
    metadata: PolicyMetadata,
    source: str = "<memory>",
) -> None:
    """Validate the required Markdown structure of a policy document."""

    content_lines = [line.strip() for line in body.splitlines() if line.strip()]

    expected_title = f"# {metadata.title}"
    h1_lines = [line for line in content_lines if line.startswith("# ")]

    if len(h1_lines) != 1:
        raise PolicyDocumentLoadError(f"{source}: policy must contain exactly one H1 title")

    if not content_lines or content_lines[0] != expected_title:
        raise PolicyDocumentLoadError(f"{source}: first content line must be {expected_title!r}")

    if len(content_lines) < 2 or not content_lines[1].startswith("> Synthetic training policy."):
        raise PolicyDocumentLoadError(
            f"{source}: synthetic training policy disclaimer must immediately follow the title"
        )

    section_lines = [line for line in content_lines if line.startswith("## ")]

    if len(section_lines) < 4:
        raise PolicyDocumentLoadError(
            f"{source}: policy must contain at least four numbered sections"
        )

    section_numbers: list[int] = []

    for section_line in section_lines:
        match = re.fullmatch(r"## (\d+)\.0 (.+)", section_line)

        if match is None:
            raise PolicyDocumentLoadError(
                f"{source}: invalid section heading {section_line!r}; "
                "expected format '## N.0 Section title'"
            )

        section_numbers.append(int(match.group(1)))

    expected_numbers = list(range(1, len(section_numbers) + 1))

    if section_numbers != expected_numbers:
        raise PolicyDocumentLoadError(
            f"{source}: section numbers are {section_numbers}; expected {expected_numbers}"
        )


def parse_policy_document(
    text: str,
    source: str = "<memory>",
) -> PolicyDocument:
    """Parse and validate a Markdown policy containing YAML front matter."""

    lines = text.splitlines()

    if not lines or lines[0].strip() != "---":
        raise PolicyDocumentLoadError(
            f"{source}: policy must begin with a YAML front-matter delimiter"
        )

    try:
        closing_index = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as error:
        raise PolicyDocumentLoadError(
            f"{source}: closing YAML front-matter delimiter was not found"
        ) from error

    metadata_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :]).strip()

    if not body:
        raise PolicyDocumentLoadError(f"{source}: policy body must not be empty")

    try:
        metadata_data = yaml.safe_load(metadata_text)
    except yaml.YAMLError as error:
        raise PolicyDocumentLoadError(f"{source}: invalid YAML front matter: {error}") from error

    if not isinstance(metadata_data, dict):
        raise PolicyDocumentLoadError(f"{source}: YAML front matter must contain a mapping")

    try:
        metadata = PolicyMetadata.model_validate(metadata_data)
    except ValidationError as error:
        raise PolicyDocumentLoadError(
            f"{source}: metadata contract validation failed: {error}"
        ) from error

    # return PolicyDocument(metadata=metadata, body=body)
    validate_policy_structure(body, metadata, source)

    return PolicyDocument(metadata=metadata, body=body)


def load_policy_document(path: str | Path) -> PolicyDocument:
    """Read, parse, and validate one policy document."""

    policy_path = Path(path)
    text = policy_path.read_text(encoding="utf-8")

    return parse_policy_document(text, source=str(policy_path))


def load_policy_manifest(path: str | Path) -> PolicyManifest:
    """Read and validate the policy corpus manifest."""

    manifest_path = Path(path)
    text = manifest_path.read_text(encoding="utf-8")

    try:
        return PolicyManifest.model_validate_json(text)
    except ValidationError as error:
        raise PolicyDocumentLoadError(
            f"{manifest_path}: manifest validation failed: {error}"
        ) from error
