# SimklWebhook-plex
Update Simkl watched state via a Tautulli webhook (using [Shoko Metadata](https://shokoanime.com/) or plex TV series)

## Set up in Tautulli

1. Download the [Script](/Webhook.py)

2. In Tautulli go to **Settings > Notification Agents > Add a new Notification Agent > Script**

3. In the Script Settings
    - Configuration Tab
        - Script Folder: Select the folder path where the python file is saved
        - Script File: `Webhook.py`

    - Triggers Tab
        - Select  **Watched**

    - Conditions Tab
        - If you want to run the script for different plex users you must create a Notification Agent for each one and add the condition
            `User`  `is`  `[PLEX USERNAME]`

    - Arguments Tab
        - In the **Watched** dropdown add the script argument
        ` --guid {guid} --filename {filename} --tvdbid {thetvdb_id} --imdbid {imdb_id} --tmdbid {themoviedb_id} --season {season_num} --episode {episode_num} --username {username} --title {title} --show_name {show_name} --media_type {media_type} --year {year} --url [SIMKL WEBHOOK URL] `
        - You can get your [Simkl Webhook URL](https://simkl.com/apps/plex/), just copy the url and replace `[SIMKL WEBHOOK URL]`.
        ![Simkl Webhook URL Image](/simkl_webhook_url.png)

4. Save


## Known issues
* There is a limitation regarding some long running anime, because the scripts uses the absolute episode number and this information is not provided by PLEX. The solution is to rename the episode files and include `[abs-##]`, replacing **##** with the absolute episode number of that episode.

* The special episodes are not yet handled 


## Acknowledgments
* We use the [Anime List](https://github.com/Anime-Lists/anime-lists) to match the TvdbID with the corresponding AnidbID.
