"""Restore the six original datasets from verified GitHub Release parts.

Python 3.10+, standard library only. No credentials required for public release.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import urllib.request

REPO = 'Bear-Lan/sim_real_data'
TAG = 'dataset-20261006'
TASKS = ('Adjust_Bottle', 'Grab_Roller', 'Stack_Bowls_Two')


def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'sim-real-data-downloader'})
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.load(response)


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8*1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def get_file(url, target, expected_hash):
    if target.exists():
        if sha256(target) == expected_hash:
            return
        raise ValueError(f'Existing file has wrong checksum: {target}')
    partial = target.with_name(target.name+'.partial')
    req = urllib.request.Request(url, headers={'User-Agent': 'sim-real-data-downloader'})
    with urllib.request.urlopen(req, timeout=120) as response, partial.open('wb') as output:
        shutil.copyfileobj(response, output, length=4*1024*1024)
    if sha256(partial) != expected_hash:
        raise ValueError(f'Checksum mismatch: {partial}')
    partial.rename(target)


def extract_safe(archive, target):
    target.mkdir(parents=True, exist_ok=True)
    resolved = target.resolve()
    with tarfile.open(archive, 'r|gz') as tar:
        for member in tar:
            path = target/member.name
            if not path.resolve().is_relative_to(resolved) or not (member.isfile() or member.isdir()):
                raise ValueError(f'Unsafe archive member: {member.name}')
            if member.isdir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                if path.exists():
                    raise FileExistsError(f'Refusing to overwrite: {path}')
                with tar.extractfile(member) as source, path.open('wb') as output:
                    shutil.copyfileobj(source, output, length=1024*1024)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--task', choices=TASKS)
    args = parser.parse_args()
    release = fetch_json(f'https://api.github.com/repos/{REPO}/releases/tags/{TAG}')
    assets = {a['name']: a for a in release['assets']}
    manifest = fetch_json(assets['release_manifest.json']['browser_download_url'])
    if manifest['status'] != 'verified_complete':
        raise ValueError('Release has not passed completion checks')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    cache = output/'.downloads'
    cache.mkdir(exist_ok=True)
    for group in manifest['groups']:
        if group['kind'] != 'metadata' and args.task and group['task'] != args.task:
            continue
        target = output if group['kind'] == 'metadata' else output/group['kind']/group['task']
        marker = cache/(group['name']+'.restored.json')
        if marker.exists():
            print(f"Already restored: {group['name']}", flush=True)
            continue
        archive = cache/(group['name']+'.tar.gz')
        if not archive.exists():
            h = hashlib.sha256()
            with archive.with_name(archive.name+'.partial').open('wb') as combined:
                for part in group['parts']:
                    print(f"Downloading {part['name']} ({part['bytes']/1024**3:.2f} GiB)", flush=True)
                    local = cache/part['name']
                    get_file(assets[part['name']]['browser_download_url'], local, part['sha256'])
                    with local.open('rb') as f:
                        for block in iter(lambda: f.read(4*1024*1024), b''):
                            combined.write(block)
                            h.update(block)
                    local.unlink()  # Only this script's checksum-verified temporary download.
            if h.hexdigest() != group['sha256']:
                raise ValueError('Combined archive checksum mismatch')
            archive.with_name(archive.name+'.partial').rename(archive)
        elif sha256(archive) != group['sha256']:
            raise ValueError('Existing archive checksum mismatch')
        print(f"Extracting {group['name']}", flush=True)
        extract_safe(archive, target)
        marker.write_text(json.dumps({'sha256':group['sha256'],'target':str(target)}))
        archive.unlink()  # Raw extracted data remains; only verified temporary archive is removed.
    print(f'Finished: {output}', flush=True)


if __name__ == '__main__':
    main()
