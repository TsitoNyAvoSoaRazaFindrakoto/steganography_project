"""
Pseudo-random number generation functions for cryptographic purposes.
"""
import hashlib
import hmac
import os
import struct

def generate_seed(length=16):
	"""Generate a random seed of specified length."""
	return os.urandom(length)

def seed_from_password(password, salt=None, iterations=10000):
	"""Generate a seed from a password using PBKDF2."""
	if salt is None:
		salt = os.urandom(16)
	
	key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
	return key, salt

class PRNG:
	"""A simple pseudo-random number generator based on HMAC-SHA256."""
	
	def __init__(self, seed):
		self.seed = seed
		self.counter = 0
		self.buffer = b''
		self.buffer_index = 0
		
	def _refill_buffer(self):
		"""Refill the internal buffer with new random bytes."""
		counter_bytes = struct.pack('>Q', self.counter)
		self.buffer = hmac.new(self.seed, counter_bytes, hashlib.sha256).digest()
		self.buffer_index = 0
		self.counter += 1
		
	def get_bytes(self, num_bytes):
		"""Get specified number of random bytes."""
		result = bytearray()
		
		while len(result) < num_bytes:
			if self.buffer_index >= len(self.buffer):
				self._refill_buffer()
				
			remaining = num_bytes - len(result)
			chunk = self.buffer[self.buffer_index:self.buffer_index + remaining]
			self.buffer_index += len(chunk)
			
			result.extend(chunk)
			
		return bytes(result)
	
	def get_int(self, min_val, max_val):
		"""Get a random integer in the range [min_val, max_val]."""
		range_size = max_val - min_val + 1
		if range_size <= 0:
			raise ValueError("max_val must be greater than min_val")
			
		# Calculate how many bytes we need
		needed_bits = range_size.bit_length()
		needed_bytes = (needed_bits + 7) // 8
		
		# Get random bytes and convert to integer
		while True:
			random_bytes = self.get_bytes(needed_bytes)
			random_int = int.from_bytes(random_bytes, byteorder='big')
			
			# Make sure it's within our range
			if random_int < range_size:
				return min_val + random_int
