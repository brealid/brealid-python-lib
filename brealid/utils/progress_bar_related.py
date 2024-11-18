import os
try:
    from tqdm import tqdm
except ImportError:
    raise ImportError('package `tqdm` should be installed!')

def download(url, filename, desc=None):
    """
    从给定的 URL 下载文件，并将其保存为 filename。
    使用 tqdm 显示下载进度条。
    """
    try:
        import requests
    except ImportError:
        raise ImportError('package `requests` should be installed!')
    if desc is None:
        desc = f'Downloading from {url}'
    # 获取文件大小
    response = requests.head(url)
    file_size = int(response.headers.get('content-length', 0))
    
    # 下载文件并显示进度条
    with requests.get(url, stream=True) as r, open(filename, 'wb') as file, tqdm(
        desc=desc,
        total=file_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in r.iter_content(chunk_size=100000):
            file.write(chunk)
            bar.update(len(chunk))

def unzip(zip_path, extract_to, desc=None):
    try:
        import zipfile
    except ImportError:
        raise ImportError('package `zipfile` should be installed!')
    if desc is None:
        desc = f'Extracting from {url}'
    # 打开 ZIP 文件
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # 获取文件列表
        files = zip_ref.namelist()
        
        # 创建解压目标文件夹（如果不存在）
        os.makedirs(extract_to, exist_ok=True)
        
        # 使用 tqdm 显示解压进度条
        with tqdm(total=len(files), desc=desc, unit="file") as pbar:
            for file in files:
                zip_ref.extract(file, extract_to)
                pbar.update(1)  # 更新进度条