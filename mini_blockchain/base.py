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


def compute_hash(*args):
    info = str.encode("".join(map(str, args)))
    sha = hashlib.sha256(info)
    return sha.hexdigest()


class Block(sheepts.StringMixin):

    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = utc_now()
        self.hash = compute_hash(
            self.index, self.data, self.timestamp, self.previous_hash
        )

    def next_block(self, data):
        return Block(self.index + 1, data, self.hash)

    @property
    def proof_of_work(self):
        return self.data.get(BlockTag.proof_of_work)

    @property
    def transactions(self):
        return self.data.get(BlockTag.transactions)

    def dumps(self):
        data = dict(self.__dict__)
        data["timestamp"] = str(data["timestamp"])
        return json.dumps(data)

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
    def __init__(self, num=9):
        self.num = num

    def __call__(self, last_proof):
        proof = last_proof + 1
        while not self.is_valid_proof(last_proof, proof):
            proof += 1
        return proof

    def is_valid_proof(self, last_proof, proof):
        return proof % self.num == 0 and proof % last_proof == 0


class PoWByHashHead(sheepts.StringMixin):
    """
    In Bitcoin, the Proof of Work algorithm is called Hashcash.
    It is not too different from the basic example below.
    """
    def __init__(self, valid_head="0000"):
        self.valid_head = valid_head

    def __call__(self, last_proof):
        proof = 0
        while not self.is_valid_proof(last_proof, proof):
            proof += 1
        return proof

    def is_valid_proof(self, last_proof, proof):
        return compute_hash(last_proof, proof).startswith(self.valid_head)


class BlockChain(sheepts.StringMixin):

    def __init__(self, chain_, unconfirmed_transactions):
        self.chain = chain_
        self.unconfirmed_transactions = unconfirmed_transactions

    def mine(self, miner_address):
        proof = self.get_proof_of_work(self.last_proof_of_work)
        self.add_transaction("network", miner_address, 1)
        data = {
            BlockTag.proof_of_work: proof,
            BlockTag.transactions: list(self.unconfirmed_transactions)
        }
        new_block = self.last_block.next_block(data)
        self.chain.append(new_block)
        self.unconfirmed_transactions = []
        return new_block.dumps()

    def add_proof(self):
        pass

    def add_transaction(self, from_, to, amount):
        transaction = {
            "from": from_,
            "to": to,
            "amount": amount
        }
        self.unconfirmed_transactions.append(transaction)

    @sheepts.lazy_property
    def get_proof_of_work(self):
        return PoWByHashHead()

    @property
    def last_proof_of_work(self):
        return self.last_block.proof_of_work

    @property
    def last_block(self):
        return self.chain[-1]
