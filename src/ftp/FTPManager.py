import paramiko
from src.data_bank_functions.file_for_internal_usage import sftpHost, sftpPW, sftpUser


def check_for_new_data():
    """
    Function that establishes a SSH connection to a SFTP-server which is then used to download data from the SFTP Server
    when there is no new data nothing will be downloaded if there is new data the function will provide a list of all
    the files that are new and download them to the res repository. The downloaded files will be moved to another
    repository to be reused if something went wrong.

    Returns: A List of files_to_fetch if there is new data or a empty list if there is no data

    """
    # Hinzufügen des passenden Passwort und Username aus /src/data_bank_functions/file_for_internal_usage.py
    host, port = sftpHost, 22
    username, password = sftpUser, sftpPW

    # Verbindungsaufbau zu SFTP Server per SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    # Berechne Anzahl der Dokumente in Ordner Speiseplandaten
    stdin, stdout, stderr = ssh.exec_command('ls Speiseplandaten | wc -l')
    number_of_files_in_dir = int(stdout.read().decode())
    print(number_of_files_in_dir)

    # Falls es neue Dokumente gibt
    if number_of_files_in_dir > 0:
        # öffne sftp session
        sftp = ssh.open_sftp()

        # Name der Dokumente im Ordner
        files_to_fetch = sftp.listdir('/Speiseplandaten')
        print(files_to_fetch)

        # Download der neuen Files & verschieben der Files in Done Ordner
        for file in files_to_fetch:
            sftp.get('/Speiseplandaten/' + file, 'res\\' + file)
            sftp.rename('/Speiseplandaten/' + file, '/Done/' + file)

        sftp.close()
        ssh.close()
        # wird später mit XML Reader eingelesen und in Datenbank gespeichert
        return files_to_fetch
    else:
        return []  # wenn es keine neuen Dateien gibt soll eine leere Liste zurückgeben werden
