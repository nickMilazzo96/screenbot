import logging
from typing import Any

import requests
from configs import BASE_ID, TABLE_NAME, headers

logger = logging.getLogger(__name__)


# Function to create multiple records in Airtable using batch API
def airtable_batch_upload(records_batch: list[tuple[Any, Any, Any, Any]]) -> None:
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

    # Prepare the batch of records
    data = {
        "records": [
            {
                "fields": {
                    "Title": record[1],
                    "PMID": record[0],
                    "Abstract": record[2],
                    "Relevant?": record[3],
                },
            }
            for record in records_batch
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        logger.info(f"Batch of {len(records_batch)} records created successfully.")
    except Exception:
        logger.exception("Failed to create batch.")


if __name__ == "__main__":
    airtable_batch_upload()
