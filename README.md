# SimklWebhook-plex
Update Simkl watched state via a Tautulli webhook (using Shoko Metadata or plex TV series)

## Set up in Tautulli

1. Save the [Script](/Webhook.py)

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
        - You can get your [Simkl Webhook URL](https://simkl.com/apps/plex/), just copy the url and add it at the end of the arguments
        ![Simkl Webhook URL Image](/simkl_webhook_url.png)

4. Save