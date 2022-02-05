# SimklWebhook-plex
Update Simkl watched state via a Tautulli webhook (using Shoko Metadata or plex TV series)

## Set up in Tautulli

1. Save the `Webhook.py` script

2. In Tautulli go to **Settings > Notification Agents > Add a new Notification Agent > Script**

3. In the Script Settings
    - Configuration Tab
        - Script Folder: Select the folder path where the python file is saved
        - Script File: `Webhook.py`

    - Triggers Tab
        - Select  **Watched**

    - Conditions Tab
        - If you want to run the script for different plex users you must create a Notification Agent for each one and add the condition
            `User is [PLEX USERNAME]`

4. Save