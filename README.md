# SimplePythonRedis

A small Redis-like server in Python, following along with [Building a simple Redis server with Python](https://charlesleifer.com/blog/building-a-simple-redis-server-with-python/) by Charles Leifer.

Uses `gevent` for concurrent connections and implements a basic RESP-style protocol and in-memory key/value store.

## Install

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --group dev
```

## Run

Start the server:

```bash
.venv/bin/python main.py
```

In another terminal, use the client:

```bash
.venv/bin/python
```

```python
>>> from main import Client
>>> client = Client()
>>> client.mset("k1", "v1", "k2", ["v2-0", 1, "v2-2"], "k3", "v3")
3
>>> client.get("k2")
[b'v2-0', 1, b'v2-2']
```

## Test

```bash
.venv/bin/pytest -q
```
