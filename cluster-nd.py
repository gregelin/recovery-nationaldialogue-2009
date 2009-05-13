#!/usr/bin/python
"""A script to cluster ideas scraped from The National Dialogue

"""

__author__ = "Greg Elin (gelin@sunlightfoundation.com)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2009/04/30 $"
__copyright__ = "(CC) By Attribution"
__license__ = "Python"

import re


class ReadFile:
    '''Read a file and split it into lines.
    
    filename: name of file to read
    splitter: value to split lines, default is \n

    '''
    
    def __init__(self, filename, splitter="\n"):
        self.filename = filename
        self.splitter = splitter
        self.lines = []
        self.get_lines()
        
    def get_lines(self):
        try: 
            f = open( self.filename)
            self.lines = f.read().split(self.splitter)
            f.close()
        except IOError:
            print "Problem opening file ",filename
        
        
def getwords(txt):
    # Remove all HTML tags
    txt=re.compile(r'<[^>]+>').sub('', txt)
    
    # Split words by all non-alpha characters
    words=re.compile(r'[^A-Z^a-z]+').split(txt)
    
    # Convert to lowercase
    return [word.lower() for word in words if word!='']
    

def makedocs(division_pattern, textlines):
    '''Group a sequence of lines into a unique document after each division pattern is recognized.
    
    Returns a dictionary
    
    division_pattern: the regular expression which denotes start of a new pseudo doc
    textlines: the sequence of lines
    
    ''' 
    key = "default"
    docs = {key : ""}
    for line in textlines:
        m = re.match(division_pattern, line)
        if m:
            key = m.group(0)
        else:
            if docs.has_key(key): docs[key] = "\n".join([docs[key], line])
            else: docs[key] = ""
    return docs


def getwordcounts(txt):
    '''Returns a count of words in a block of text
    
    txt: block of text
    '''
    words=getwords(txt)
    wc = {}
    for word in words:
        wc.setdefault(word,0)
        wc[word]+=1
    #print "wc: ", wc, "\n------------"
    return wc
        

def main():
    f = "idea_dump_all.txt"
    rf = ReadFile(f,"\n")
    #print rf.filename

    # Create psuedo docs from the source file, using the 'src: url' as the division
    division_pattern = "^src: .*"
    docs = makedocs(division_pattern,rf.lines)
    
    # Extract list of word from each pseudo doc
    #docs_wc = getwordcounts(docs)
    
    apcount={}
    wordcounts={}
    for k,v in docs.items():
        #print "k: ",k
        wc=getwordcounts(v)
        wordcounts[k] = wc
        for word,count in wc.items():
            apcount.setdefault(word,0)
            if count>1:
                apcount[word]+=1
    
    # Keep words that appear in more than 10% of pseudo docs and less than 50% and are not in stop words
    stopwords=["how","has","by","such","one","so","a","the","of","at","as","this","also","an","that","have","are","be","s","on","or","with"]
    wordlist=[]
    for w,bc in apcount.items():
        frac=float(bc)/len(docs)
        if frac>0.1 and frac<0.50 and (w not in stopwords): wordlist.append(w)
    
    
    # Printing some basic information
    for word in wordlist:
        print "%d : %s" % (apcount[word], word)
    print "len(docs): ", len(docs)
    
ocdata.txt','w')
    out.write('idea')
    for word in wordlist: out.write("\t%s" % word)
    out.write("\n")
    for doc,wc in wordcounts.items():
        out.write(doc)
        for word in wordlist:
            if word in wc: out.write("\t%d" % wc[word])
            else: out.write("\t0")
        out.write("\n")
    

if __name__=="__main__":
    main()


    