# Paste your version of blockchain.py from the basic_block_gp
# folder here
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)

        hash_string = raw_hash.hexdigest()
        return hash_string

    @property
    def last_block(self):
        return self.chain[-1]

# Remove the proof_of_work function from the server
    # def proof_of_work(self, block):
    #    block_string = json.dumps(block, sort_keys=True)
    #    proof = 0
    #    while self.valid_proof(block_string, proof) is False:
    #        proof += 1

    #    return proof

    @staticmethod
    def valid_proof(block_string, proof):
        print(f'I will now check if {proof} is valid')
        guess = block_string + str(proof)
        guess = guess.encode()

        hash_value = hashlib.sha256(guess).hexdigest()
        print(hash_value)
# Change valid_proof to require 6 leading zeros
        return hash_value[:3] == '000000'


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

# Modify the mine endpoint to instead receive
# and validate or reject a new proof sent by a client.
# It should accept a POST
@app.route('/mine', methods=['GET', 'POST'])
def mine():
    # Use data = request.get_json() to pull the data out of the POST
    data = request.get_json()
    # Check that 'proof', and 'id' are present
    proof = data.get('proof')
    id = data.get('id')
    if proof and id:
        response = {
            'message': 'new block'
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Proof and ID not present'
        }
        return jsonify(response), 400
    #print('We shall now mine a block!')
    #proof = blockchain.proof_of_work(blockchain.last_block)
    #print(f'After a long process, we got a value {proof}')

    # Forge the new Block by adding it to the chain with the proof
    new_block = blockchain.new_block(proof)
    response = {
        'block': new_block
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'len': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200

# Add an endpoint called last_block that returns the last block in the chain
@app.route('/last_block', methods=['GET'])
def last_block():
    return last_block()


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
