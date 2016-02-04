import pytest
from hypothesis import given
from hypothesis.strategies import integers
from integritytool.runner import *

def test_leaf_hash():
	entry = { 
	"leaf_input": "AAAAAAFSeasHmIAAAABNeyAib3duZXIiOiAiSG9tZSBPZmZpY2UiLCAiZW5kLWRhdGUiOiAiIiwgImdvdmVybm1lbnQtZG9tYWluIjogIjEwMS5nb3YudWsiIH0AAA==", 
	"extra_data": "" 
	}

	actual_leaf_hash = leaf_hash(entry)
	assert actual_leaf_hash == b"zpD/7JrTGb5db3HbC87SJiMqXoIZCWfX2HUvpOb31GI="

def test_left_subtree_size():
	with pytest.raises(AssertionError):
		left_subtree_size(1)
	assert left_subtree_size(2) == 1
	assert left_subtree_size(7) == 4
	assert left_subtree_size(127) == 64
	assert left_subtree_size(128) == 64
	assert left_subtree_size(129) == 128

@given(integers(min_value=2))
def test_left_subtree_size_gen(n):
        k = left_subtree_size(n)

        # assert k is a power of 2
        # from http://www.graphics.stanford.edu/~seander/bithacks.html#DetermineIfPowerOf2
        assert (k & (k - 1)) == 0

        # assert k the largest power of 2 smaller than n
        # from RFC 6962 § 2.1
        assert k < n
        assert n <= 2*k
