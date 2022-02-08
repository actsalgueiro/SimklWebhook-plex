import os
import time
import xml.etree.ElementTree as ET
import requests

filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'anime-list.xml')

def getScudLee():
    # create element tree object from ScudLee XML
    # get ScudLee XML from github
    if not os.path.exists(filepath):
        scudleeXML = requests.get("https://raw.githubusercontent.com/Anime-Lists/anime-lists/master/anime-list.xml")
        with open(filepath, "wb") as f:
            f.write(scudleeXML.content)
    else: 
        # update XML if its older than 24h
        try: 
            if time.time() - os.path.getmtime(filepath) > 60*60*24:
                scudleeXML = requests.get("https://raw.githubusercontent.com/Anime-Lists/anime-lists/master/anime-list.xml")
                with open(filepath, "wb") as f:
                    f.write(scudleeXML.content)
        except OSError:
            scudleeXML = requests.get("https://raw.githubusercontent.com/Anime-Lists/anime-lists/master/anime-list.xml")
            with open(filepath, "wb") as f:
                f.write(scudleeXML.content)

def anidbToTvdb(anidbid, episode):
    """Convert the Tvdb anime info into Anidb info

    Args:
        anidbid (int): TvdbID of the anime
        episode (int): Tvdb episode

    Returns:
        tvdbidb: Corresponding TvdbID of the anime
        season: Anime seasons in Tvdb
        episode: Anime episode in Tvdb
    """
    
    getScudLee()
    tree = ET.parse(filepath)
    root = tree.getroot()

    for anime in root.findall(f'./*[@anidbid="{anidbid}"]'):
        if anime.attrib['defaulttvdbseason'] == 'a':
            # CANNOT HANDLE ABSOLUTE EPISODES MATCHING
            for map in anime.findall(f'./mapping-list/mapping/[@anidbseason="1"]'):
                if not map.text == None:
                    l = map.text.split(";")
                    for eps in l[1:-1] :
                        eps = eps.split("-")
                        if int(eps[0]) == episode:
                            return int(anime.attrib['tvdbid']), int(map.attrib['tvdbseason']), int(eps[1])
                if 'start' in map.attrib:
                    if int(map.attrib['start']) <= episode <= int(map.attrib['end']) :
                        return int(anime.attrib['tvdbid']), int(map.attrib['tvdbseason']), (episode + int(map.attrib['offset']))            
        elif int(anime.attrib['defaulttvdbseason']) > 0:
            # IGNORE SPECIALS
            for map in anime.findall(f'./mapping-list/mapping/[@anidbseason="1"]'):
                if not map.text == None:
                    l = map.text.split(";")
                    for eps in l[1:-1] :
                        eps = eps.split("-")
                        if int(eps[0]) == episode:
                            return int(anime.attrib['tvdbid']), int(map.attrib['tvdbseason']), int(eps[1])
                if 'start' in map.attrib:
                    if int(map.attrib['start']) <= episode <= int(map.attrib['end']) :
                        return int(anime.attrib['tvdbid']), int(map.attrib['tvdbseason']), (episode + int(map.attrib['offset']))
            if 'episodeoffset' in anime.attrib:
                return int(anime.attrib['tvdbid']), int(anime.attrib['defaulttvdbseason']), episode + int(anime.attrib['episodeoffset'])
            else:
                return int(anime.attrib['tvdbid']), int(anime.attrib['defaulttvdbseason']), episode


def tvdbToAnidb(tvdbid, season, episode, absepisode):
    """Convert the Tvdb anime info into Anidb info

    Args:
        tvdbid (int): TvdbID of the anime
        season (int): Tvdb season
        episode (int): Tvdb episode
        absepisode (int): Tvdb absolute episode

    Returns:
        anidbid: Corresponding AnidbID of the anime
        episode: Anime episode in Anidb
    """

    #getAnimeList()
        
    getScudLee()
    tree = ET.parse(filepath)
    root = tree.getroot()

    animelist = []

    # DO NOT HANDLE SPECIALS
    # Future work
    if season == 0:
        return 0,episode

    #search anime by TvdbID
    for anime in root.findall(f'./*[@tvdbid="{tvdbid}"]') :
        animelist.append(anime)

    for anime in reversed(animelist):
        # Check if season has absolute episode
        if anime.attrib['defaulttvdbseason'] == 'a':
            if 'episodeoffset' in anime.attrib:
                if absepisode > int(anime.attrib['episodeoffset']) :
                    return int(anime.attrib['anidbid']), (absepisode - int(anime.attrib['episodeoffset']))
            else:
                return int(anime.attrib['anidbid']), absepisode
        
        # Search for corresponding season
        if anime.attrib['defaulttvdbseason'] == f'{season}':
            # Calculate episode offset
            if 'episodeoffset' in anime.attrib:
                if episode > int(anime.attrib['episodeoffset']) :
                    return int(anime.attrib['anidbid']), (episode - int(anime.attrib['episodeoffset']))
            else:
                # Episode is the same as TvDB
                return int(anime.attrib['anidbid']), episode
        
        # If there is mapping information for the season
        for map in anime.findall(f'./mapping-list/mapping/[@tvdbseason="{season}"]') :
            # First check if there is individual episode mapping for the Episode
            if not map.text == None:
                l = map.text.split(";")
                for eps in l[1:-1] :
                    eps = eps.split("-")
                    if int(eps[1]) == episode:
                        return  int(anime.attrib['anidbid']), eps[0]
            # Second - check if the episode is between the [start, end] and calculate with the offset
            if 'start' in map.attrib:
                if (int(map.attrib['start']) + int(map.attrib['offset'])) <= episode <= (int(map.attrib['end']) + int(map.attrib['offset'])):
                    return int(anime.attrib['anidbid']), (episode - int(map.attrib['offset']))
    return 0,episode



# anidbToTvdb(anidbid, episode)
print (anidbToTvdb(10760,10))

# tvdbToAnidb(tvdbid, season, episode, absepisode)
print (tvdbToAnidb(321209, 1, 9, 9))
# getAnimeList()
# print ( tvdbToAnidb (114801, 3, 16, 112) )