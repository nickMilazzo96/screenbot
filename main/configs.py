### OpenAI API key ###
model_id = 'ft:gpt-4o-mini-2024-07-18:personal::AG5eHVCS' # model tuned with v3 data on Oct 8
###

### Airtable Configs ###
BASE_ID = 'app71xlZgKi5nUTQy'  # first part of url, beginning with "app"
TABLE_NAME = 'tbl6quzHPHYGgIDXW' # second part of url, beginning with "tbl"

# Headers for Airtable API requests
headers = {
    'Authorization': f'Bearer {AIRTABLE_API_KEY}',
    'Content-Type': 'application/json'
}
