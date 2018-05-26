from datetime import datetime
import hashlib
import json
from pandas import to_datetime

import sheepts


class BlockTag(object):
    proof_of_work = "proof_of_work"
    transactions = "transactions"


def utc_now():
    return datetime.utcnow()


def get_hash_hex(*args):
    sha = hashlib.sha256()
    info = str.encode("".join(map(str, args)))
    sha.update(info)
    return sha.hexdigest()


class Block(sheepts.StringMixin):

    def __init__(self, index, data, previous_hash, timestamp=None,
                 hash_=None):
        self.index = index
        self.data = data
        self.timestamp = utc_now() if timestamp is None \
            else to_datetime(timestamp)
        self.previous_hash = previous_hash
        self._hash = hash_

    @property
    def hash(self):
        if self._hash is None:
            self._hash = get_hash_hex(
                self.index, self.data, self.timestamp, self.previous_hash
            )
        return self._hash

    def next_block(self, data):
        return Block(self.index + 1, data, self.hash)

    def dumps(self):
        data = {
            "index": self.index,
            "data": self.data,
            "timestamp": str(self.timestamp),
            "previous_hash": self.previous_hash,
            "hash_": self.hash,
        }
        return json.dumps(data)

    @property
    def proof_of_work(self):
        return self.data.get(BlockTag.proof_of_work)

    @property
    def transactions(self):
        return self.data.get(BlockTag.transactions)

    @classmethod
    def from_json(cls, s_json):
        kwargs = json.loads(s_json)
        return cls(**kwargs)


class GenesisBlock(Block):
    def __init__(self, data):
        super(GenesisBlock, self).__init__(0, data, "0")


class ProofOfWork(sheepts.StringMixin):
    def __init__(self, num_letters=9):
        self.num_letters = num_letters

    def __call__(self, last_proof):
        current_proof = last_proof + 1
        while not (
                current_proof % self.num_letters == 0 and
                current_proof % last_proof == 0):
            current_proof += 1
        return current_proof


class BlockChain(sheepts.StringMixin):
    num_letters = 9

    def __init__(self, blocks, transactions_current_node):
        self.blocks = blocks
        self.transactions_current_node = transactions_current_node

    def mine(self, miner_address):
        proof = self.get_proof_of_work(self.last_proof_of_work)
        transaction_for_miner = {
            "from": "network",
            "to": miner_address,
            "amount": 1
        }
        self.transactions_current_node.append(transaction_for_miner)
        data = {
            BlockTag.proof_of_work: proof,
            BlockTag.transactions: list(self.transactions_current_node)
        }
        new_block = self.last_block.next_block(data)
        self.blocks.append(new_block)
        self.transactions_current_node = []
        return new_block.dumps()

    @sheepts.lazy_property
    def get_proof_of_work(self):
        return ProofOfWork(num_letters=self.num_letters)

    @property
    def last_proof_of_work(self):
        return self.last_block.proof_of_work

    @property
    def last_block(self):
        return self.blocks[-1]
