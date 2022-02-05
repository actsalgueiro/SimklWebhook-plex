import sys
import json
import requests
import argparse
import logging
import re
from anidb_match import tvdbToAnidb

logging.basicConfig(filename='webhook.log', filemode='w', encoding='utf-8', level=logging.INFO)

shoko_data = {
    'host': '127.0.0.1',
    'port': '8111',
    'username': 'Default',
    'password': ''
}

def get_api_key():
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'user': shoko_data['username'],
        'pass': shoko_data['password'],
        'device': 'simkl-scrobble'
    }

    url = 'http://' + shoko_data['host'] + ':' + shoko_data['port'] + '/api/auth'

    request_data = json.loads(requests.post(url, headers=headers, data=json.dumps(payload)).text)

    return request_data['apikey']


def main(guid, filename, tvdbid, imdbid, tmdbid, episode, season, username, title, show_name, media_type, year, url):

    logging.info(f"\n guid: {guid}\n filename: {filename}\n tvdbid: {tvdbid}\n imdbid: {imdbid}\n tmdbid: {tmdbid}\n episode: {episode}\
        \n season: {season}\n username: {username}\n title: {title}\n show_name: {show_name}\n media_type: {media_type}\n year: {year}\n url: {url}\n")

    webhookurl = url.replace("&amp;", "&")

    headers = {
        'Content-Type': 'application/json'
    }

    anidbid = 0

    logging.info(f"guid: {guid}")
    if "shoko://" in guid:
        # example guid - com.plexapp.agents.shoko://1/1/1?lang=en
        shokoID = guid.split('shoko://')[1].split('/')[0]
        season = guid.split('shoko://')[1].split('/')[1]
        episode = guid.split('shoko://')[1].split('/')[2].split('?')[0]

        api_key = get_api_key()
    # if "hama://" in guid:
    #     andiDB_id = guid.split('hama://anidb-')[1].split('/')[0]
    #     season = guid.split('hama://')[1].split('/')[1]
    #     episode = guid.split('hama://')[1].split('/')[2].split('?')[0]
    if "plex://" in guid: 
        # example 'Show Title (year) - SXXEXX - Episode Name [abs-XX][SOURCE-QUALITY-GROUP].mkv'
        if filename != None:
            if 'abs-' in filename:
                # absepisode = filename.split('[')[1].split('-')[1][:-1]
                absepisode = re.search(r"(?<=\[)abs-[0-9]+?(?=\])", filename).group().split('-')[1]
            else:
                absepisode = 0
        logging.info(f"abs: {absepisode}")
        logging.info(f"{int(tvdbid)}, {int(season)}, {int(episode)}, {int(absepisode)}")
        anidbid, episode = tvdbToAnidb(int(tvdbid), int(season), int(episode), int(absepisode))
            
        
    # print("ID: %s Season: %s Episode: %s" % (shokoID, season, episode))

    # local api call for anidb info
    if "shoko://" in guid:
        url = 'http://' + shoko_data['host'] + ':' + shoko_data['port'] + f"/api/v3/Series/{shokoID}/AniDB?apikey={api_key}"
        request_data = requests.get(url)

        aniDB_id = json.loads(request_data.text)['ID']
    
    # prepare IDs
    imdbid = f"/imdb-{imdbid}" if imdbid != None else ""
    tmdbid = f"/themoviedb-{tmdbid}" if tmdbid != None else ""
    tvdbid = f"/thetvdb-{tvdbid}" if tvdbid != None else ""
    anidbid = f"/anidb-{anidbid}" if anidbid > 0 else ""
    # construct payload

    # payload = {"event":"media.scrobble","user":f"{username}", "Metadata":{ "title": f"{title}{show_name}","type":f"{media_type}","year": f"{year}","guid":f"{imdbid}{tmdbid}{tvdbid}{anidbid}/{season}/{episode}/"} }
    payload = {
        "event":"media.scrobble",
        "user":f"{username}", 
        "Metadata":
        { 
            "title": f"{title}{show_name}",
            "type":f"{media_type}",
            "year": f"{year}",
            "guid":f"{imdbid}{tmdbid}{tvdbid}{anidbid}/{season}/{episode}/"
        } 
    }

    logging.info (payload)
    response = requests.post(webhookurl, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        logging.debug( "Error: %s - %s" % (response.status_code, response.text))
    else:
        logging.debug("Success.")
        return 0
    return -1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--guid', required=True)
    parser.add_argument('--filename', required=True)
    parser.add_argument('--tvdbid', required=True)
    parser.add_argument('--imdbid', required=False)
    parser.add_argument('--tmdbid', required=False)
    parser.add_argument('--episode', required=True)
    parser.add_argument('--season', required=True)
    parser.add_argument('--username', required=False)
    parser.add_argument('--title', required=False)
    parser.add_argument('--show_name', required=False)
    parser.add_argument('--media_type', required=True)
    parser.add_argument('--year', required=False)
    parser.add_argument('--url', required=True)
    opts = parser.parse_args()

    main(opts.guid, opts.filename, opts.tvdbid, opts.imdbid, opts.tmdbid, opts.episode, opts.season, opts.username, opts.title, opts.show_name, opts.media_type, opts.year, opts.url)

