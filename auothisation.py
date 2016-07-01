import os
import oauth2client

SCOPES = 'https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = 'config/client_secret.json'
APPLICATION_NAME = 'gdrive-mysql-backup-service'
CREDENTIAL_FILE = 'gdrive-credentials.json'


class Authorisation(object):

    def __init__(self, cmd):
        self.cmd = cmd

    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')

        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

        credential_path = os.path.join(credential_dir, CREDENTIAL_FILE)

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        cmd_flags = self.cmd.get_arguments()

        if not credentials or credentials.invalid:
            flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME

            if cmd_flags:
                credentials = oauth2client.tools.run_flow(flow, store, cmd_flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = oauth2client.tools.run(flow, store)

            print('Storing credentials to ' + credential_path)

        return credentials
