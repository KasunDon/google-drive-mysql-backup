# Google Drive - MySQL backup service
MySQL backup script uploads `mysqldump` files to Google Drive .

![alt tag](http://ckeinc.com/wp-content/uploads/2015/07/google-drive-logo-vector.png) ![alt tag](https://www.mysql.com/common/logos/logo-mysql-170x115.png)

# Prerequisites
* Python 2.6 or greater.
* `pip` python package management tool.
* A Google account with Google Drive enabled.

# Installation
    git clone git@github.com:KasunDon/google-drive-mysql-backup.git /opt/google-drive-mysql-backup
    
    cd /opt/google-drive-mysql-backup

    pip install -r requirements.txt

Also we need creating OAuth keys to access Google Drive API. Please use following steps,
* Sign into Google Developers Console and create or select a project in the [Google Developers Console](https://console.developers.google.com/iam-admin/projects).
* Enable **Google Drive API** under API Section.
* Go to **credentials**.
* Go to **OAuth consent screen** tab. Select an Email address, enter a Product name and other information.
* Go to **Credentials tab**, click the Create credentials button and select **OAuth client ID**.
* Select the application type **Other** and set application name.
* Download credential as a **JSON** file
* Place downloaded credential file  as `config/client_secret.json`.

MySQL connection details should also added to `config/mysql-config.json`

# Authorising Backup service
When running backup service for first time it should be authorised with Google API's. There are two ways to authorise backup service.

1. Brower based authorisation, following command will launch up browser window for authorisation

        python backup_initiator.py

2. Server-side authorisation, following command will show up a URL for manual authorisation. Copy the URL from the console and manually open it in your browser.Once authorised verfication code should be added.

        python backup_initiator.py --noauth_local_webserver         

# Running backup service
Use following command to list help options.

    python backup_initiator.py -h 

[![asciicast](https://asciinema.org/a/1v7d53zyly5hzth6ngrj447yi.png)](https://asciinema.org/a/1v7d53zyly5hzth6ngrj447yi)

If you need specific file name **prefix** for backup files use following command.

    python backup_initiator.py --backup-file-name "myblog_mysql-backup" 