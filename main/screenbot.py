from screenbot_funcs import *
from rss_funcs import *
from airtable_export import airtable_batch_upload


search_and_screen()

# Load the list of lists from a JSON file
with open("screenbot/main/json/screened_studies.json", "r") as f:
    records = json.load(f)

# Batch processing: Send records in batches of up to 10
BATCH_SIZE = 10

for i in range(0, len(records), BATCH_SIZE):
    records_batch = records[i : i + BATCH_SIZE]
    airtable_batch_upload(records_batch)
