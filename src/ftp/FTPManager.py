#TODO: implementation of class FTPConnector
import paramiko

client = paramiko.sshClient()

client.connect('ftp.mensaskill.de',port=22,username = 'u106517548-python', password='!python?')