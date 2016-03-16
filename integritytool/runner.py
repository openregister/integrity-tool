#!/usr/bin/env python3

import base64, json, cmd, hashlib
from pprint import pprint
from math import *

SHA_LEN = 256

# Pre-compute defaults for empty leaves
def leaf_hash(leaf_bytes):
  bytearray = b'\x00' + leaf_bytes
  return hashlib.sha256(bytearray).digest()

def parent_hash(left_child_hash, right_child_hash):
  bytearray = b'\x01' + left_child_hash + right_child_hash
  return hashlib.sha256(bytearray).digest()

DEFAULTS = [leaf_hash(''.encode('ISO-8859-1'))]
for i in range(SHA_LEN):
  DEFAULTS.append(parent_hash(DEFAULTS[-1], DEFAULTS[-1]))
DEFAULTS = DEFAULTS[::-1]

class ReplCmd(cmd.Cmd):
  def __init__(self):
    cmd.Cmd.__init__(self)
    self.prompt = '> '
    self.runner = Runner()

  def do_mth(self, arg=''):
    self.runner.compute_root_hash()

  def do_mapth(self, arg):
    #try:
    key, value, proof = arg.split(' ')
    key = key.strip()
    value = value.strip()
    proof = [s[1:-1] if (s[0] == '\'' and s[-1] == '\'') else int(s) for s in proof[1:-1].split(',')]
    #except:
      #self.help_mapth()

    print('Key: ' + key)
    print('Value: ' + value)
    print('Proof: ' + str(proof))

    mapth = self.runner.compute_map_root_hash_from_proof(key, value, proof)
    print('Map tree hash: ' + str(base64.b64encode(mapth)))

  def help_mapth(self):
    print('mapth <key> <value> <proof>')

class Runner():

  def left_subtree_size(self, tree_size):
    assert tree_size > 1
    return 2**((tree_size - 1).bit_length() -1)

  def subtree_hash(self, entries):
    n = len(entries)
    assert n > 1

    k = self.left_subtree_size(n)
    left_tree_hash = self.merkle_tree_hash(entries[0:k])
    right_tree_hash = self.merkle_tree_hash(entries[k:n])

    return parent_hash(left_tree_hash, right_tree_hash)

  # based on MTH() defined in RFC6962
  def merkle_tree_hash(self, entries):
    if len(entries) == 1:
      return leaf_hash(base64.b64decode(entries[0]['leaf_input']))
    else:
      return self.subtree_hash(entries)

  def compute_root_hash(self):
    with open('entries.json') as data_file:
      data = json.load(data_file)
      pprint(data)

    print(base64.b64encode(self.merkle_tree_hash(data['entries'])))
    # read entries.json
    # compute root hash from entries
    # print root hash
    # visually compare with root hash in sth.json

  def compute_map_root_hash_from_proof(self, key, value, proof):
    path = self.construct_key_path(key)
    proof = self.decompress_proof(proof)
    value_hash = leaf_hash(value.encode('ISO-8859-1'))

    for i in range(SHA_LEN, 0, -1):
      if path[i - 1]:
        value_hash = parent_hash(proof[i-1], value_hash)
      else:
        value_hash = parent_hash(value_hash, proof[i-1])

    return value_hash

  # Uncompress Google's compressed proof. Output is 256 raw byte arrays.
  def decompress_proof(self, proof):
    pp = []
    for y in proof:
      if type(y) == int:
        pp += [''] * y
      else:
        pp.append(y)
    return [DEFAULTS[idx + 1] if x == '' else base64.b64decode(x) for idx, x in enumerate(pp)]

  # Take a key as string and produce 256 boolean values indicating left (False) or right (True)
  def construct_key_path(self, key):
    return [x == '1' for x in ''.join(('%8s' % bin(x)[2:]) for x in hashlib.sha256(key.encode('ISO-8859-1')).digest())[:SHA_LEN]]

if __name__ == '__main__':
  ReplCmd().cmdloop()

