import gzip
import urllib.request
import xml.etree.ElementTree as ET
import os
import sys
import urllib.request
from datetime import datetime
import codecs

# VARIABLES



# END

# TODO init projet (Création des dossiers)
def createfolder(folder):
    if folder != "":
        if not os.path.exists(folder):
            os.makedirs(folder)

def unzip(fileGz):
    inF = gzip.GzipFile(fileGz, 'rb')
    s = inF.read()
    inF.close()

    # unzip FILE
    new_file = fileGz.replace(".gz", "")

    outF = open(new_file, "wb")
    outF.write(s)
    outF.close()
    return new_file

# TODO récup premier sitemap (url, file) => création d'un fichier xml : fileXML

def getGzpByURL(url):

    fileSiteMap = url.rsplit('/', 1)[1]
    print(fileSiteMap)
    if not (os.path.exists(fileSiteMap.replace(".gz", ""))):
        if not (os.path.exists(fileSiteMap)):
            print("GZ not exist firstUrl")
            req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
            response = urllib.request.urlopen(req)

            zipcontent= response.read()

            with open(fileSiteMap, 'wb') as f:
                f.write(zipcontent)
            # Récup gz via l'url
        else:
            print("GZ exist")
        new_file = unzip(fileSiteMap)
    else:
        print("NO REQUETE URL")
        new_file = fileSiteMap.replace(".gz", "")
    tree = ET.parse(new_file)
    root = tree.getroot()
    return root


# TODO parcours toutes les sous sitemaps( fileXML)
# 1 get All URL


def parcoursAllXML(root):
    if not (os.path.exists("sitemap/xml")):
        createfolder("sitemap")
        createfolder("sitemap/gz")
        createfolder("sitemap/xml")
        for child in root:
            url = child[0].text
            print(url)
            file = url.rsplit('/', 1)[1]

            req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
            response = urllib.request.urlopen(req)

            zipcontent = response.read()
            # print(zipcontent)

            with open("sitemap/gz/"+file, 'wb') as f:
                f.write(zipcontent)

            # 0 unzip file
            inF = gzip.GzipFile("sitemap/gz/"+file, 'rb')
            s = inF.read()
            inF.close()

            new_file = file.replace(".gz", "")
            new_file = "sitemap/xml/" + new_file
            outF = open(new_file, "wb")
            outF.write(s)
            outF.close()






# TODO récupere tous les gz dans sitemaps/gz
# TODO Parcours tout les gz , dézip dans sitemaps/xml
# TODO Parcours tout les sitemaps/xml.


# TODO Recherche tout les urls contenant "rooms/"
def findInAllXML(folder,word):
    createfolder("archives")
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
                    downloadHTML(child[0].text) # Download le html de l'url
                    if(compteur >= 10):
                        sys.exit()


    fo.close()

# TODO Stockage dans un fichier : urlRooms
# TODO Parcours url du fichier : urlRooms
# TODO Télécharge tout les html jusqu'à 10 dans dossier archives/dateAujourd'hui/dateAujourd'hui_ID.html

# TODO refactor in object
# TODO if sitemap exist

def downloadHTML( url ):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib.request.urlopen(req)

    site_id = url.split('/')[-1]

    now = datetime.now()
    chain = str(now.year) + '-' + str(now.month) + '-' + str(now.day)

    with codecs.open('archives/' + chain + '-' + site_id + '.html', 'w', encoding='utf8') as f:
        f.write(con.read().decode('utf-8'))

    f.close()

def main():

    firstUrl = 'yourUrl'

    root = getGzpByURL(firstUrl) # Get the first sitemap GZ and unzip
    parcoursAllXML(root)
    word = 'test'
    findInAllXML('sitemap/xml/', word)


main()
