import importlib.metadata
import json


pkg_name = 'mylib'


def get_version():
    D = next(json.loads(p.read_text())
            for p in importlib.metadata.distribution(pkg_name).files()
            if p.name == 'direct_url.json')
    return D
