# Steganography Project

A comprehensive steganography toolkit for hiding and extracting data in various file formats.

## Features

- **Image Steganography**: Hide data in PNG images using LSB (Least Significant Bit) method
- **Audio Steganography**: Hide data in WAV audio files using LSB method
- **Text Steganography**: Hide data in text files using whitespace or zero-width characters
- **Password Protection**: Optional password-based encryption for enhanced security
- **Data Compression**: Huffman coding for efficient data storage
- **Jupyter Integration**: Interactive notebooks for visualization and experimentation

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/steganography-project.git
   cd steganography-project
   ```

2. Create and initializa a venv
   ```
	 python -m venv .venv
	 source .venv/bin/activate
	 ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

#### Hiding Data

```bash
python main.py hide -c carrier_file -d data_file [-o output_file] [-p password] [-m method]
```

Options:
- `-c, --carrier`: Path to the carrier file (PNG image, WAV audio, or TXT file)
- `-d, --data`: Path to the data file you want to hide
- `-o, --output`: Optional path to save the output file
- `-p, --password`: Optional password for secure encoding
- `-m, --method`: Steganography method (lsb, whitespace, zerowidth)

#### Extracting Data

```bash
python main.py extract -c carrier_file -o output_file [-p password] [-m method]
```

Options:
- `-c, --carrier`: Path to the carrier file containing hidden data
- `-o, --output`: Path to save the extracted data
- `-p, --password`: Password for secure decoding (if used during hiding)
- `-m, --method`: Steganography method (lsb, whitespace, zerowidth)

### Jupyter Notebook

For interactive usage and visualization, you can use the Jupyter notebook:

1. Start Jupyter notebook server:
   ```
   jupyter notebook
   ```

2. Navigate to `examples/steganography_demo.ipynb` to open the demo notebook.

3. Follow the examples in the notebook to learn how to hide and extract data interactively.

## Examples

### Hiding an image in another image:
```bash
python main.py hide -c examples/input_image.png -d secret.jpg -o examples/output_image.png
```

### Hiding text in an audio file with password protection:
```bash
python main.py hide -c examples/input_audio.wav -d secret.txt -p mysecretpassword
```

### Extracting hidden data from an image:
```bash
python main.py extract -c examples/output_image.png -o extracted_secret.jpg
```

## Project Structure

