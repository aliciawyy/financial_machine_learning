from unittest import TestCase
from datetime import datetime
import json
import mock

from mini_blockchain import base


class BlockTest(TestCase):
    def setUp(self):
        patcher = mock.patch(
            base.__name__ + ".utc_now", return_value=datetime(2018, 5, 20)
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.block = base.Block(2, 0.125, "2584a14d")
        self.block_hash = (
            "5cf131d3b1007bb8de4335a1d2eae51b9cb83c8e61"
            "2bde3d41d2f4a6f5a8536b"
        )

    def test_hash(self):
        for block, expected_hash in self._load_block_and_hash():
            assert expected_hash == block.hash

    def _load_block_and_hash(self):
        return [
            (self.block, self.block_hash),
            (base.GenesisBlock(3.14159),
             "0df631f65c4e3295e23d4f0dd5e71ade459cbfc024"
             "a737ac1f5bd727ac711499"),
            (self.block.next_block(2.015),
             "9708ea4c0176b07648b7133382b9af8a0acb9e15a41774f"
             "467157af9c306671f")
        ]

    def test_next_block(self):
        next_block = self.block.next_block(2.015)
        assert 3 == next_block.index
        assert self.block_hash == next_block.previous_hash

    def test_dumps(self):
        result = self.block.dumps()
        data = json.loads(result)
        expected = {
            "index": "2",
            "data": "0.125",
            "timestamp": "2018-05-20 00:00:00",
            "hash": self.block_hash
        }
        assert len(expected) == len(data)
        for k, v in expected.items():
            assert v == data[k]
