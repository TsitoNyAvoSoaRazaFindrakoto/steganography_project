#!/usr/bin/env python3
"""
Main script for the steganography project.
"""
import argparse
import os
import sys

from steganography.image_stego import LSBImageSteganography
from steganography.audio_stego import LSBAudioSteganography
from steganography.text_stego import WhitespaceTextSteganography, ZeroWidthTextSteganography
from core.file_utils import read_binary_file, read_text_file, write_binary_file, write_text_file, get_file_extension

def main():
    parser = argparse.ArgumentParser(description="Steganography Tool for hiding data in images, audio, and text files")
    
    # Main subparser for commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    subparsers.required = True
    
    # Hide command
    hide_parser = subparsers.add_parser("hide", help="Hide data in a carrier file")
    hide_parser.add_argument("-c", "--carrier", required=True, help="Path to the carrier file")
    hide_parser.add_argument("-d", "--data", required=True, help="Path to the data file to hide")
    hide_parser.add_argument("-o", "--output", help="Path to save the output file")
    hide_parser.add_argument("-p", "--password", help="Password for secure encoding")
    hide_parser.add_argument("-m", "--method", choices=["lsb", "whitespace", "zerowidth"], default="lsb", help="Steganography method (default: lsb)")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract hidden data from a file")
    extract_parser.add_argument("-c", "--carrier", required=True, help="Path to the carrier file containing hidden data")
    extract_parser.add_argument("-o", "--output", required=True, help="Path to save the extracted data")
    extract_parser.add_argument("-p", "--password", help="Password for secure decoding")
    extract_parser.add_argument("-m", "--method", choices=["lsb", "whitespace", "zerowidth"], 
                              default="lsb", help="Steganography method (default: lsb)")
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        if args.command == "hide":
            hide_data(args)
        elif args.command == "extract":
            extract_data(args)
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

def hide_data(args):
    """Handle the hide command."""
    # Check if the carrier file exists
    if not os.path.isfile(args.carrier):
        raise FileNotFoundError(f"Carrier file not found: {args.carrier}")
    
    # Check if the data file exists
    if not os.path.isfile(args.data):
        raise FileNotFoundError(f"Data file not found: {args.data}")
    
    # Read the data to hide
    data = read_binary_file(args.data)
    
    # Determine the carrier type
    carrier_ext = get_file_extension(args.carrier)
    
    # Create the appropriate steganography object
    stego = None
    
    if carrier_ext == "png":
        stego = LSBImageSteganography(args.password)
    elif carrier_ext == "wav":
        stego = LSBAudioSteganography(args.password)
    elif carrier_ext == "txt":
        if args.method == "whitespace":
            stego = WhitespaceTextSteganography(args.password)
        elif args.method == "zerowidth":
            stego = ZeroWidthTextSteganography()
        else:
            raise ValueError(f"Method '{args.method}' not supported for text files")
    else:
        raise ValueError(f"Unsupported carrier file type: {carrier_ext}")
    
    # Hide the data
    output_path = stego.hide_data(args.carrier, data, args.output)
    
    print(f"Data successfully hidden in {output_path}")

def extract_data(args):
    """Handle the extract command."""
    # Check if the carrier file exists
    if not os.path.isfile(args.carrier):
        raise FileNotFoundError(f"Carrier file not found: {args.carrier}")
    
    # Determine the carrier type
    carrier_ext = get_file_extension(args.carrier)
    
    # Create the appropriate steganography object
    stego = None
    
    if carrier_ext == "png":
        stego = LSBImageSteganography(args.password)
    elif carrier_ext == "wav":
        stego = LSBAudioSteganography(args.password)
    elif carrier_ext == "txt":
        if args.method == "whitespace":
            stego = WhitespaceTextSteganography(args.password)
        elif args.method == "zerowidth":
            stego = ZeroWidthTextSteganography()
        else:
            raise ValueError(f"Method '{args.method}' not supported for text files")
    else:
        raise ValueError(f"Unsupported carrier file type: {carrier_ext}")
    
    # Extract the data
    data = stego.extract_data(args.carrier)
    
    # Save the extracted data
    write_binary_file(args.output, data)
    
    print(f"Data successfully extracted to {args.output}")

if __name__ == "__main__":
    sys.exit(main())
