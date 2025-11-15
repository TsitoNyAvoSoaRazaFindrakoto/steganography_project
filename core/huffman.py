"""
Huffman coding implementation for efficient data compression.
"""
import heapq
from collections import Counter
from typing import Dict, Optional, Tuple


class HuffmanNode:
	def __init__(self, char: Optional[str], freq: int):
		self.char = char
		self.freq = freq
		self.left: Optional['HuffmanNode'] = None
		self.right: Optional['HuffmanNode'] = None

	def __lt__(self, other: 'HuffmanNode') -> bool:
		return self.freq < other.freq

def build_huffman_tree(data: str) -> Optional[HuffmanNode]:
	"""Build a Huffman tree from the given data."""
	frequency = Counter(data)
	priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
	print(frequency)
	print(priority_queue)
	heapq.heapify(priority_queue)

	while len(priority_queue) > 1:
		left = heapq.heappop(priority_queue)
		right = heapq.heappop(priority_queue)

		internal_node = HuffmanNode(None, left.freq + right.freq)
		internal_node.left = left
		internal_node.right = right

		heapq.heappush(priority_queue, internal_node)

	return priority_queue[0] if priority_queue else None


def generate_codes(node: Optional[HuffmanNode], current_code: str = "", codes: Optional[Dict[str, str]] = None) -> Dict[str, str]:
	"""Generate Huffman codes for each character."""
	if codes is None:
		codes = {}

	if node:
		if node.char is not None:
			codes[node.char] = current_code if current_code else "0"
		generate_codes(node.left, current_code + "0", codes)
		generate_codes(node.right, current_code + "1", codes)

	return codes


def huffman_encode(data: str) -> Tuple[str, Dict[str, str]]:
	"""Encode data using Huffman coding."""
	if not data:
		return "", {}

	root = build_huffman_tree(data)
	codes = generate_codes(root)

	encoded_data = ''.join(codes[char] for char in data)
	return encoded_data, codes


def huffman_decode(encoded_data: str, codes: Dict[str, str]) -> str:
	"""Decode Huffman-encoded data."""
	if not encoded_data:
		return ""

	reversed_codes = {code: char for char, code in codes.items()}
	decoded_data = []

	current_code = ""
	for bit in encoded_data:
		current_code += bit
		if current_code in reversed_codes:
			decoded_data.append(reversed_codes[current_code])
			current_code = ""

	return ''.join(decoded_data)




