#!/usr/bin/python
"""Extract links from a document. Extract just the URLs.


command line arguments in python.

-h  help                    display command line options
-f, <file> --file=<file>    source target file
-v, --verbose               verbose
-o, --output                output
-d, --debug                 turn debugging on

"""

__author__ = "Greg Elin"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2009/05/04 07:00:00 $"
__copyright__ = "Copyright (c) 2009 Greg Elin"
__license__ = "Python"

import sys
import getopt
import re
import codecs

_debug = 0 # turn debugging off

def usage():
    print __doc__
    
def extract_urls(str):
    urls = []
    pattern = """(((ht|f)tp(s?))\://)?(www.|[a-zA-Z].)[a-zA-Z0-9\-\.]+\.(com|edu|gov|m\r+il|net|org|biz|info|name|museum|us|ca|uk)(\:[0-9]+)*(/($|[a-zA-Z0-9\.+\,\;\?\'\\\+&amp;%\$#\=~_\-:!@]+))*\W"""
    for m in re.finditer(pattern, str):
        urls.append(m.group())
    return urls 

def url_standardize(url):
    # trim line endings
    url = url.strip()
    # remove ending ",/.;!&nbsp;&<>" and other punctutation
    url = re.sub("([,/.;:\?!&nbsp;&<>\)\"'])+$","",url)
    # replace smart quotes
    url = url.replace(u"\u201c", "").replace(u"\u201d", "")
    url = url.replace(u"\u2018", "").replace(u"\u2019", "")
    # remove "^\w "
    url = re.sub("(^\w )|(^p;)|(\w>)","",url)
    # remove anything that came from an email address
    url = re.sub("^\w@(.)*","",url)
    # make domain name lower case
    #url = re.sub("(www.|[a-zA-Z].)[a-zA-Z0-9\-\.]+\.(com|edu|gov|m\r+il|net|org|biz|info|name|museum|us|ca|uk)", "/\1/".lower(), url)
    
    return url
    
def url_filter(url):
    # remove urls starting with "^http://www.thenationaldialogue.org/"
    return re.sub("^http://www.thenationaldialogue.org(.)*","",url)

def main(argv):
    output = None
    verbose = False
    src_file = None
    
    try:
        opts, args = getopt.getopt(argv, "hf:vod", ["help", "file", "verbose", "output", "debug"])
    except getopt.GetoptError, err:
        # print error, and help information
        print str(err)
        print ""
        usage()
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-f", "--file"):
            src_file = arg
        elif opt == "-d":
            global _debug
            _debug = 1
        else:
            assert False, "unhandled option"

    print "file = %s" % src_file
    
    # Open file and read the file into an array split on new lines
    f = codecs.open(src_file,"r","utf-8")
    lines = f.read().split("\n")
    f.close()
    
    urls_a = []
    uniq = {}
    
    for item in lines:
        # track if we are idea of comment
        my_urls = extract_urls(item)
        for key in my_urls:
            key = url_standardize(key)
            key = url_filter(key)
            if uniq.has_key(key):
                # add information to uniq key
                uniq[key]["reference"].append(item)
            else:
                # create new uniq key
                uniq[key] = {"key":key, "reference":[item]}
                
   
    for key in uniq.keys():
        print "%s" % key
        #print uniq[key]


if __name__ == "__main__":
    main(sys.argv[1:])
