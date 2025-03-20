import os
import zipfile
import tarfile
import gzip
import shutil
import rarfile
from py7zr import SevenZipFile
from typing import List


def is_compressed(filename) -> bool:
    """Verifica se o arquivo é de um tipo compactado suportado."""
    compressed_types = ['.zip', '.tar', '.gz', '.bz2', '.7z', '.rar']
    return any(filename.endswith(ext) for ext in compressed_types)

def list_zip(filename) -> List[str]:
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        return [file for file in zip_ref.namelist() if not file.endswith('/')]

def list_tar(filename) -> List[str]:
    with tarfile.open(filename, 'r:*') as tar_ref:
        return [file for file in tar_ref.getnames() if tar_ref.getmember(file).isfile()]

def list_gzip(filename) -> List[str]:
    with gzip.open(filename, 'rb') as f_in:
        with open('temp_file', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        files = os.listdir('.')
        os.remove('temp_file')
        return files

def list_7zip(filename) -> List[str]:
    with SevenZipFile(filename, 'r') as archive:
        return [file.filename for file in archive.getmembers() if not file.filename.endswith('/')]

def list_rar(filename) -> List[str]:
    with rarfile.RarFile(filename) as rf:
        return [file for file in rf.namelist() if not file.endswith('/')]

def list(filename) -> List[str]:
    """Lista todos os arquivos de um arquivo compactado."""
    if not is_compressed(filename):
        return []
    elif filename.endswith('.tar') or filename.endswith('.tar.gz') or filename.endswith('.tar.bz2'):
        return list_tar(filename)
    elif filename.endswith('.zip'):
        return list_zip(filename)
    elif filename.endswith('.gz'):
        return list_gzip(filename)
    elif filename.endswith('.7z'):
        return list_7zip(filename)
    elif filename.endswith('.rar'):
        return list_rar(filename)
    else:
        return []

def test(filename= 'exemplo.rar'):
    files = list(filename)
    if files:
        print(f"Arquivos no {filename}:")
        for file in files:
            print(file)

