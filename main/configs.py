### OpenAI API key ###
api_key = "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"  # noqa: E501
model_id = "ft:gpt-4o-mini-2024-07-18:personal::AG5eHVCS"  # model tuned with v3 data on Oct 8
###

### Airtable Configs ###
AIRTABLE_API_KEY = "patnVP34xrFD8xPS9.37b8c996a32aab3600d686b4c20c848236c5a18de769a7031599e2dcbe3a7467"
BASE_ID = "app71xlZgKi5nUTQy"  # first part of url, beginning with "app"
TABLE_NAME = "tbl6quzHPHYGgIDXW"  # second part of url, beginning with "tbl"

# Headers for Airtable API requests
headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}", "Content-Type": "application/json"}
