#TODO: implementation of class FTPConnector
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect()

sftp = ssh.open_sftp()
sftp.put('test.txt','upload.txt')
sftp.get("speiseplanstw.xml","download.xml")
sftp.close()

ssh.close()