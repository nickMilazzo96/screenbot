import json
from pathlib import Path

from airtable_export import airtable_batch_upload
from screenbot_funcs import search_and_screen

search_and_screen()

# Load the list of lists from a JSON file
with Path.open("screenbot/main/json/screened_studies.json") as f:
    records = json.load(f)

# Batch processing: Send records in batches of up to 10
BATCH_SIZE = 10

for i in range(0, len(records), BATCH_SIZE):
    records_batch = records[i : i + BATCH_SIZE]
    airtable_batch_upload(records_batch)
