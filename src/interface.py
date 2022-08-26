# Librairies #

from bs4 import BeautifulSoup
import os
import re
import shutil

# Interface #

def makeInterface(sourceXml, sourceHtml, targetHtml, tempFile):

	# Transformation des éléments XML en HTML #
	
	with open(sourceXml, "r", encoding="utf-8") as file:
	
		soup = BeautifulSoup(file, "html.parser")
	
		myText = soup.find("text")
		myText.name = "div"
		myText.attrs = {"id" : "text", "class" : "row"}
					
		for elt in myText.find_all("add"):
			elt.name = "ins"
		
		for elt in myText.find_all("hi", attrs = {"rend" : "u"}):
			elt.name = "span"
			elt.attrs = {"class" : "underline"}
			
		for elt in myText.find_all("hi", attrs = {"rend" : "superscript"}):
			elt.name = "sup"
			elt.attrs = {}
			
		for elt in myText.find_all("head"):
			elt.name = "h2"
			elt.attrs = {"class" : "play-title"}
			
		for elt in myText.find_all("lb"):	
			elt.name = "br"
			
		for elt in myText.find_all("p"):
			elt.name = "p"
			elt.attrs = {"class" : "main"}
			
		for elt in myText.find_all("note", attrs = {"place" : "margin-right"}):
			elt.name = "p"
			elt.attrs = {"class" : "note-right"}
			
		for elt in myText.find_all("note", attrs = {"place" : "margin-left"}):
			elt.name = "p"
			elt.attrs = {"class" : "note-left"}
			
		for elt in myText.find_all("note", attrs = {"place" : "margin-top-left"}):
			elt.name = "p"
			elt.attrs = {"class" : "note-left"}
			
		for elt in myText.find_all("fw"):
			elt.name = "p"
			elt.attrs = {"class" : "folio"}
			
		for elt in myText.find_all("speaker"):
			elt.name = "span"
			elt.attrs = {"class" : "speaker"}
			
		for elt in myText.find_all("stage"):
			elt.name = "span"
			elt.attrs = {"class" : "stage"}
	
	with open(tempFile, "w", encoding="utf-8") as file:
		file.write(str(myText))
		
	# REGEX #
			
	with open(tempFile, "r", encoding="utf-8") as file:
	
		linesRaw = file.readlines()
		linesCorr = []
		for line in linesRaw:
			line = re.sub('<div n="[0-9]" type="(.*?)">', "", line)
			line = re.sub("</div>", "", line)
			line = re.sub('<pb facs="(.*?)" n="(.*?)">', r'</div><div class="col-6 myImage"><img src="media/\1"></div><div class="col-6 myText">', line)
			line = re.sub("</pb>", "", line)
			line = re.sub(r'^\s*$', "", line)
			line = re.sub("<body>", "<div>", line)
			line = re.sub("</body>", "</div></div>", line)
			line = re.sub('<sp who="(.*?)">', "", line)
			line = re.sub("</sp>", "", line)
			line = re.sub("<l>", '<p class="line">', line)
			line = re.sub("</l>", "</p>", line)
			line = re.sub('<list type="speakers">', "", line)
			line = re.sub("</list>", "", line)
			line = re.sub('<item xml:id="(.*?)"></item>', "", line)
			line = re.sub('<delspan spanto="(.*?)" type="(.*?)"></delspan>', '<span class="delSpan"></span>', line)
			line = re.sub('<anchor xml:id="(.*?)"></anchor>', '<span class="delSpan"></span>', line)
			line = re.sub('<handshift medium="(.*?)"></handshift>', "", line)
			line = re.sub('<handshift resp="(.*?)"></handshift>', "", line)
			
			linesCorr.append(line)
			
	with open(tempFile, "w", encoding="utf-8") as file:
			
		for line in linesCorr:
			file.write(line)
		print("Done", "Interface adjustment : ", sourceXml)
	
	# Création du fichier final #
	
	with open(tempFile, "r", encoding="utf-8") as file:
		soup = BeautifulSoup(file, "html.parser")
	
		myText = soup.find("div", attrs = {"id" : "text"})
						
	with open(sourceHtml, "r", encoding="utf-8") as file:
		soup = BeautifulSoup(file, "html.parser")
		
		div = soup.find("div", attrs = {"id" : "mainText"})
		div.clear()
		div.append(myText)
		
	with open(targetHtml, "wb") as fichier:
		fichier.write(soup.prettify("utf-8"))
		print("Done", "Create target HTML file : ", targetHtml)
	
	# Numérotation des class #
	
	with open(targetHtml, "r", encoding="utf-8") as file:
		soup = BeautifulSoup(file, "html.parser")
		myText = soup.find("div", attrs = {"id" : "text"})
		
		# Traitement des images #
		i = 0
		for elt in myText.find_all("div", {"class": "myImage"}):
			myImageId = "myImage" + str(i)
			elt.attrs = {"id" : myImageId, "class" : "col-12 col-lg-6 myImage card overflow-auto", "style" : "display:none; max-width:100%; max-height:80vh; height:auto;"}
			i = i+1
			
		# Traitement des textes #
		j = 0
		for elt in myText.find_all("div", {"class": "myText"}):
			myTextId = "myText" + str(j)
			elt.attrs = {"id" : myTextId, "class" : "col-12 col-lg-6 myText card overflow-auto", "style" : "display:none; max-height:80vh"}
			j = j+1
	
	with open(targetHtml, "r", encoding="utf-8") as file:
		soup = BeautifulSoup(file, "html.parser")
	
		div = soup.find("div", attrs = {"id" : "mainText"})
		div.clear()
		div.append(myText)
		
	with open(targetHtml, "wb") as fichier:
		fichier.write(soup.prettify("utf-8"))
		print("Done", "Make interface", targetHtml)
	
	
	# JavaScript #
		
	with open(targetHtml, "r", encoding="utf-8") as file:
		soup = BeautifulSoup(file, "html.parser")
		myScript = soup.find("script", attrs = {"src" : "js/script.js"})
		myScript.name = "script"
		myScript.attrs = {"src" : "js/script_g267.js"}
			
	with open(targetHtml, "wb") as fichier:
		fichier.write(soup.prettify("utf-8"))
		print("Done", "Change Script", targetHtml)
		
def main():

	sourceXml = os.path.abspath("../corpus/flaubert_g267.xml")
	sourceHtml = os.path.abspath("../src/lorem-ipsum.html")
	targetHtml = os.path.abspath("../g267.html")
	tempFile = os.path.abspath("../src/tempFile.xml")
	makeInterface(
		sourceXml=sourceXml,
		sourceHtml=sourceHtml,
		targetHtml=targetHtml,
		tempFile=tempFile,
	)

main()