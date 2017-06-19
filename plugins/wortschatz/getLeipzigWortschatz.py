# -*- coding: utf-8 -*-

import urllib.request
from html.parser import HTMLParser

def replace_spec_chars (string):
    string = replace_white_space(string)
    output = ""
    splits = string.split()
    for s in splits:
        s = s.replace('\\xc3\\xbc', 'ü')
        s = s.replace('\\xc3\\xb6', 'ö')
        s = s.replace('\\xc3\\xa4', 'ä')
        s = s.replace('\\xc3\\x9c', 'Ü')
        s = s.replace('\\xc3\\x96', 'Ö')
        s = s.replace('\\xc3\\x84', 'Ä')
        s = s.replace('\\xc3\\x9f', 'ß')

        output = output +s+" "
    return output

def replace_white_space (token):
    token = token.replace("\\n", "")
    token = token.replace("\\t", "")
    return token


def get_data (keyword):

    site = urllib.request.urlopen('http://corpora.uni-leipzig.de/de/res?corpusId=deu_newscrawl_2011&word='+str(keyword))
    readIn = site.read()
    readIn = str(readIn)

    entries = []

    class MyHTMLParser(HTMLParser):
        def handle_data(self, data):
            entries.append(data)


    parser = MyHTMLParser()
    parser.feed(readIn)

    result = {}
    result["gesuchtes Wort"] = keyword
    index = 0
    while index < len(entries):
        #print(entries[index])
        if entries[index].startswith("Anzahl"):
            split = entries[index].split(": ")
            anzahl = split[1]
            result["Frequenz"] = anzahl
        if entries[index].startswith(" Rang"):
            split = entries[index].split(": ")
            rang = split[1]
            result["Wortrang"] = rang
        if entries[index].startswith("Artikel:"):
            artikel = entries[index+1]
            artikel = artikel.strip()
            artikel = replace_spec_chars(artikel)
            result["Artikel"] = artikel
        if entries[index].startswith("Wortart:"):
            wortart = entries[index+1]
            wortart = wortart.strip()
            wortart = "".join(wortart.split())
            wortart = replace_spec_chars(wortart)
            result["Wortart"] = wortart
        if entries[index].startswith("Beschreibung:"):
            desc = entries[index+1]
            desc = desc.strip()
            desc = replace_spec_chars(desc)
            result["Beschreibung"] = desc
        if entries[index].startswith("Synonym:"):
            counter = index + 2
            tmps = entries
            synonyme = ""
            i = counter + 1
            while counter < len(tmps):
                if counter < i + 6:
                    synonyme = synonyme + entries[counter]
                else:
                    break
                counter = counter + 1
            synonyme = "".join(synonyme.split())
            synonyme = replace_spec_chars(synonyme)
            result["Synonyme"] = synonyme
        index += 1

    output = ""
    for k,v in result.items():
        output = output + str(k)+":\t"+str(v)+"\n"

    return output
