#!/usr/bin/env python3

import base64
import json
from hashlib import sha256
from pprint import pprint

def leaf_hash(entry):
  leaf_input = entry['leaf_input']
  leaf_input_raw = base64.b64decode(leaf_input)
  bytearray = b'\x00' + leaf_input_raw
  return base64.b64encode(sha256(bytearray).digest())

def left_subtree_size(tree_size):
  #TODO
  if tree_size == 3:
    return 2
  if tree_size == 2:
    return 1
  raise "not implemented"

def tree_hash(entries):
  n = len(entries)
  k = left_subtree_size(n)

  return "bar"

# based on MTH() defined in RFC6962§2.1
def merkle_tree_hash(entries):
  if len(entries) == 1:
    return leaf_hash(entries[0])
  else:
    return tree_hash(entries)

def run():
  with open('entries2.json') as data_file:
    data = json.load(data_file)
    pprint(data)

  print(merkle_tree_hash(data['entries']))
  print(leaf_hash(data['entries'][0]))
  # read entries.json
  # compute root hash from entries
  # print root hash
  # visually compare with root hash in sth.json

if __name__ == '__main__':
  run()

