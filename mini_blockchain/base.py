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

    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.timestamp = utc_now()
        self.previous_hash = previous_hash
        self.hash = get_hash_hex(
            self.index, self.data, self.timestamp, self.previous_hash
        )

    def next_block(self, data):
        return Block(self.index + 1, data, self.hash)

    def dumps(self):
        data = dict(self.__dict__)
        data["timestamp"] = str(data["timestamp"])
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
        hash_ = kwargs.pop("hash")
        timestamp = to_datetime(kwargs.pop("timestamp"))
        block = cls(**kwargs)
        block.hash = hash_
        block.timestamp = timestamp
        return block


class GenesisBlock(Block):
    def __init__(self, data):
        super(GenesisBlock, self).__init__(0, data, "0")


class PoWByNumLetters(sheepts.StringMixin):
    """
    Proof Of Work
    The goal of PoW is to discover a number which solves a problem.
    The number must be difficult to find but easy to verify.
    """
    def __init__(self, num_letters=9):
        self.num_letters = num_letters

    def __call__(self, last_proof):
        current_proof = last_proof + 1
        while not (
                current_proof % self.num_letters == 0 and
                current_proof % last_proof == 0):
            current_proof += 1
        return current_proof


class PoWByHashHead(sheepts.StringMixin):
    """
    In Bitcoin, the Proof of Work algorithm is called Hashcash.
    It is not too different from the basic example below.
    """
    def __init__(self, valid_head="0000"):
        self.valid_head = valid_head

    def __call__(self, last_proof):
        proof = 0
        while get_hash_hex(last_proof, proof)[:self.head_len] != \
                self.valid_head:
            proof += 1
        return proof

    @sheepts.lazy_property
    def head_len(self):
        return len(self.valid_head)


class BlockChain(sheepts.StringMixin):

    def __init__(self, blocks, transactions_current_node):
        self.blocks = blocks
        self.transactions_current_node = transactions_current_node

    def mine(self, miner_address):
        proof = self.get_proof_of_work(self.last_proof_of_work)
        self.add_transaction("network", miner_address, 1)
        data = {
            BlockTag.proof_of_work: proof,
            BlockTag.transactions: list(self.transactions_current_node)
        }
        new_block = self.last_block.next_block(data)
        self.blocks.append(new_block)
        self.transactions_current_node = []
        return new_block.dumps()

    def add_transaction(self, from_, to, amount):
        transaction = {
            "from": from_,
            "to": to,
            "amount": amount
        }
        self.transactions_current_node.append(transaction)

    @sheepts.lazy_property
    def get_proof_of_work(self):
        return PoWByHashHead()

    @property
    def last_proof_of_work(self):
        return self.last_block.proof_of_work

    @property
    def last_block(self):
        return self.blocks[-1]
