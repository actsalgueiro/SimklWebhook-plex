from github import Github
import os
import time
import xml.etree.ElementTree as ET
from urllib import request

filePath = os.path.abspath("anime-list.xml")

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

    # create element tree object
    tree = ET.parse(filePath)
    root = tree.getroot()

    animelist = []

    # DO NOT HANDLE SPECIALS
    if season == 0:
        return

    #search anime by TvdbID
    for anime in root.findall(f'./*[@tvdbid="{tvdbid}"]') :
        #print(f"{anime.attrib}")
        animelist.append(anime)

    for anime in reversed(animelist):
        # Check if season has absolute episode
        if anime.attrib['defaulttvdbseason'] == 'a':
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
            #print (map.attrib)
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

def getAnimeList():
    """Download anime-list.xml file from the GitHub rep if there were any changes
    """

    if not os.path.exists(filePath) :
        remote_url = 'https://raw.githubusercontent.com/Anime-Lists/anime-lists/master/anime-list.xml'
        # Define the local filename to save data
        local_file = 'anime-list.xml'
        # Download remote and save locally
        request.urlretrieve(remote_url, local_file)
        return

    g = Github()
    repo = g.get_repo("Anime-Lists/anime-lists")
    commits = repo.get_commits(path='anime-list.xml')
    # Get last commit date of the file
    if commits.totalCount:
        gitDate = time.strptime(str(commits[0].commit.committer.date).split(None, 1)[0], "%Y-%m-%d")
        #print("Last Commit Time: ", gitDate)
    
    # Get directory file date
    modificationTime = time.strptime(time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(filePath))), "%Y-%m-%d")
    #print("Last Modified Time : ", modificationTime )

    if gitDate > modificationTime:
        #print("New version found")
        # Define the remote file to retrieve
        remote_url = 'https://raw.githubusercontent.com/Anime-Lists/anime-lists/master/anime-list.xml'
        # Define the local filename to save data
        local_file = 'anime-list.xml'
        # Download remote and save locally
        request.urlretrieve(remote_url, local_file)