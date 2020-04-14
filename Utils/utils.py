import hashlib

class HashFile(object):
    def __init__(self, filename, blocksize = 65536):
        file_hash = hashlib.sha256()
        with open(filename, 'rb') as f:
            fb = f.read(blocksize)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(blocksize)

        self.digest = file_hash.hexdigest()

    def getDigest(self):
        return self.digest


