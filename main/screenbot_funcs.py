import json
import os

import configs as configs
import openai
from Bio import Entrez
from rss_funcs import *


def search_and_screen():  # takes list of lists, each element [pmid, title, abstract] and appends new "relevance" element. I.e., [pmid, title, abstract, relevant]
    with open("screenbot/main/json/rss_feeds.json") as f:
        rss_urls = json.load(f)

    studies_list = rss_scrape(
        rss_urls,
    )  # takes a list of rss feeds, returns a list of lists with elements [pmid, title, abstract]

    # Iteratively pull studies from PubMed using search strings in df, put outputs in new dataframe 'results'
    for study in studies_list:
        study = study.append(get_gpt_response(configs.api_key, study[1], study[2]))

    # Create json payload to push to Airtable
    with open("screenbot/main/json/screened_studies.json", "w") as p:
        json.dump(studies_list, p, indent=4)


# Ask user for .csv file
## ASSUMED CSV FORMAT ##
## string_name | search_string ###
def csv_prompt():
    csv_file = input("Please provide a path to the .csv file with your search strings...")
    if not os.path.isfile(csv_file):
        print("The provided path is not a valid file. Please try again.")
        csv_file = input("Please provide a path to the .csv file with your search strings... ")
    print("Valid path provided. Proceeding...")
    return csv_file


# Formula for scraping study PMID, title, and abstract from PubMed using given search string
def pubmed_scrape(ncbi_email, search_string, max_results, min_date):
    # Set your email here
    Entrez.email = ncbi_email

    try:
        # Pull PMIDs resulting from search string and store them in variable pmid_list
        handle = Entrez.esearch(db="pubmed", term=search_string, retmax=max_results, sort="relevance", mindate=min_date)
        record = Entrez.read(handle)
        handle.close()
        id_list = record["IdList"]

        # Pull details of relevant pmids and store in a list of dictionaries
        ids = ",".join(id_list)
        handle = Entrez.efetch(db="pubmed", id=ids, rettype="xml")
        records = Entrez.read(handle)
        handle.close()

        articles = []
        for record in records["PubmedArticle"]:
            article = {}
            article["PMID"] = record["MedlineCitation"]["PMID"]
            article["Title"] = record["MedlineCitation"]["Article"]["ArticleTitle"]
            # Prevents an error if no abstract is available.
            if (
                "Abstract" in record["MedlineCitation"]["Article"]
                and "AbstractText" in record["MedlineCitation"]["Article"]["Abstract"]
                and len(record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]) > 0
                and record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]
            ):
                article["Abstract"] = record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]
            else:
                article["Abstract"] = "No abstract available."
            articles.append(article)

        return articles

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


# Formula for getting GPT response from OpenAI API
def get_gpt_response(api_key, title, abstract):
    openai.api_key = api_key
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


##########################

if __name__ == "__main__":
    pubmed_scrape()
    get_gpt_response()
    csv_prompt()
