# python-library-template

This template focus on developmemt of internal Python package,
in such case the package description is not important.

----

To install:
```
pip install git+https://github.com/apua/python-library-template@dev#subdirectory=mylib
```

To re-install:
```
pip install --force-reinstall git+https://github.com/apua/python-library-template@dev#subdirectory=mylib
```

Uninstall all:
```
pip freeze | xargs pip uninstall -y
```

Ref:

+ https://pip.pypa.io/en/stable/cli/pip_install/
+ https://pip.pypa.io/en/stable/cli/pip_install/#examples

----

Full version information in installed environment:
```
jq . venv/lib/python*/site-packages/mylib-*.dist-info/direct_url.json
{
  "subdirectory": "mylib",
  "url": "https://github.com/apua/python-library-template",
  "vcs_info": {
    "commit_id": "d59783483d287fa61aa7eec789da5635b7717249",
    "requested_revision": "dev",
    "vcs": "git"
  }
}
```

Ref:

+ https://packaging.python.org/specifications/direct-url

In Python, perhaps... :
```python
>>> import pkg_resources
>>> mylib = pkg_resources.get_distribution('mylib')
>>> mylib.egg_info
'/private/tmp/yyyy/venv/lib/python3.9/site-packages/mylib-0.1.dist-info'
```

In Python ≧ 3.10:
```python
>>> import importlib.metadata
>>> dist = importlib.metadata.distribution('mylib')
>>> dist.files
[PackagePath('mylib-0.1.dist-info/INSTALLER'), PackagePath('mylib-0.1.dist-info/METADATA'), PackagePath('mylib-0.1.dist-info/RECORD'), PackagePath('mylib-0.1.dist-info/REQUESTED'), PackagePath('mylib-0.1.dist-info/WHEEL'), PackagePath('mylib-0.1.dist-info/direct_url.json'), PackagePath('mylib-0.1.dist-info/top_level.txt'), PackagePath('mylib/__init__.py'), PackagePath('mylib/__pycache__/__init__.cpython-310.pyc')]
>>> D = next(json.loads(d.read_text()) for p in dist.files if p.name == 'direct_url.json')
>>> D
'subdirectory': 'mylib', 'url': 'https://github.com/apua/python-library-template', 'vcs_info': {'commit_id': 'd59783483d287fa61aa7eec789da5635b7717249', 'requested_revision': 'dev', 'vcs': 'git'}}
```

Ref:

+ https://docs.python.org/3/library/importlib.metadata.html#distribution-files

----

See also:

+ https://github.com/apua/mylib


## pyproject.toml

Let pip takes default build backend `setuptools`.

Ref:

+ https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/#fallback-behaviour

----

Take "src-layout".

Ref:

+ https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout

----

List dependencies directly, instead of from file as following:
```toml
[project]
dynamic = ["dependencies", "optional-dependencies"]

[tool.setuptools.dynamic]
dependencies = { file = ["requirements.txt"] }
optional-dependencies = { tests = { file = ["test_requirements.txt"] } }
```

To install dependencies only, remove itself after installing.

To install with optional dependencies, declare package name:
```
pip install --force-reinstall mylib[test]@git+https://github.com/apua/python-library-template@dev#subdirectory=mylib
```

Ref:

+ https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#dynamic
+ https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html#dynamic-metadata

----

We don't create commands from `[project.scripts]` automatically.
In our case (eg: `module load`), an executable maintaines its own venv,
thus the executable always outside from the Python package.

`[project.scripts]` is `[project.entry-points.console_scripts]`.

`[project.entry-points."..."]` is not "entry points for CLI".
Instead, it is metadata read by `importlib.metadata`.

```toml
# [project]
# entry-points = {'my.group' = {mykey = 'myvalue'}}

[project.entry-points.'my.group']
mykey = 'myvalue'
```

```python
>>> from importlib.metadata import entry_points
>>> entry_points(group='my.group')
[EntryPoint(name='mykey', value='myvalue', group='my.group')]
```

Ref:

+ https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#entry-points
+ https://packaging.python.org/en/latest/specifications/entry-points/#entry-points
+ https://docs.python.org/3/library/importlib.metadata.html#entry-points
