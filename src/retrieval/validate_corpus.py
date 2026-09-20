import argparse
import sys
from pathlib import Path

from src.retrieval.corpus_validator import (
    PolicyCorpusValidationError,
    validate_policy_corpus,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the policy-corpus validation command parser."""

    parser = argparse.ArgumentParser(
        description="Validate the synthetic warranty policy corpus.",
    )
    parser.add_argument(
        "policy_directory",
        nargs="?",
        type=Path,
        default=Path("data/policies"),
        help="Policy directory containing manifest.json.",
    )

    return parser


def main(arguments: list[str] | None = None) -> int:
    """Validate the corpus and return a process exit code."""

    parser = build_parser()
    options = parser.parse_args(arguments)

    try:
        documents = validate_policy_corpus(options.policy_directory)
    except PolicyCorpusValidationError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"PASS: validated {len(documents)} policies in {options.policy_directory}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
