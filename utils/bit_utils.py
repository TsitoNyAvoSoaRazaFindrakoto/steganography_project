"""
Utility functions for bit manipulation in steganography.
"""

def bytes_to_bits(data : bytes) -> str:
	result = ""
	for byte in data:
		binary = format(byte, '08b')
		result += binary
	return result

def bits_to_bytes(bits : str) -> bytes:
	padding = (8 - len(bits) % 8) % 8
	padded_bits = bits + '0' * padding
	
	bytes_list = bytearray()
	for i in range(0, len(padded_bits), 8):
		byte = padded_bits[i:i+8]
		bytes_list.append(int(byte, 2))
	
	return bytes(bytes_list)

def get_bit(value : int, position : int = 0) -> int:
	return (value >> position) & 1

def get_inverted_bit(value : int, position : int = 0) -> int:
	return (value >> position) & 0

def set_bit(value : int, position : int, bit : int) -> int:
	mask = 1 << position
	if bit:
		return value | mask
	else:
		return value & ~mask

def replace_lsb(value : int, bit : int) -> int:
	return (value & ~1) | (bit & 1)

def count_usable_bits(data_size : int, bits_per_unit : int=1) -> int:
	return data_size * bits_per_unit

def get_bytes_from_array(bytes_array : bytes,indexes : list[int]) -> bytes:
	new_bytes = bytearray()
	for index in indexes:
		new_bytes.append(bytes_array[index])
	return bytes(new_bytes)
