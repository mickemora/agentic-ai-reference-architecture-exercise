from datetime import date
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

PolicyStatus = Literal["draft", "active", "superseded", "retired"]


class ContractModel(BaseModel):
    """Common validation behavior for policy-corpus contracts."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class PolicyMetadata(ContractModel):
    """Required YAML front matter for a synthetic policy document."""

    document_id: str = Field(pattern=r"^SYN-POL-\d{3}$")
    title: str = Field(min_length=3, max_length=120)
    category: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    component: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    market: Literal["synthetic-us"]
    effective_date: date
    version: str = Field(pattern=r"^\d+\.\d+$")
    status: PolicyStatus
    source_uri: str = Field(
        pattern=(
            r"^s3://agentic-ai-reference-architecture-exercise/"
            r"policies/\d{2}-[a-z0-9-]+\.md$"
        )
    )
    classification: Literal["synthetic-public-training"]


class PolicyDocument(ContractModel):
    """A policy document with validated metadata and Markdown content."""

    metadata: PolicyMetadata
    body: str = Field(min_length=1)


class ManifestDocument(ContractModel):
    """Compact document record stored in the corpus manifest."""

    document_id: str = Field(pattern=r"^SYN-POL-\d{3}$")
    path: str = Field(pattern=r"^\d{2}-[a-z0-9-]+\.md$")
    category: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    component: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class PolicyManifest(ContractModel):
    """Contract for the complete synthetic policy corpus manifest."""

    corpus_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    version: str = Field(pattern=r"^\d+\.\d+$")
    effective_date: date
    market: Literal["synthetic-us"]
    classification: Literal["synthetic-public-training"]
    documents: list[ManifestDocument] = Field(min_length=1)

    @model_validator(mode="after")
    def require_unique_documents(self) -> Self:
        document_ids = [document.document_id for document in self.documents]
        paths = [document.path for document in self.documents]

        if len(document_ids) != len(set(document_ids)):
            raise ValueError("Manifest document_id values must be unique")

        if len(paths) != len(set(paths)):
            raise ValueError("Manifest document paths must be unique")

        return self
