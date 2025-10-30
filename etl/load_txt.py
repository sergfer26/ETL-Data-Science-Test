import os

import paramiko

import argparse

import dotenv

from loguru import logger

dotenv.load_dotenv()

hostname = os.environ["hostname"] 
port = int(os.environ["port"])
username = os.environ["username"]
password = os.environ["password"]
remote_path = os.environ["remote_path"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    args = parser.parse_args()

    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the SFTP server
    ssh_client.connect(hostname, port, username, password)

    # Create an SFTP session
    sftp = ssh_client.open_sftp()
    
    local_file = args.file
    try:
        # Falta considerar caso de subdirectorios
        sftp.mkdir(remote_path) 
    except FileExistsError:
        logger.info(f"Remote directory {remote_path} already exists")
    remote_file = os.path.join(remote_path, os.path.basename(local_file))
    sftp.put(local_file, remote_file)

    # Close the SFTP session
    sftp.close()

    # Close the SSH connection
    ssh_client.close()