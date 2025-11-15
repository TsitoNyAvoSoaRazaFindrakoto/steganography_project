"""
Utility functions for file operations in the steganography project.
"""
import os
import json
from pathlib import Path
from typing import Dict, Union


def write_binary_file(filepath: str, data: bytes) -> None:
	"""
	Write binary data to a file.
	
	Args:
			filepath: Path to the file
			data: Binary data to write
	"""
	# Create directories if they don't exist
	os.makedirs(os.path.dirname(filepath), exist_ok=True)
	
	with open(filepath, 'wb') as f:
		f.write(data)

def read_text_file(filepath: str, encoding: str='utf-8') -> str:
	"""
	Read a text file.
	
	Args:
			filepath: Path to the file
			encoding: Text encoding (default: utf-8)
			
	Returns:
			Text content of the file
	"""
	with open(filepath, 'r', encoding=encoding) as f:
		return f.read()

def write_text_file(filepath: str, text: str, encoding: str='utf-8') -> None:
	"""
	Write text to a file.
	
	Args:
			filepath: Path to the file
			text: Text to write
			encoding: Text encoding (default: utf-8)
	"""
	# Create directories if they don't exist
	os.makedirs(os.path.dirname(filepath), exist_ok=True)
	
	with open(filepath, 'w', encoding=encoding) as f:
		f.write(text)

def get_file_extension(filepath: str) -> str:
	"""
	Get the extension of a file.
	
	Args:
		filepath: Path to the file
		
	Returns:
		File extension (lowercase, without the dot)
	"""
	return Path(filepath).suffix.lower()[1:]
	
def read_binary_file(filepath: str, ignore_bytes: int = 0) -> bytes:
	"""
	Read a file in binary mode.
	
	Args:
			filepath: Path to the file
			
	Returns:
			Binary content of the file
	"""
	with open(filepath, 'rb') as f:
		f.seek(ignore_bytes)
		return f.read()

def display_all_bytes(data, title):
    print(f"=== {title} ===\n")
    print(f"Total bytes: {len(data)}\n")
    
    print("All bytes as:")
    for i, byte in enumerate(data):
        print(f"Byte {i}:")
        print(f"  Integer: {byte}")
        print(f"  Hex: 0x{byte:02x}")
        print(f"  Binary: {bin(byte)[2:].zfill(8)}")
        print(f"  ASCII: {chr(byte) if 32 <= byte <= 126 else '.'}\n")
