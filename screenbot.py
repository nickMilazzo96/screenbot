import requests
from bs4 import BeautifulSoup
import json
import openai
import configs
import api_keys

## RSS Scraping ##
def ab_clean(
    text,
):  # cleans up the abstract given in xml cause it's full of symbols and extraneous text
    start = text.find("ABSTRACT")
    text = text[start + len("ABSTRACT") :]
    end = text.find(" style=")
    text = text[:end]
    to_replace = [
        'xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:p1="http://pubmed.gov/pub-one">',
        "<p>",
        "<p",
        "</p>",
        "<b>",
        "</b>",
        "<i>",
        "</i>",
    ]
    for string in to_replace:
        text = text.replace(string, "")
    return text.strip()


def rss_scrape(
    rss_urls,
):  # from a given rss url returns a list of lists with elements [pmid, title, abstract]
    studies = []  # this is where you'll collect your new studies
    try:  # look for exlcusion_list.json
        with open("json/exclusion_list.json", "r") as f:
            exclusion_list = json.load(f)
            exclusion_set = set(
                exclusion_list
            )  # load json list and convert it to set for improved search
    except FileNotFoundError:
        exclusion_set = set([])  # if set doesn't exist, make it

    for url in rss_urls:
        feed = requests.get(url)
        feed_content = feed.content
        soup = BeautifulSoup(feed_content, features="xml")
        for item in soup.find_all("item"):
            pmid = item.find("dc:identifier").text[5:]
            if (
                pmid in exclusion_set
            ):  # check for pmid in exclusion_set. Only continue to other data if pmid is NOT in exclusion_set
                pass
            else:
                title = item.find("title").text
                abstract = ab_clean(item.find("content:encoded").text)
                studies.append([pmid, title, abstract])
                exclusion_set.add(pmid)
            # convert set to list for json dump
            exclusion_list = list(exclusion_set)
            with open("json/exclusion_list.json", "w") as f:
                json.dump(exclusion_list, f)
    return studies


## Process studies with GPT ##
def get_gpt_response(
    api_key, title, abstract
):  # takes title + abstract and returns "y" or "n" for relevance
    openai.api_key = api_keys.openai
    response = openai.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::AFlBwOlr",
        messages=[
            {
                "role": "system",
                "content": "Your job is to help me identify whether a study is relevant. It is relevant if it is conducted exclusively in humans, pertains to nutrition and/or supplementation, is a randomized trial, meta-analysis, or observational study. Studies where medications are the only intervention are not relevant. Please only respond with 'Y' (if relevant) or 'N' (if irrelevant). Your answers must be a single character.",
            },
            {"role": "user", "content": f"{title} | {abstract}"},
        ],
        temperature=0.1,
    )
    gpt_response = response.choices[0].message.content
    return gpt_response


def search_and_screen():  # takes list of lists, each element [pmid, title, abstract] and appends new "relevance" element. I.e., [pmid, title, abstract, relevant]
    with open("json/rss_feeds.json", "r") as f:
        rss_urls = json.load(f)

    studies_list = rss_scrape(
        rss_urls
    )  # takes a list of rss feeds, returns a list of lists with elements [pmid, title, abstract]

    # Iteratively pull studies from PubMed using search strings in df, put outputs in new dataframe 'results'
    for study in studies_list:
        study = study.append(get_gpt_response(api_keys.openai, study[1], study[2]))

    # Create json payload to push to Airtable
    with open("json/screened_studies.json", "w") as p:
        json.dump(studies_list, p, indent=4)


## Export to Airtable ##

# Headers for Airtable API requests
headers = {
    "Authorization": f"Bearer {api_keys.airtable}",
    "Content-Type": "application/json",
}

def airtable_batch_upload(
    records_batch,
):  # using output of search_and_screen, create new records in Airtable using batch API
    url = f"https://api.airtable.com/v0/{configs.BASE_ID}/{configs.TABLE_NAME}"

    # Prepare the batch of records
    data = {
        "records": [
            {
                "fields": {
                    "Title": record[1],
                    "PMID": record[0],
                    "Abstract": record[2],
                    "Relevant?": record[3],
                }
            }
            for record in records_batch
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Batch of {len(records_batch)} records created successfully.")
    else:
        print(f"Failed to create batch. Error: {response.text}")

############################################################
############################################################


search_and_screen()

# Load the list of lists from a JSON file
with open("json/screened_studies.json", "r") as f:
    records = json.load(f)

# Batch processing: Send records in batches of up to 10
BATCH_SIZE = 10

for i in range(0, len(records), BATCH_SIZE):
    records_batch = records[i : i + BATCH_SIZE]
    airtable_batch_upload(records_batch)
