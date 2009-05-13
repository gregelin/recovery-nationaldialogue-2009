#!/usr/bin/python
"""A script to pull down the full idea page including comments from TheNationalDialogue.org

"""

__author__ = "Greg Elin (gelin@sunlightfoundation.com)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2009/04/30 $"
__copyright__ = "(CC) By Attribution"
__license__ = "Python"

# TODO:
# Scrape is not getting all pages of the posts with more than 10 comments

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


files = ["http://www.thenationaldialogue.org/ideas/first-make-the-data-available-in-raw-form"]
files = []
df = "scrape_highest_comments_all.tsv"

def clean(text):
    text = text.replace("&nbsp; ","")
    text = text.strip()
    return text

def getFullIdea(soup, src):
    question = soup.find(id="question")
    return question
    
def getComments(soup, src):
    cnum = 0
    for comment in soup.findAll("div", {"class" : "answer-content"}):
        cnum = cnum + 1
        s = comment.contents[3]
        try: 
            author_url = comment.find("span", {"class":"documentAuthor"}).find("a")['href']
            author = comment.find("span", {"class":"documentAuthor"}).find("a").contents[0]
        except:
            author_url = None
            author =  None
        print "%s: %s" % ("author", author)
        print "%s: %s" % ("author_url", author_url)
        print "%s: %s" % ("comment_number", cnum)
        print "comment: >\n"
        while getattr(s, 'name', None) != 'div':
            if (s != "\n"):
                print s
            s = s.next

def getVotes(str):
    p = re.compile('[0-9]+')
    if p.search(str):
        val = p.search(str).group().strip()
    else:
        val = None
    return val

def extractTags(soup):
    try: 
        tags = "; ".join(["%s" % li.contents[1].contents[0] for li in soup.findAll('li')])
    except: 
        tags = None
    return tags

def main():
    # Open file and read the file into an array split on new lines
    f = open(df)
    lines = f.read().split("\n")
    f.close()
    timestamp = datetime.date.today().isoformat()
    
    for line in lines:
        src = line.split("\t")[1]
        files.append(src)
    
    print "---\n"
    for file in files[0:270]:
        soup=BeautifulSoup(urlopen(file))
        idea = getFullIdea(soup, file)
        print "\n\n"
        print "%s: %s" % ("src", file)
        print "%s: %s" % ("timestamp", timestamp)
        print "%s: >\n %s" % ("idea", idea)
        print "tags: %s" % extractTags(soup.find("ul", {"class" : "rubber-tags"}))
        #getComments(soup, file)
        


if __name__=="__main__":
    main()
    