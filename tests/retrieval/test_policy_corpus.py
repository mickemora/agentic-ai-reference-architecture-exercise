from pathlib import Path
from shutil import copytree

import pytest

from src.retrieval import (
    PolicyCorpusValidationError,
    PolicyDocumentLoadError,
    extract_policy_references,
    parse_policy_document,
    validate_policy_corpus,
)
from src.retrieval.validate_corpus import main as validation_cli_main

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
POLICY_DIRECTORY = REPOSITORY_ROOT / "data" / "policies"


def test_current_policy_corpus_is_valid() -> None:
    documents = validate_policy_corpus(POLICY_DIRECTORY)

    assert len(documents) == 20
    assert documents[0].metadata.document_id == "SYN-POL-001"
    assert documents[-1].metadata.document_id == "SYN-POL-020"


def test_policy_must_begin_with_front_matter() -> None:
    invalid_policy = "# Policy without YAML front matter"

    with pytest.raises(
        PolicyDocumentLoadError,
        match="must begin with a YAML front-matter delimiter",
    ):
        parse_policy_document(invalid_policy)


def test_unknown_metadata_field_is_rejected() -> None:
    policy_path = POLICY_DIRECTORY / "01-basic-warranty-coverage.md"
    policy_text = policy_path.read_text(encoding="utf-8")
    invalid_policy = policy_text.replace(
        "classification: synthetic-public-training",
        ("classification: synthetic-public-training\nunexpected_field: should-not-be-accepted"),
    )

    with pytest.raises(
        PolicyDocumentLoadError,
        match="metadata contract validation failed",
    ):
        parse_policy_document(invalid_policy)


def test_manifest_metadata_mismatch_is_rejected(
    tmp_path: Path,
) -> None:
    temporary_corpus = tmp_path / "policies"
    copytree(POLICY_DIRECTORY, temporary_corpus)

    policy_path = temporary_corpus / "01-basic-warranty-coverage.md"
    policy_text = policy_path.read_text(encoding="utf-8")
    policy_path.write_text(
        policy_text.replace(
            "category: coverage",
            "category: governance",
            1,
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        PolicyCorpusValidationError,
        match="expected 'coverage'",
    ):
        validate_policy_corpus(temporary_corpus)


def test_unlisted_policy_file_is_rejected(
    tmp_path: Path,
) -> None:
    temporary_corpus = tmp_path / "policies"
    copytree(POLICY_DIRECTORY, temporary_corpus)

    source = temporary_corpus / "01-basic-warranty-coverage.md"
    unlisted = temporary_corpus / "99-unlisted-policy.md"
    unlisted.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    with pytest.raises(
        PolicyCorpusValidationError,
        match="not listed in manifest.json",
    ):
        validate_policy_corpus(temporary_corpus)


def test_policy_title_must_match_metadata() -> None:
    policy_path = POLICY_DIRECTORY / "01-basic-warranty-coverage.md"
    policy_text = policy_path.read_text(encoding="utf-8")
    invalid_policy = policy_text.replace(
        "# Basic Warranty Coverage",
        "# Incorrect Policy Title",
        1,
    )

    with pytest.raises(
        PolicyDocumentLoadError,
        match="first content line must be",
    ):
        parse_policy_document(invalid_policy)


def test_policy_must_include_synthetic_disclaimer() -> None:
    policy_path = POLICY_DIRECTORY / "01-basic-warranty-coverage.md"
    policy_text = policy_path.read_text(encoding="utf-8")
    invalid_policy = policy_text.replace(
        "> Synthetic training policy.",
        "> Training document.",
        1,
    )

    with pytest.raises(
        PolicyDocumentLoadError,
        match="synthetic training policy disclaimer",
    ):
        parse_policy_document(invalid_policy)


def test_policy_section_numbers_must_be_sequential() -> None:
    policy_path = POLICY_DIRECTORY / "01-basic-warranty-coverage.md"
    policy_text = policy_path.read_text(encoding="utf-8")
    invalid_policy = policy_text.replace(
        "## 2.0 General eligibility",
        "## 7.0 General eligibility",
        1,
    )

    with pytest.raises(
        PolicyDocumentLoadError,
        match="section numbers are",
    ):
        parse_policy_document(invalid_policy)


def test_policy_references_are_extracted() -> None:
    body = "Review SYN-POL-002 and SYN-POL-006. SYN-POL-002 may appear more than once."

    references = extract_policy_references(body)

    assert references == {"SYN-POL-002", "SYN-POL-006"}


def test_unknown_policy_reference_is_rejected(
    tmp_path: Path,
) -> None:
    temporary_corpus = tmp_path / "policies"
    copytree(POLICY_DIRECTORY, temporary_corpus)

    policy_path = temporary_corpus / "01-basic-warranty-coverage.md"
    policy_text = policy_path.read_text(encoding="utf-8")
    policy_path.write_text(
        policy_text.replace(
            "SYN-POL-002",
            "SYN-POL-999",
            1,
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        PolicyCorpusValidationError,
        match="references unknown policy SYN-POL-999",
    ):
        validate_policy_corpus(temporary_corpus)


def test_validation_cli_succeeds(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = validation_cli_main([str(POLICY_DIRECTORY)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "PASS: validated 20 policies" in captured.out
    assert captured.err == ""


def test_validation_cli_fails_for_missing_corpus(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    missing_directory = tmp_path / "missing-policies"

    exit_code = validation_cli_main([str(missing_directory)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert "FAIL:" in captured.err
