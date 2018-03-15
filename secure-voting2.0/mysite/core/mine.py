from django.db import models
import hashlib
import logging

# receiverId,timestampVote are given
''' prevHash= "hello" #from DB from previous hash
receiverId = "bjp"
timeStampVote = "1:03"
nonce = 0 '''


def generate_hash(receiverId, timeStampVote, prevHash):
    nonce = 0
    signal = True
    difficulty = 3
    zeroStr = ""
    concatValue = str(receiverId) + str(timeStampVote) + str(prevHash)
    #logging.warning("This is concatValue without nonce:"+concatValue)
    for i in range(difficulty):
        zeroStr = zeroStr+'0'
    originalValue=concatValue
    while signal:
        concatValue = originalValue + str(nonce)
        hash_object = hashlib.sha256(concatValue.encode())
        finalHash = hash_object.hexdigest()
        # print(finalHash)   #printing the final calculated hash

        if(finalHash[:difficulty] == zeroStr):
            blockHash = finalHash
            signal = False
        else:
            nonce = nonce+1
            signal = True

    return (blockHash, nonce)
