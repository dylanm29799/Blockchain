#Module 1 - Create a BlockChain


#Importing Libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

#Part 1 - Building a blockchain

class Blockchain:
    
    # Initialize the blockchain with an empty list and create the genesis block
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    # Create a new block with the given proof and previous hash, then add it to the chain
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        self.chain.append(block)
        return block
    # Return the last block in the chain
    def get_prev_block(self): 
        return self.chain[-1]
    
    # Find a proof of work that satisfies the condition of leading zeros in the hash
    def proof_of_work(self, previous_proof):
        new_proof = 1; 
        check_proof = False;
        while check_proof is False: 
            # Generate a SHA-256 hash based on the proof difference squared
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # Check if the hash starts with four leading zeros
            if hash_operation[:4] == '0000':
                check_proof = True
            else: 
                new_proof += 1
        return new_proof
    
    def hash(self, block): 
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain): 
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
        previous_proof = previous_block['proof']
        proof = block['proof']
        hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
        if hash_operation[:4] != '0000':
            return False
        previous_block = block
        block_index +=1 
        return True


#Part 2 - Mining the blockchain

#Creating Web App
app = Flask(__name__)

#Creating blockchain
blockchain = Blockchain()

#Mining a new Block

@app.route('/mineblock', methods = ['GET'])
def mine_block(): 
    previous_block = blockchain.get_prev_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    res = {'message' : 'CONGRATS ON THE BLOCK!!!!',
           'index' : block['index'], 
           'timestamp' : block['timestamp'],
           'proof' : block['proof'],
           'previous_hash' : block['previous_hash']}
    return jsonify(res, 200)

#Getting the Full Blockchain

@app.route('/get_chain', methods = ['GET'])
def get_chain(): 
    res = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(res, 200)    

#Running the app
app.run(host= '0.0.0.0',
        port = 5000)
















        