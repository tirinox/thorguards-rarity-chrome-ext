"""
This script downloads metadata + thumbnail picture for each ThorGuard Gen0
"""
import asyncio
import json
import os

import aiofiles
import aiohttp
import tqdm

from config import Config
from convert_metadata import run_convert_metadata, load_all_meta_map_from_disk, convert_one_meta

cfg = Config()


async def fetch_json(session, url):
    async with session.get(url) as resp:
        if resp.status == 200:
            data = await resp.read()
            return json.loads(data)


async def download_file(session, url, target_path):
    async with session.get(url) as resp:
        if resp.status == 200:
            f = await aiofiles.open(target_path, mode='wb')
            await f.write(await resp.read())
            await f.close()


async def get_one_nft_meta_job(session, start, count, progress, meta_map: dict):
    cfg = Config()
    for i in range(start, min(start + count, cfg.N)):
        if str(i) not in meta_map:
            data = await fetch_json(session, url=cfg.url_for_metadata(i))
            meta_map[str(i)] = convert_one_meta(data)
        progress.update(1)


async def get_one_nft_pic_job(session, start, count, progress):
    for i in range(start, min(start + count, cfg.N)):
        local_path = cfg.path_for_thumb_pic(i)
        if not os.path.exists(local_path):
            await download_file(session, url=cfg.url_for_thumb_pic(i),
                                target_path=local_path)
        progress.update(1)


async def main():
    if cfg.DOWNLOAD_METADATA:
        os.makedirs(cfg.PATH_METADATA, exist_ok=True)

    if cfg.DOWNLOAD_IMAGES:
        os.makedirs(cfg.PATH_THUMB, exist_ok=True)

    progress = tqdm.tqdm(total=cfg.N)

    meta_storage = load_all_meta_map_from_disk(from_scratch=cfg.DOWNLOAD_FROM_SCRATCH)

    batch_size = cfg.DOWNLOAD_BATCH_SIZE
    async with aiohttp.ClientSession() as session:
        start = 1
        tasks = []
        while start < cfg.N:
            if cfg.DOWNLOAD_IMAGES:
                tasks.append(get_one_nft_pic_job(session, start, batch_size, progress))

            if cfg.DOWNLOAD_METADATA:
                tasks.append(get_one_nft_meta_job(session, start, batch_size, progress, meta_storage))

            start += batch_size

        await asyncio.gather(*tasks)

    print('Download finished!')

    run_convert_metadata(meta_storage)

    print('All done! You can now run query_r.py!')


if __name__ == '__main__':
    asyncio.run(main())
