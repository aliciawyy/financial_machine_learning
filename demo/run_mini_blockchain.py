import mini_blockchain as mb


def demo_block_chain(num_blocks=5):
    block = mb.GenesisBlock("Genesis")
    block_chain = [block]
    for i in range(num_blocks - 1):
        block = block.next_block("Block {}".format(i))
        block_chain.append(block)

    for block in block_chain:
        print(block.index, block.previous_hash, block.hash, "\n")


if __name__ == "__main__":
    demo_block_chain(num_blocks=3)
