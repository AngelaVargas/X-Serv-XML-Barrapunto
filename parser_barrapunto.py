#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys


def normalize_whitespace(text):
    string = ""
    return string.join(text)


class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.fichero = open("noticias.html", "w")
        self.link = ""
        self.title = ""
        self.noticia = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
                self.title = self.theContent
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = normalize_whitespace(self.theContent)		#Junto los titulos
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = normalize_whitespace(self.theContent)			#Junto los links
                self.noticia = "<li><a href=" + self.link + ">" + self.title + "</a></li>"	#Creo una lista ordenada con los titulos y links
                self.fichero.write(self.noticia)		#Escribo la lista ordenada en el fichero
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

if len(sys.argv)<2:
    print ("Usage: python xml-parser-barrapunto.py <document>")
    print ("")
    print (" <document>: file name of the document to parse")
    sys.exit(1)
    
# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = open(sys.argv[1],"r")
theParser.parse(xmlFile)

print ("Parse complete")

