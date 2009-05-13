#!/usr/bin/python
"""A script to pull down all the ideas from TheNationalDialogue.org

"""

__author__ = "Greg Elin (gelin@sunlightfoundation.com)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2009/04/30 $"
__copyright__ = "(CC) By Attribution"
__license__ = "Python"

# TODO:

# Imports
from BeautifulSoup import BeautifulSoup
from urllib import urlopen
import re
import datetime

# File formats
# http://www.thenationaldialogue.org/ideas/mostcomments_view/allideas_topic_view?b_start:int=5&-C=
# http://www.thenationaldialogue.org/ideas/mostcomments_view/allideas_topic_view?b_start:int=10&-C=
# <a class="question-title-short" href="http://www.thenationaldialogue.org/ideas/use-saas-for-project-performance-status">Use SaaS for Project Performance Status</a>
# url2 = "http://www.thenationaldialogue.org/ideas/mostcomments_view/allideas_topic_view?b_start:int=10&-C="
# url =  "http://www.thenationaldialogue.org/ideas/mostcomments_view/allideas_topic_view?b_start:int="+
#

url_prefix = "http://www.thenationaldialogue.org/ideas/mostcomments_view/allideas_topic_view?b_start:int="
url_suffix = "&-C="
pages = 120
increment = 5

try:
    contact_email = person.parent.parent.findNextSibling('tr').findNextSibling("tr").findNextSibling("tr").contents[1].contents[0].contents[0]
except:
    contact_email = None
    
def clean(text):
    text = text.replace("&nbsp; ","")
    text = text.strip()
    return text

def getIdeas(src):
    soup=BeautifulSoup(urlopen(src))
    for idea in soup.findAll("a", {"class" : "question-title-short"}):
        
        href = idea['href']
        name = idea.contents[0].strip()
        author = idea.parent.findNextSibling('p').find("a").contents[0]
        try:
            comments = idea.parent.findNextSibling('a').contents[0].strip()
        except: 
            comments = None
        try:
            stars = idea.parent.findNextSibling('div').contents[3].contents[0].split("Number of stars: ")[1].strip()
        except: 
            stars = None
        try:
            votes = getVotes(idea.parent.findNextSibling('div').contents[3].contents[2].split("based on ")[1]).strip()
        except:
            votes = None
        timestamp = datetime.date.today().isoformat()
        print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (name, href, author, comments, stars, votes, src, timestamp)

def getVotes(str):
    p = re.compile('[0-9]+')
    if p.search(str):
        val = p.search(str).group().strip()
    else:
        val = None
    return val


def main():
    for num in range(0, pages):
        i = num*increment
        file = url_prefix+`i`+url_suffix
        getIdeas(file)


if __name__=="__main__":
    main()
    