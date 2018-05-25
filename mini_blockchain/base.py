from datetime import datetime
import hashlib
import json

import sheepts


def utc_now():
    return datetime.utcnow()


def get_hash_hex(*args):
    sha = hashlib.sha256()
    info = str.encode("".join(map(str, args)))
    sha.update(info)
    return sha.hexdigest()


class Block(sheepts.StringMixin):
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.timestamp = utc_now()
        self.previous_hash = previous_hash

    @sheepts.lazy_property
    def hash(self):
        return get_hash_hex(
            self.index, self.data, self.timestamp, self.previous_hash
        )

    def next_block(self, data):
        return Block(self.index + 1, data, self.hash)

    def dumps(self):
        data = {
            "index": str(self.index),
            "data": str(self.data),
            "timestamp": str(self.timestamp),
            "hash": self.hash
        }
        return json.dumps(data)


class GenesisBlock(Block):
    def __init__(self, data):
        super(GenesisBlock, self).__init__(0, data, "0")
