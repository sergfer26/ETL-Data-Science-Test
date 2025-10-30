import os
import dotenv
import zipfile
import paramiko

from loguru import logger
from datetime import datetime

dotenv.load_dotenv()

hostname = os.environ["hostname"] 
port = int(os.environ["port"])
username = os.environ["username"]
password = os.environ["password"]
remote_path = os.environ["remote_path"]
local_path = os.environ["local_path"]


def zip_file(file_name: str):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    os.makedirs(local_path, exist_ok=True)
    with zipfile.ZipFile(f'{local_path}/backup_{timestamp}.zip', 'a') as zipf:
        zipf.write(file_name, os.path.basename(file_name))


def retrieve_txt_files():
    # Create an SSH client
    ## Suggested approach by Claude
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_client.connect(hostname, port, username, password)
    sftp = ssh_client.open_sftp()
    txt_files = []
    try:
        for file in sftp.listdir(remote_path):
            if file.endswith('.txt'):
                try:
                    sftp.get(os.path.join(remote_path, file), os.path.join(local_path, file))
                    sftp.remove(os.path.join(remote_path, file))
                    txt_files.append(file)
                    zip_file(file)
                    logger.info(f"[*] Successfully downloaded and deleted {file}")
                except Exception as e:
                    logger.error(f"[!] Error processing {file}: {e}")
    finally:
        sftp.close()
        ssh_client.close()
    
    return txt_files