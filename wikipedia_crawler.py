import time
import urllib

import bs4
import requests


start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Ancient_Greek"
#

def find_first_link(url):
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    # This div contains the article's body
    # (June 2017 Note: Body nested in two div tags)
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    # stores the first link found in the article, if the article contains no
    # links this value will remain None
    article_link = None

    # Find all the direct children of content_div that are paragraphs
    for element in content_div.find_all("p", recursive=False):
        # Find the first anchor tag that's a direct child of a paragraph.
        # It's important to only look at direct children, because other types
        # of link, e.g. footnotes and pronunciation, could come before the
        # first link to an article. Those other link types aren't direct
        # children though, they're in divs of various classes.
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break

    if not article_link:
        return

    # Build a full url from the relative article_link url
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)

    return first_link

def continue_crawl(search_history, target_url, max_steps=50):
    if search_history[-1] == target_url:
        print("Wir haben den gesuchten Artikel gefunden!")
        return False
    elif len(search_history) > max_steps:
        print("Das dauert verdächtig lang, wir hören lieber auf!")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("Das haben wir leider schon mal gesehen, beende die Suche!")
        return False
    else:
        return True

article_chain = [start_url]

while continue_crawl(article_chain, target_url):
    print(article_chain[-1])

    first_link = find_first_link(article_chain[-1])
    if not first_link:
        print("Dieser Artikel hat leider keine Links, beende die Suche!")
        break

    article_chain.append(first_link)

    time.sleep(2) # Slow things down so as to not hammer Wikipedia's servers
print("Anzahl der Versuche: " + str(len(article_chain)))
	

input('Zum Beenden "Enter" drücken')