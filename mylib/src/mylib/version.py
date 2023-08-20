import importlib.metadata
import json


def get_version():
    D = next(json.loads(p.read_text())
            for p in importlib.metadata.distribution(__package__).files
            if p.name == 'direct_url.json')
    return D
