import requests
from urllib.request import urlopen
from datetime import datetime, timedelta, timezone


def main():
    articleName = input("Enter the name of the article you'd like to search")

    endDate = datetime.now(timezone.utc)
    startDate = endDate - timedelta(days=30)

    URL = "https://en.wikipedia.org/w/api.php"

    rvstart = endDate.strftime("%Y-%m-%dT%H:%M:%SZ")
    rvend = startDate.strftime("%Y-%m-%dT%H:%M:%SZ")

    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": articleName,
        "rvlimit": "max", # use "max" to get as many as allowed per request (500 for bots, 50 for users)
        "rvstart": rvstart,
        "rvend": rvend,
        "rvdir": "older",
        "rvprop": "timestamp|user|comment"
    }

    S = requests.Session()
    allRevisions = []

    while True:
        try: 
            R = S.get(url=URL, params=PARAMS)
            DATA = R.json()

            pages = DATA.get("query", {}).get("pages", {})

            for articleName, pageData in pages.items():
                revisions = pageData.get("revisions", [])
                allRevisions.extend(revisions)

                if pageData.get("title") != articleName:
                    print("Redirected to", pageData.get("title"))
                    articleName = pageData.get("title")
                    
                else: 
                    articleName = pageData.get("title")
                    
            if "continue" in DATA:
                PARAMS["rvcontinue"] = DATA["continue"]["rvcontinue"]
            else:
                print("Error: Article not found")
                break

        except: 
            print("Error: No Network Connection")
            break

    if articleName == "":
        print("Error: Invalid Name")

    else: 
        print(f"Changes for article {articleName}")

    for revision in allRevisions:
        print(f"{revision['timestamp']} by {revision['user']}\nComment: {revision.get('comment', '')}")

main()