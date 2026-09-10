#!/usr/bin/env python3
"""Public companion tools for an installed Amos / ComfyUI AutoDL image."""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.request


def roots():
    return Path(os.environ.get('AMOS_ROOT', '/root/amos-cloud-r42')), Path(os.environ.get('COMFY_ROOT', '/root/ComfyUI'))


def report(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def doctor():
    amos, comfy = roots()
    files = {'comfy_main': (comfy / 'main.py').is_file(), 'amos_runtime': (amos / 'amos-workbench').is_file(), 'amos_start': (amos / 'autodl-start.sh').is_file(), 'signed_manifest': (amos / 'release-manifest.sig').is_file()}
    versions = {}
    for package in ('torch', 'sageattention', 'comfy-kitchen'):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = 'not installed'
    ok = all(files.values())
    report({'success': ok, 'python': sys.version.split()[0], 'files': files, 'packages': versions, 'note': 'File presence is not signature verification or GPU acceptance.'})
    return 0 if ok else 1


def smoke():
    results = {}
    for label, address in (('workbench', 'http://127.0.0.1:6008/api/health'), ('comfy_or_no_gpu_page', 'http://127.0.0.1:6006/')):
        try:
            with urllib.request.urlopen(address, timeout=5) as response:
                body = response.read(65536)
                ok = response.status == 200
                if label == 'workbench':
                    health = json.loads(body)
                    ok = ok and health.get('status') == 'ok' and health.get('service') == 'amos-cloud-runtime'
                results[label] = {'success': ok, 'http': response.status}
        except Exception as error:
            results[label] = {'success': False, 'error': str(error)}
    report(results)
    return 0 if all(item['success'] for item in results.values()) else 1


def start():
    amos, _ = roots()
    entry = amos / 'autodl-start.sh'
    if not entry.is_file():
        report({'success': False, 'error': 'Installed image runtime is missing. This repository is not the complete runtime installer.'})
        return 1
    # The installed boot chain retains the release signature verification.
    return subprocess.call(['bash', str(entry)], cwd=amos)


def self_test():
    assert callable(doctor) and callable(smoke)
    amos, comfy = roots()
    assert isinstance(amos, Path) and isinstance(comfy, Path)
    report({'success': True, 'test': 'companion-cli', 'gpu_used': False, 'network_used': False, 'environment_modified': False})
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['doctor', 'smoke', 'start', 'self-test'])
    args = parser.parse_args()
    raise SystemExit({'doctor': doctor, 'smoke': smoke, 'start': start, 'self-test': self_test}[args.command]())
