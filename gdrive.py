import httplib2
from apiclient import discovery
from googleapiclient.http import MediaFileUpload

GDRIVE_FOLDER_MIME = 'application/vnd.google-apps.folder'
GDRIVE_SPACE = 'drive'


class GDrive(object):
    def __init__(self, authorisation):
        self.authorisation = authorisation

    def get_client(self):
        credentials = self.authorisation.get_credentials()
        http = credentials.authorize(httplib2.Http())
        return discovery.build('drive', 'v3', http=http)

    def get_unique_id(self):
        ids = self.get_client() \
            .files().generateIds(count=1, space=GDRIVE_SPACE, fields='ids').execute()
        return ids.get('ids')[0]

    def find_folder(self, name):
        page_token = None

        while True:
            folders = self.get_client() \
                .files() \
                .list(q="mimeType='" + GDRIVE_FOLDER_MIME + "' and name='" + name + "' and trashed=false",
                      spaces=GDRIVE_SPACE,
                      fields='nextPageToken, files(id)',
                      pageToken=page_token).execute()
            files = folders.get('files', [])

            if len(files) > 0:
                return files[0]['id']

            page_token = folders.get('nextPageToken', None)

            if page_token is None:
                break

        return False

    def create_folder(self, name):
        folder_metadata = {
            'name': name,
            'mimeType': GDRIVE_FOLDER_MIME
        }

        folder = self.get_client().files().create(body=folder_metadata, fields='id').execute()

        if not folder:
            return False

        return folder.get('id')

    def resume_file_upload(self, file_name, file_path, remote_folder, mime_type):

        metadata = {
            "id": self.get_unique_id(),
            "name": file_name,
            "parents": [remote_folder]
        }

        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        file = self.get_client(). \
            files(). \
            create(body=metadata, media_body=media, fields='id').execute();

        if not file:
            raise ValueError('Backup file (' + file_name + ') has failed to upload to Google Drive')

        return file.get('id')



