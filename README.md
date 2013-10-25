sjson
=====

A library for transfer a Stream of JSONs

## Example

### Server

```python
import socket
from sjson import SJSON, CMD

port = 9090

print socket.gethostname(), port

server_sjson = SJSON()
(client, address) = server_sjson.bind((socket.gethostname(), port))
client.send({"hello": "world"})
client.send(1j + 1)
client.send(1)
client.send(1.1)
client.send("1")
client.send(["1"])
client.send(None)
client.send(CMD("ACK"))
client.send(CMD("ERROR"))
client.send(CMD("WORKER"))
client.send(CMD("END"))
client.send(CMD("---"))  # == CMD("ERROR")
client.close()
```

### Client

```python
import socket
from sjson import SJSON

port = 9090

print socket.gethostname(), port

client_sjson = SJSON()
client_sjson.connect((socket.gethostname(), port))
for item in client_sjson.recv():
    print repr(item)

```
