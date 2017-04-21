import gzip
import urllib.request
import xml.etree.ElementTree as ET
import os
import sys
import urllib.request
from datetime import datetime
import codecs

# VARIABLES

class Tools:

    def createfolder(self, folder):
        if folder != "":
            if not os.path.exists(folder):
                os.makedirs(folder)

    def unzip(self, fileGz, foldergz="", folderxml=""):
        inF = gzip.GzipFile(foldergz + fileGz, 'rb')
        s = inF.read()
        inF.close()

        # unzip FILE
        new_file = folderxml + fileGz.replace(".gz", "")

        outF = open(new_file, "wb")
        outF.write(s)
        outF.close()
        return new_file

    def checkFileFolder(self,file):
        return os.path.exists(file)


class XmlURL(Tools):
    def __init__(self, url, namefile,nbGetHTML):
        self.url = url
        self.nameUrls = namefile
        self.nbGetHTML = nbGetHTML

    def getGzpByURL(self):

        fileSiteMap = self.url.rsplit('/', 1)[1]
        print(fileSiteMap)
        if not (os.path.exists(fileSiteMap.replace(".gz", ""))): # si fichier xml exist
            if not (os.path.exists(fileSiteMap)): # si fichier gz exist
                print("GZ not exist firstUrl")
                req = urllib.request.Request(self.url, headers={'User-Agent': "Magic Browser"})
                response = urllib.request.urlopen(req)

                zipcontent = response.read()

                with open(fileSiteMap, 'wb') as f: # Récup gz via l'url
                    f.write(zipcontent)

            else:
                print("GZ exist")
            new_file = self.unzip(fileSiteMap)
        else:
            print("NO REQUETE URL")
            new_file = fileSiteMap.replace(".gz", "")
        tree = ET.parse(new_file)
        root = tree.getroot()
        return root



    def parcoursAllXML(self,root):
        if not (os.path.exists("sitemap/xml")):
            self.createfolder("sitemap")
            self.createfolder("sitemap/gz")
            self.createfolder("sitemap/xml")
            for child in root:
                url = child[0].text
                print(url)
                file = url.rsplit('/', 1)[1]

                req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
                response = urllib.request.urlopen(req)

                zipcontent = response.read()
                # print(zipcontent)

                with open("sitemap/gz/" + file, 'wb') as f:
                    f.write(zipcontent)

                self.unzip(file,"sitemap/gz/","sitemap/xml/")


    def findInAllXML(self,folder,word,downloadHTML = True):
        self.createfolder("archives")
        fo = open('test','w')
        compteur = 0
        for file in os.listdir(folder):
            if file.endswith(".xml"):
                tree = ET.parse(folder+"/"+file)

                root = tree.getroot()
                for child in root:

                    if (word in child[0].text):
                        print(compteur)
                        compteur = compteur + 1
                        print(child[0].text)
                        fo.write(child[0].text+"\n") #On stocke l'URL dans fichier test
                        if downloadHTML:
                            self.downloadHTML(child[0].text) # Download le html de l'url
                            if (compteur >= self.nbGetHTML):
                                sys.exit()



        fo.close()

    def downloadHTML(self,url):
        req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
        con = urllib.request.urlopen(req)

        site_id = url.split('/')[-1]

        now = datetime.now()
        chain = str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        with codecs.open('archives/' + chain + '-' + site_id + '.html', 'w', encoding='utf8') as f:
            f.write(con.read().decode('utf-8'))

        f.close()

def main():
    firstUrl = 'yoururl'
    fileName = "test"
    nbGetHTML = 10
    xmlURL = XmlURL(firstUrl, fileName,nbGetHTML)
    print("test")
    root = xmlURL.getGzpByURL() # Get the first sitemap GZ and unzip
    xmlURL.parcoursAllXML(root)
    word = 'rooms/'
    xmlURL.findInAllXML('sitemap/xml/', word, False)


main()
