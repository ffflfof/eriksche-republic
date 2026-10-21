import os
import glob
import re

script_files = glob.glob("txtepisodes/s*e*script.txt")
latest_file = None
max_season_episode = (-1,-1)
for filepath in script_files:
    match = re.search(r's(\d+)e(\d+)_script\.txt', filepath)
    if match:
        season = int(match.group(1))
        episode = int(match.group(2))
        current_tuple = (season, episode)
        if current_tuple > max_season_episode:
            max_season_episode = current_tuple
            latest_file = filepath
if latest_file:
    seasonnum = max_season_episode[0]
    smth = max_season_episode[1]
    current_file = latest_file
else:
    exit()
with open(f"./{current_file}", "r") as file:
    txt = file.readlines()
with open(f"s{seasonnum}e{smth}.html", "w") as file:
    title = txt.pop(0)
    charlines = 0
    for i in txt:
        if i.strip() == "Script:" and charlines != 0:
            break
        else:
            charlines +=1
    file.write("<!DOCTYPE html>\n")
    file.write('<html lang="en">\n')
    file.write("<head>\n")
    file.write('\t<meta charset="UTF-8">\n')
    file.write('\t<link rel="stylesheet" href="episodes.css">\n')
    file.write(f'\t<title>{title.split(":")[0]}</title>\n')
    file.write("</head>\n")
    file.write("<body>\n")
    file.write('\t<div id="navbar">\n')
    if smth != 1:
        file.write(f'\t\t<a href="s{seasonnum}e{smth-1}.html">&lt;-- previous episode</a>\n')
    else:
        file.write('\t\t<span></span>\n')
    file.write('\t\t<a href="index.html">&lt; Home Page &gt;</a>\n')
    file.write('\t\t<span></span>\n')
    file.write("\t</div>\n")
    file.write(f"\t<h1><br>{title.strip()}</h1>\n")
    file.write(f"\t<h3>{txt[0].strip()}</h3>\n")
    file.write('\t<ul id="charlist">\n')
    for i in txt[1:charlines]:
        file.write(f"\t\t<li>{i.strip()}</li>\n")
    file.write("\t</ul>\n")
    for i in range(charlines):
        del txt[0]
    file.write(f"\t<h3>{txt.pop(0).strip()}</h3>\n")
    file.write('\t<div id="text">\n')
    for i in range(len(txt)):
        if not "\t" in txt[i] and not "    " in txt[i]:
            file.write(f"\t\t<h4>{txt[i].strip()}</h4>\n")
            file.write('\t\t<div class="indent">\n')
        elif ("\t" in txt[i] or "    " in txt[i]) and (i == len(txt)-1 or (not "\t" in txt[i+1] and not "    " in txt[i+1])):
            file.write(f"\t\t\t<p>{txt[i].strip()}</p>\n")
            file.write("\t\t</div>\n")
        elif ("\t" in txt[i] or "    " in txt[i]):
            file.write(f"\t\t\t<p>{txt[i].strip()}</p>\n")
    file.write("\t</div>\n")
    file.write("</body>\n")
    file.write("</html>\n")

with open("index.html", "r") as file:
    season = 0
    latestseasonindex = 0
    lastdivindex = 0
    txt2 = file.readlines()
    for index, i in enumerate(txt2):
        if "Season" in i:
            season = int(i.lstrip().split(" ")[1][0])
            latestseasonindex = index
        if "</div>" in i:
            lastdivindex = index
    if season == 0 and latestseasonindex == 0:
        txt2.insert(9, "\t<h2><br><br>Season 1: </h2>\n")
        latestseasonindex = 9
    if seasonnum > 1 and smth == 1:
        txt2.insert(lastdivindex+1, f"\t<h2><br>Season {seasonnum}: </h2>")
        latestseasonindex = lastdivindex+1
    if smth == 1:
        txt2.insert(latestseasonindex+1, "\t<div>\n")
        txt2.insert(latestseasonindex+2, f'\t\t<a href="s{seasonnum}e{smth}.html">{smth}</a>\n')
        txt2.insert(latestseasonindex+3, "\t</div>\n")
    if smth != 1 and smth != 24:
        txt2[lastdivindex-1]+= f'\t\t<a href="s{seasonnum}e{smth}.html">{smth}</a>\n'
    if smth == 24:
        txt2[lastdivindex-1]+= f'\t\t<a href="s{seasonnum}e{smth}.html">{smth}</a>\n'
with open("index.html", "w") as file:
    file.writelines(txt2)
if smth != 1:
    with open(f"s{seasonnum}e{smth-1}.html", "r") as file:
        txt3 = file.readlines()
        txt3[11] = f'\t\t<a href="s{seasonnum}e{smth}.html">next episode --&gt;</a>\n'
    with open(f"s{seasonnum}e{smth-1}.html", "w") as file:
        file.writelines(txt3)