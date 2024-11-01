import json

import requests
from bs4 import BeautifulSoup


def ab_clean(text):  # cleans up the abstract given in xml cause it's full of symbols and extraneous text
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


def rss_scrape(rss_urls):  # from a given rss url returns a list of lists with elements [pmid, title, abstract]
    studies = []  # this is where you'll collect your new studies
    try:  # look for exlcusion_list.json
        with open("screenbot/main/json/exclusion_list.json") as f:
            exclusion_list = json.load(f)
            exclusion_set = set(exclusion_list)  # load json list and convert it to set for improved search
    except FileNotFoundError:
        exclusion_set = set([])  # if set doesn't exist, make it

    for url in rss_urls:
        feed = requests.get(url)
        feed_content = feed.content
        soup = BeautifulSoup(feed_content, "xml")
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
            with open("screenbot/main/json/exclusion_list.json", "w") as f:
                json.dump(exclusion_list, f)
    return studies


##########################

if __name__ == "__rss_main__":
    ab_clean()
    rss_scrape()
