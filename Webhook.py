import sys
import json
import requests
import argparse

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


def main(guid, username, title, show_name, media_type, year, url):

    webhookurl = url.replace("&amp;", "&")

    headers = {
        'Content-Type': 'application/json'
    }
    
    api_key = get_api_key()
    
    # parse the guid - com.plexapp.agents.shoko://1/1/1?lang=en
    if "shoko://" in guid:
        shokoID = guid.split('shoko://')[1].split('/')[0]
        season = guid.split('shoko://')[1].split('/')[1]
        episode = guid.split('shoko://')[1].split('/')[2].split('?')[0]
    if "hama://" in guid:
        andiDB_id = guid.split('hama://anidb-')[1].split('/')[0]
        season = guid.split('hama://')[1].split('/')[1]
        episode = guid.split('hama://')[1].split('/')[2].split('?')[0]
    
    # print("ID: %s Season: %s Episode: %s" % (shokoID, season, episode))

    # local api call for anidb info
    if "shoko://" in guid:
        url = 'http://' + shoko_data['host'] + ':' + shoko_data['port'] + f"/api/v3/Series/{shokoID}/AniDB?apikey={api_key}"
        request_data = requests.get(url)

        andiDB_id = json.loads(request_data.text)['ID']
    
    #print("Anidb-ID: ", andiDB_id)

    # construct payload
    payload = {"event":"media.scrobble","user":f"{username}", "Metadata":{ "title": f"{title}{show_name}","type":f"{media_type}","year": f"{year}","guid":f"/anidb-{andiDB_id}/{season}/{episode}/"} }

    response = requests.post(webhookurl, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        print( "Error: %s - %s" % (response.status_code, response.text))
    else:
        print("Success.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--guid', required=True)
    parser.add_argument('--username', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--show_name', required=True)
    parser.add_argument('--media_type', required=True)
    parser.add_argument('--year', required=True)
    parser.add_argument('--url', required=True)
    opts = parser.parse_args()

    main(opts.guid, opts.username, opts.title, opts.show_name, opts.media_type, opts.year, opts.url)

