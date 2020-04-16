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

        self.new_block(previous_hash=1, proof=100)

    def new_tranaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: <str> Address of the Recipient
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction

        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
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
        #print(f'I will now check if {proof} is valid')
        guess = block_string + str(proof)
        guess = guess.encode()

        hash_value = hashlib.sha256(guess).hexdigest()
        # print(hash_value)
# Change valid_proof to require 6 leading zeros
        return hash_value[:3] == '000'
        # changed to 3 '000' so easier to perform


app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/', methods=['GET'])
def server_working():
    response = {
        'text': 'server working'
    }
    return jsonify(response), 200

# Modify the mine endpoint to instead receive
# and validate or reject a new proof sent by a client.
# It should accept a POST
@app.route('/mine', methods=['POST'])
def mine():
    # Use data = request.get_json() to pull the data out of the POST
    data = request.get_json()
    # Check that 'proof', and 'id' are present
    if 'id' not in data or 'proof' not in data:
        response = {
            'message': 'missing value'
        }
        return jsonify(response), 400

    proof = data['proof']
    last_block = blockchain.last_block
    block_string = json.dumps(last_block, sort_keys=True)

    if blockchain.valid_proof(block_string, proof):
        # lets mine a new block and return a success!
        # someone has given the correct proof, lets reward them
        blockchain.new_tranaction(
            sender="0",
            recipient=data['id'],
            amount=1
        )
        new_block = blockchain.new_block(proof)
        response = {
            'block': new_block
        }
        return jsonify(response), 200
    else:
        # respond with an error message
        response = {
            'message': 'Proof is invalid'
        }
        return jsonify(response), 200


# Add an endpoint called last_block that returns the last block in the chain
@app.route('/last_block', methods=['GET'])
def return_last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'len': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_tranaction():
    data = request.get_json()

    # check that required fields are present
    if 'recipient' not in data or 'amount' not in data or 'sender' not in data:
        response = {'message': 'Error: missing values'}
        return jsonify(response), 400

    # Check that this tranaction is valid!
    # in the real world, we would probably want to verify that this transaction is legit
    # for now, we can allow anyone to add whatever they want

    # create the new transaction
    index = blockchain.new_tranaction(
        data['sender'], data['recipient'], data['amount'])
    response = {
        'message': f'Transaction will be posted in block with index {index}'}
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
