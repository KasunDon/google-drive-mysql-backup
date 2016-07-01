from datetime import datetime
import json
import os

BACKUP_FOLDER='mysql-backup-service'
MYSQL_CONFIG='config/mysql-config.json'


class Backup(object):
    def __init__(self, cmd, gdrive):
        self.cmd = cmd
        self.gdrive = gdrive

    def create_backup_filename(self):
        return self.cmd\
                   .get_arguments()\
                   .backup_file_name + \
               '_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.sql'

    def get_mysql_connection_details(self):
        try:
            with open(MYSQL_CONFIG, 'r') as fp:
                return json.load(fp)
        except IOError as exc:
            raise ValueError('Error opening MySQL config file', exc.filename,
                             exc.strerror, exc.errno)
        return false

    def create_a_mysql_dump(self):
        dump_file = self.create_backup_filename()
        config = self.get_mysql_connection_details()

        print('Creating MySQL dump file (' + dump_file + ') for db:' + config.get('db') +
          ' - ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        command = 'mysqldump -h' + config.get('host') + \
              ' -P' + config.get('port') + \
              ' -u' + config.get('username')
        password = config.get('password')

        if password:
            command += ' -p"' + password + '"'

        temp_backup_location = '/tmp/' + dump_file

        command += ' ' + config.get('db') + ' > ' + temp_backup_location

        os.system(command)

        if os.path.exists(temp_backup_location) is False:
            raise ValueError('Failed to create backup file.')

        return {"file-name": dump_file, "path": temp_backup_location}

    def backup(self):
        backup = self.create_a_mysql_dump()
        folder_id = self.gdrive.find_folder(BACKUP_FOLDER)

        if folder_id is False:
            folder_id = self.gdrive.create_folder(BACKUP_FOLDER)
            print('Backup folder not found, created a new folder (ID:) ' + folder_id)
        else:
            print('Found existing backup folder (ID:) ' + folder_id)

        backup_file_path = backup.get('path')
        upload_status = self.gdrive.resume_file_upload(backup.get('file-name'), backup_file_path,
                                           folder_id, 'application/octet-stream')

        print('Backup file successfully uploaded to Google Drive (ID:) ' + upload_status)
        os.remove(backup_file_path)



