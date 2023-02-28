# owners

CLI tool to inspect [CODEOWNERS](https://docs.gitlab.com/ee/user/project/code_owners.html) files: show unowned and owned directories, get owned paths for a user, find owners for a given path.

## Installation

```bash
python3 -m pip install owners
```

## Usage

Show paths owned by the given user or group:

```bash
python3 -m owners owned-by @some-user-name
```

Show owners of the given file or directory:

```bash
python3 -m owners owners-of some/local/path
```

Print a colorful tree of all directories and their owners:

```bash
python3 -m owners tree
```
