import random # is used to generate pseudo-random keys
import string # is used to generate pseudo-random keys


MAX_LIMIT = 255 # the limit for the extended ASCII Character set

# function to generate the keys
def generateKeys(numberOfKeys):
    for keyIndex in range(numberOfKeys):

        # the next line is the generation of a random string see https://www.askpython.com/python/examples/generate-random-strings-in-python
        randomKey = "".join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(random.randint(100, 1000)))
        
        f = open("rng_tunnel/key" + str(keyIndex) + ".json", "w")
        f.write('{\n\t"key": "' + randomKey + '"\n}')
        f.close()