import re
from pathlib import Path

from src.retrieval.policy_contracts import PolicyDocument
from src.retrieval.policy_loader import (
    PolicyDocumentLoadError,
    load_policy_document,
    load_policy_manifest,
)


class PolicyCorpusValidationError(ValueError):
    """Raised when one or more corpus-level validation checks fail."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        message = "Policy corpus validation failed:\n- " + "\n- ".join(errors)
        super().__init__(message)


POLICY_REFERENCE_PATTERN = re.compile(r"\bSYN-POL-\d{3}\b")


def extract_policy_references(body: str) -> set[str]:
    """Return unique policy document IDs referenced in Markdown content."""

    return set(POLICY_REFERENCE_PATTERN.findall(body))


def validate_policy_corpus(
    policy_directory: str | Path,
) -> list[PolicyDocument]:
    """Validate every policy and its agreement with the manifest."""

    directory = Path(policy_directory)
    manifest_path = directory / "manifest.json"

    try:
        manifest = load_policy_manifest(manifest_path)
    except (OSError, PolicyDocumentLoadError) as error:
        raise PolicyCorpusValidationError([str(error)]) from error

    errors: list[str] = []
    documents: list[PolicyDocument] = []
    manifest_paths = {entry.path for entry in manifest.documents}

    manifest_document_ids = {entry.document_id for entry in manifest.documents}

    for entry in manifest.documents:
        document_path = directory / entry.path

        if not document_path.is_file():
            errors.append(f"{entry.path}: file listed in manifest does not exist")
            continue

        try:
            document = load_policy_document(document_path)
        except (OSError, PolicyDocumentLoadError) as error:
            errors.append(str(error))
            continue

        metadata = document.metadata

        expected_values = {
            "document_id": entry.document_id,
            "category": entry.category,
            "component": entry.component,
            "market": manifest.market,
            "classification": manifest.classification,
        }

        for field_name, expected_value in expected_values.items():
            actual_value = getattr(metadata, field_name)

            if actual_value != expected_value:
                errors.append(
                    f"{entry.path}: {field_name} is {actual_value!r}; expected {expected_value!r}"
                )

        expected_source_uri = (
            f"s3://agentic-ai-reference-architecture-exercise/policies/{entry.path}"
        )

        if metadata.source_uri != expected_source_uri:
            errors.append(
                f"{entry.path}: source_uri is {metadata.source_uri!r}; "
                f"expected {expected_source_uri!r}"
            )

        unknown_references = extract_policy_references(document.body) - manifest_document_ids

        for reference in sorted(unknown_references):
            errors.append(f"{entry.path}: references unknown policy {reference}")

        documents.append(document)

    actual_policy_paths = {path.name for path in directory.glob("*.md") if path.name != "README.md"}

    for unlisted_path in sorted(actual_policy_paths - manifest_paths):
        errors.append(f"{unlisted_path}: policy file is not listed in manifest.json")

    if errors:
        raise PolicyCorpusValidationError(errors)

    return documents
