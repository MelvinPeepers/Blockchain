import hashlib
import requests

import sys
import json


def proof_of_work(block):
    block_string = json.dumps(block, sort_keys=True)

    proof = 0

    while valid_proof(block_string, proof) is False:
        proof += 1

    return proof


def valid_proof(block_string, proof):
    #print(f'I will now check if {proof} is valid')
    guess = block_string + str(proof)
    guess = guess.encode()

    hash_value = hashlib.sha256(guess).hexdigest()
    # print(hash_value)
# Change valid_proof to require 6 leading zeros
    return hash_value[:3] == '000'
    # changed to 3 to make it easier


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        new_proof = proof_of_work(data['last_block'])

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        print(data)
        if 'block' in data:
            coins_mined += 1
            print(f"Total coins mined: {coins_mined}")
        else:
            print(data['message'])
        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
