# ScreenBot

ScreenBot is a Python script designed to scrape RSS feeds from PubMed, filter out excluded studies, and screen the remaining studies for relevance using OpenAI's GPT. The results are then saved and can be uploaded to Airtable.

## Installation & Requirements
This project is managed using [uv](https://docs.astral.sh/uv/). 

Clone the repository:
```sh
git clone <repository-url>
cd <repository-directory>
```

Create and activate a virtual environment using uv:
```sh
uv venv
```

Activate virtual environment with
```sh
source path/to/virtual/env/bin/activate
```

Install the required packages:
```sh
uv sync
```

### Python
Python >= 3.12

### Packages
bs4>=0.0.2
lxml>=5.3.0
openai>=1.54.3
requests>=2.32.3

## Project Structure
```sh
__pycache__/
.ruff_cache/
json/
    exclusion_list.json
    rss_feeds.json
    screened_studies.json
configs.py
pyproject.toml
README.md
screenbot.py
uv.lock
```
### Configuration
**configs.py:** Contains configuration variables such as the OpenAI API key.

**json:** Contains .json files for the program.

### Usage
**RSS Scraping**

The rss_scrape function scrapes RSS feeds from PubMed and filters out studies listed in exclusion_list.json.

**Abstract Cleaning**

The ab_clean function cleans up the abstract text extracted from the RSS feed.

**Search and Screen**

The search_and_screen function loads RSS feed URLs from rss_feeds.json, scrapes the feeds, and screens the studies for relevance using OpenAI's GPT.

**Airtable Batch Upload**

The airtable_batch_upload function uploads the screened studies to Airtable.

## Usage
To run the script, simply execute screenbot.py:

## License
This project is licensed under the MIT License. See the LICENSE file for details.


