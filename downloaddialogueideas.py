#!/usr/bin/python
"""A script to pull down the full idea page including comments from TheNationalDialogue.org
   
   Screen scrapes each individual idea from TheNationalDialogue.

"""

__author__ = "Greg Elin (gelin@sunlightfoundation.com)"
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2009/05/10 $"
__copyright__ = "(CC) By Attribution"
__license__ = "Python"

# TODO:
# Scrape is not getting all pages of the posts with more than 10 comments
# Fix counter on getting extra pages on comments

# Imports
from BeautifulSoup import BeautifulSoup
from urllib import urlopen
import re
import datetime
import codecs

# File formats
# http://www.thenationaldialogue.org/ideas/mostcomments_view/allideas_topic_view?b_start:int=5&-C=
# http://www.thenationaldialogue.org/ideas/mostcomments_view/allideas_topic_view?b_start:int=10&-C=
# <a class="question-title-short" href="http://www.thenationaldialogue.org/ideas/use-saas-for-project-performance-status">Use SaaS for Project Performance Status</a>
# url2 = "http://www.thenationaldialogue.org/ideas/mostcomments_view/allideas_topic_view?b_start:int=10&-C="
# url =  "http://www.thenationaldialogue.org/ideas/mostcomments_view/allideas_topic_view?b_start:int="+
#


files = ["http://www.thenationaldialogue.org/ideas/first-make-the-data-available-in-raw-form"]
files = []
df = "idea_list_all.tsv"

def clean(text):
    text = text.replace("&nbsp; ","")
    text = text.strip()
    return text
    
def clean_utf8(text):
    text = text.decode("utf-8")
    text = text.replace(u"\u201c", "\"").replace(u"\u201d", "\"") 
    text = text.replace(u"\u2018", "'").replace(u"\u2019", "'") 
    # trademark, short dash, long dash
    text = text.replace(u"\u2122", "(tm)").replace(u"\u2013", "-").replace(u"\u2014", "--")
    
    return text
    
def clean_line_endings(text):
    patterns = {# turn indicated paragraphs into new lines
        '</?p>' : "\r",
        '<p class="MsoBodyTextIndent">' : "\r",
        "<p .*?>" : "\r",
        # turn line breaks into returns
        '</?br ?/?>' : "\r",
        # turn fixed spaces into single space
        '&nbsp;' : " ",
        # isolate any headings on their own line
        '</?h[1234568]>' : "\r",
        # Fix weird large blocks. Example:
        '&lt;!--\r\r([ ./\w\W]*?)--&gt;' : "\r",
        # make <li> into new lines
        '<li>|<li .*?>[ ]*' :  "\r    -",
        '</li>' : " ",
        # make <ul> into new lines
        '<ul>|<ul .*?>[ ]*' : "\r/*ed: unordered list*/",
        '<ol>|<ol .*?>[ ]*' : "\r/*ed: ordered list*/",
        # remove all remaining HTML tags except for links
        '<(?!\/?a(?=>|\s.*>))\/?.*?>' : ' ',
        # clean up blank lines
        #'[ ]+\n' : "\n",
        #'[\t]+\n' : "\n",
        # convert three or more returns to two returns
        #'\r\r\r*' : "\r\r",
        # convert three or more returns to two returns
        #'\n\n\n*' : "\r\r",
        # convert two or more spaces to two spaces
        "[ ]+" : ' ',
        # convert tabs to spaces
        "\t" : '    ',
        '[ ]+\n\n' : "\n\n",
        #'[\t]+\n' : "\r",
        # remove repetitive text lines
         '[\n] idea [\n]' : "",
         'What is the idea[\?]' : "",
         'Why is it important[\?]' : "",
         # convert three or more returns to two returns
         '\r\r\r*' : "\r\r",
         # convert three or more returns to two returns
         '\n\n\n*' : "\n\n",
         
     }
    
    for key in patterns.keys():
        text = re.sub(key,patterns[key],text)
    return text

def getFullIdea(soup, src):
    q = soup.find(id="question")
    q = "%s" % q
    q = clean_line_endings(q)
    #question = unicode(question, "utf-8")
    q = clean_utf8(q)
    return q
    
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
    # Open file of urls and read the file into an array split on new lines
    f = open(df)
    lines = f.read().split("\n")
    f.close()
    timestamp = datetime.date.today().isoformat()

    for line in lines:
        try:
            src = line.split("\t")[1]
            files.append(src)
        except:
            continue 
    
    print "---\n"
    for file in files[0:550]:
        print file
        soup=BeautifulSoup(urlopen(file))
        idea = getFullIdea(soup, file)
        print "\n\n"
        print "%s: %s" % ("src", file)
        #print "%s: %s" % ("timestamp", timestamp)
        #print "%s: >\n %s" % ("idea", idea)
        print "%s" % (idea)
        #print "tags: %s" % extractTags(soup.find("ul", {"class" : "rubber-tags"}))
#        getComments(soup, file)
#        # Loop through extra pages of comments if exists
#        while (soup.find('span', {"class" : "next"})):
#            try:
#                s = (soup.find('span', {"class" : "next"}).find("a")["href"])
#                soup = BeautifulSoup(urlopen(s))
#                getComments(soup, file)
#            except:
#                continue
        
        

if __name__=="__main__":
    main()
    