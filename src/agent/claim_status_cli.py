import os
import sys

import boto3

from src.adapters.bedrock_converse import run_claim_status_assistant

DEFAULT_QUESTION = "What is the status of claim CLM-1002?"


def main() -> None:
    """Run the controlled claim-status assistant against Amazon Bedrock."""
    model_id = os.getenv("BEDROCK_MODEL_ID")

    if not model_id:
        raise SystemExit(
            "BEDROCK_MODEL_ID is required. Export the Bedrock inference profile ID."
        )

    region = os.getenv("AWS_REGION") or boto3.Session().region_name

    if not region:
        raise SystemExit(
            "No AWS Region is configured. Set AWS_REGION or configure an AWS profile."
        )

    question = " ".join(sys.argv[1:]).strip() or DEFAULT_QUESTION

    client = boto3.client(
        "bedrock-runtime",
        region_name=region,
    )

    answer = run_claim_status_assistant(
        client=client,
        model_id=model_id,
        question=question,
    )

    print(answer)


if __name__ == "__main__":
    main()