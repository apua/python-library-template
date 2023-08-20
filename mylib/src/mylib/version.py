import importlib.metadata
import json
import subprocess


def get_version() -> str | None:
    try:
        dist = importlib.metadata.distribution(__package__)
    except importlib.metadata.PackageNotFoundError:
        # The package itself is not installed.
        return None

    version = dist.version
    direct_url = next(json.loads(p.read_text()) for p in dist.files if p.name == 'direct_url.json')

    # Edit mode::
    #
    # {'dir_info': {'editable': True}, 'url': 'file:///.../mylib'}
    #
    # VCS mode::
    #
    # {'subdirectory': 'mylib',
    #  'url': 'https://github.com/apua/python-library-template',
    #  'vcs_info': {
    #    'commit_id': '3efcda4ddcf972eda79c0a6eb13dd4fc286aba89',
    #    'requested_revision': 'dev',
    #    'vcs': 'git'}}
    if direct_url['url'].startswith('file:///'):
        # Edit mode.
        proc = subprocess.run('git rev-parse HEAD', shell=True, capture_output=True, check=True)
        sha = proc.stdout.decode().strip()
        return f'{version}-{sha[:7]}'
    else:
        # VCS mode.
        if direct_url['vcs_info']['requested_revision'] == 'release':
            return version
        else:
            sha = direct_url['vcs_info']['commit_id']
            return f'{version}-{sha[:7]}'
