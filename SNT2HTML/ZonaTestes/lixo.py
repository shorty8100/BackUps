# -*- coding: utf-8 -*-

menucsv = open(r"C:\S-Monitor\Files\Menu\bombagem.mnu.csv","r")
conteudo = menucsv.read()
menucsv.close()

dicIDs = {}
for linha in conteudo.split("\n"):
	dicINFO = {"descricao": "", "destino": "", "iconOFF": "", "iconON": ""}
	if "ID" in linha.split(";")[0]:
		if not linha.split(";")[0] in dicIDs:
			dicIDs[linha.split(";")[0]] = []
		dicINFO["descricao"] = linha.split(";")[1]
		dicINFO["destino"] = linha.split(";")[3]
		dicINFO["iconOFF"] = linha.split(";")[4]
		dicINFO["iconON"] = linha.split(";")[5]
		dicIDs[linha.split(";")[0]].append(dicINFO)

HTML = ""
HTML += '<ul> <li class="dropdown"><ul class="sub-menu">'
for menu in dicIDs["ID0"]:
	HTML += '<il>'
	HTML +='<a href="#">' + menu["descricao"] + "</a></li>"
HTML += '</li></ul>'

print(HTML)

