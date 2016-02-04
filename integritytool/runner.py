#!/usr/bin/env python3

import base64
import json
from hashlib import sha256
from pprint import pprint
from math import *

def leaf_hash(entry):
  leaf_input = entry['leaf_input']
  leaf_input_raw = base64.b64decode(leaf_input)
  bytearray = b'\x00' + leaf_input_raw
  return sha256(bytearray).digest()

def left_subtree_size(tree_size):
  assert tree_size > 1
  return 2**((tree_size - 1).bit_length() -1)

def subtree_hash(entries):
  n = len(entries)
  assert n > 1

  k = left_subtree_size(n)
  left_tree_hash = merkle_tree_hash(entries[0:k])
  right_tree_hash = merkle_tree_hash(entries[k:n])

  bytearray = b'\x01' + left_tree_hash + right_tree_hash
  return sha256(bytearray).digest()

# based on MTH() defined in RFC6962§2.1
def merkle_tree_hash(entries):
  if len(entries) == 1:
    return leaf_hash(entries[0])
  else:
    return subtree_hash(entries)

def run():
  with open('entries.json') as data_file:
    data = json.load(data_file)
    pprint(data)

  print(base64.b64encode(merkle_tree_hash(data['entries'])))
  # read entries.json
  # compute root hash from entries
  # print root hash
  # visually compare with root hash in sth.json

if __name__ == '__main__':
  run()

