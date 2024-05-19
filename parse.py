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
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--tags','-t', action='store_true')
parser.add_argument('--max-nesting','-m', default=99, type=int)
parser.add_argument('--stats','-s', action='store_true')
parser.add_argument('--checkboxes','-c', action='store_true')
parser.add_argument('--todo','-d', action='store_true')
parser.add_argument('files', nargs='+')
args = parser.parse_args()

class Shk2Org(ContentHandler):
    headline = ("PLAY", "FM", "PERSONAE", "SPEECH", "ACT", "SCENE",
                "SCNDESCR","INDUCT","INDUCTION","PROLOGUE","EPILOGUE","SUBTITLE")
    headline_verbatim = ("FM")
    #drawer = ("SPEAKER")
    #org_list = ("PERSONA")
    block = []
    content = ''
    tag = None
    
    def startElement(self, name, _attrs):
        self.block.append(name)
        self.content = ''
        if name in self.headline:
            depth = len(self.block)
            if depth <= args.max_nesting:
                print('*' * len(self.block), end=' ')
                if args.todo and depth > 1:
                    print('TODO' if random.randint(0, 1) else 'DONE', end=' ')
            self.tag = name
            if name in self.headline_verbatim:
                print(name.lstrip())
        elif name == "PGROUP":
            if args.stats and args.checkboxes:
                stat = "[/]" if random.randint(0, 1) else "[%]"
            else:
                stat = " "
            print(" - GROUP", stat)
        elif name not in ("TITLE", "P", "PERSONA", "GRPDESCR",
                          "STAGEDIR", "PLAYSUBT", "LINE", "SPEAKER", "SUBHEAD"):
            print("UB: ", name)

    def endElement(self, _name):
        name = self.block.pop()

        if name in ('PERSONA'):
            self.content = re.sub(r"[A-Z']{2,}( [A-Z']{2,})*", r"*\g<0>*", self.content)

        if name == 'PERSONA':
            if self.block[-1] == 'PGROUP':
                list_start = "   +"
            else:
                list_start = " -"
            if args.checkboxes:
                list_start += " [" + ("X" if random.randint(0,1) else " ") + "]"
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
            c = "*" + content + "*"
            if (args.stats and
                (args.checkboxes or not self.tag == "PERSONAE") and
                len(self.block) > 1 and len(self.block) <= args.max_nesting):
                c += " [%] " if random.randint(0, 1) else " [/] "
            if len(self.block) > args.max_nesting + 1:
                print(c)
            else :
                if args.tags:
                    t = self.tag
                    #pad = 70-len(c)-len(self.block)-2
                    print(f"{c} :{t}:")
                else:
                    print(c)
        elif inBlock == 'SPEAKER':
            print(content)
        elif inBlock == 'SUBHEAD':
            print("*/" + content.rstrip() + "/*")
        elif inBlock == 'PLAYSUBT':
            pass
        else:
            print("/" + content + "/")


parser = Shk2Org()
for file in args.files:
    parse(file, parser)
