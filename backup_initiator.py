from cmd import Cmd
from auothisation import Authorisation
from gdrive import GDrive
from backup import Backup

if __name__ == '__main__':
    cli = Cmd()
    authorisation = Authorisation(cli)
    gdrive = GDrive(authorisation)
    backup = Backup(cli, gdrive)
    backup.backup()
