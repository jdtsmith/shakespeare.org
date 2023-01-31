#!/usr/bin/env python3
# Parse XML markup for Shakespeare's plays as an Org-mode file.
# See https://github.com/okfn/shakespeare-material (Moby XML files)
# Call Syntax:
#   parse file1.xml file2.xml ...
#   
# JDS, Jan 2023
from xml.sax.handler import ContentHandler
from xml.sax import parse
import sys
import re


class Shk2Org(ContentHandler):
    headline = ("PLAY", "FM", "PERSONAE", "SPEECH", "ACT", "SCENE", "SCNDESCR")
    headline_verbatim = ("FM")
    drawer = ("SPEAKER")
    org_list = ("PERSONA")
    block = []
    content = ''

    def startElement(self, name, _attrs):
        self.block.append(name)
        self.content = ''
        if name in self.headline:
            print('*' * len(self.block), end=' ')
            if name in self.headline_verbatim:
                print(name.lstrip())
        elif name == "PGROUP":
            print(" - GROUP")
        elif name not in ("TITLE", "P", "PERSONA", "GRPDESCR",
                          "STAGEDIR", "PLAYSUBT", "LINE", "SPEAKER", "SUBHEAD"):
            print("UB: ", name)

    def endElement(self, _name):
        name = self.block.pop()

        if name in ('PERSONA'):
            self.content = re.sub(r"[A-Z']{2,}( [A-Z']{2,})*", r"*\g<0>*", self.content)

        if name == 'PERSONA':
            if self.block[-1] == 'PGROUP':
                list_start = "   + "
            else:
                list_start = " -"
            print(list_start, self.content)
        elif name == 'STAGEDIR':
            print(" : Stage Direction - ", self.content.strip())

    def characters(self, content):
        if content.strip() == "":
            return
        content = content.lstrip()
        inBlock = self.block[-1]
        if inBlock == 'STAGEDIR':
            self.content += " " + content
        elif inBlock == 'LINE':
            print(" ", content)
        elif inBlock == 'PERSONA':
            self.content += content
        elif inBlock == 'GRPDESCR':
            print("   : " + content)
        elif inBlock == 'TITLE':
            print("*" + content + "*")
        elif inBlock == 'SPEAKER':
            print(content)
        elif inBlock == 'SUBHEAD':
            print("*/" + content.rstrip() + "/*")
        elif inBlock == 'PLAYSUBT':
            pass
        else:
            print("/" + content + "/")


parser = Shk2Org()
for file in sys.argv[1:]:
    parse(file, parser)
