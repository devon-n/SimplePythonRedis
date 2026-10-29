from io import BytesIO

import gevent
import pytest
from gevent import monkey

monkey.patch_all()

from main import Client, ProtocolHandler, Server


def test_protocol_roundtrip():
    p = ProtocolHandler()
    buf = BytesIO()
    p._write(buf, ["MSET", "k1", "v1", "k2", [1, "x"]])
    buf.seek(0)
    assert p.handle_request(buf) == [b"MSET", b"k1", b"v1", b"k2", [1, b"x"]]


@pytest.fixture
def client():
    server = Server(port=0)
    greenlet = gevent.spawn(server.run)
    while not server._server.started:
        gevent.sleep(0.01)
    host, port = server._server.address
    c = Client(host, port)
    yield c
    server._server.stop()
    greenlet.kill()


def test_kv_smoke(client):
    assert client.mset("k1", "v1", "k2", ["v2-0", 1, "v2-2"], "k3", "v3") == 3
    assert client.get("k2") == [b"v2-0", 1, b"v2-2"]
    assert client.mget("k3", "k1") == [b"v3", b"v1"]
    assert client.delete("k1") == 1
    assert client.get("k1") is None
    assert client.flush() == 2
