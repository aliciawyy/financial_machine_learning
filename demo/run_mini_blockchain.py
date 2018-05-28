import mini_blockchain as mb


def demo_block_chain(num_blocks=5):
    miner_address = "3ed43a2"
    block_chain = mb.BlockChain([mb.GenesisBlock()], [])
    for _ in range(num_blocks - 1):
        block_chain.mine(miner_address)
        print(block_chain.last_block.dumps(), "\n")


if __name__ == "__main__":
    demo_block_chain(num_blocks=5)
