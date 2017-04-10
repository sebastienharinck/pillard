import gzip
import urllib.request
import xml.etree.ElementTree as ET
import os
import urllib.request
import pprint
from datetime import datetime
import codecs

# VARIABLES
url = 'https://www.sample.fr/sitemap-main-index.xml.gz'
file = "sitemap-main-index.xml.gz"
word = 'words/'
file_name = 'test'
# END


# TODO refactor in object
# TODO if sitemap exist

req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
response = urllib.request.urlopen(req)

zipcontent = response.read()

with open(file, 'wb') as f:
    f.write(zipcontent)


# 0 unzip file

def unzip(file):
    inF = gzip.GzipFile( file , 'rb')
    s = inF.read()
    inF.close()

    new_file = file.replace(".gz", "")

    outF = open( new_file , "wb")
    outF.write(s)
    outF.close()

    # 1 get All URL
    tree = ET.parse( new_file )
    root = tree.getroot()

unzip(file)
def parcoursAllXML(root):
    for child in root:
        url = child[0].text
        file = "xml/"+url.rsplit('/',1)[1]
        print(file)

        req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
        response = urllib.request.urlopen(req)

        zipcontent = response.read()

        with open(file, 'wb') as f:
            f.write(zipcontent)

        # unzip file
        inF = gzip.GzipFile(file, 'rb')
        s = inF.read()
        inF.close()

        new_file = file.replace(".gz", "")
        new_file = "xml/"+new_file
        outF = open(new_file, "wb")
        outF.write(s)
        outF.close()

def find(file_name,word):
    fo = open(file_name, "w")
    compteur = 0
    for file in os.listdir("xml/xml"):
        if file.endswith(".xml"):
            # print(file)
            tree = ET.parse("xml/xml/"+file)
            test = tree.getroot()
            for child in test:
                if ( word in child[0].text):
                    print(compteur)
                    compteur = compteur + 1
                    fo.write(child[0].text+"\n")
                    print(child[0].text)
                    downloadHTML(child[0].text)
                    if(compteur >= 10):
                        sys.exit()


    fo.close()

def downloadHTML( url ):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib.request.urlopen(req)

    site_id = url.split('/')[-1]

    now = datetime.now()
    chain = str(now.year) + '-' + str(now.month) + '-' + str(now.day)

    with codecs.open('archives/' + chain + '-' + site_id + '.html', 'w', encoding='utf8') as f:
        f.write(con.read().decode('utf-8'))

    f.close()


#parcoursAllXML(root)
find(file_name, word)

f = gzip.open(file, 'rb')
file_content = f.read()
f.close()