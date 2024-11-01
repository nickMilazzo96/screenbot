import requests
from configs import *


# Function to create multiple records in Airtable using batch API
def airtable_batch_upload(records_batch):
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

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Batch of {len(records_batch)} records created successfully.")
    else:
        print(f"Failed to create batch. Error: {response.text}")


if __name__ == "__main__":
    airtable_batch_upload()
