"""
Utility functions for Jupyter notebooks in the steganography project.
"""
import os
import sys
import matplotlib.pyplot as plt
from PIL import Image

# Ensure we can import from the main project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def display_image_comparison(original_path, stego_path, figsize=(12, 6)):
    """
    Display two images side by side for comparison.
    
    Args:
        original_path: Path to the original image
        stego_path: Path to the steganographic image
        figsize: Figure size as a tuple (width, height)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Load and display original image
    img1 = Image.open(original_path)
    ax1.imshow(img1)
    ax1.set_title("Original Image")
    ax1.axis('off')
    
    # Load and display stego image
    img2 = Image.open(stego_path)
    ax2.imshow(img2)
    ax2.set_title("Image with Hidden Data")
    ax2.axis('off')
    
    plt.tight_layout()
    plt.show()

def display_audio_waveform(audio_path, figsize=(10, 4)):
    """
    Display the waveform of an audio file.
    
    Args:
        audio_path: Path to the audio file (.wav)
        figsize: Figure size as a tuple (width, height)
    """
    try:
        import wave
        import numpy as np
        
        with wave.open(audio_path, 'rb') as wav:
            # Get audio parameters
            nchannels = wav.getnchannels()
            sampwidth = wav.getsampwidth()
            framerate = wav.getframerate()
            nframes = wav.getnframes()
            
            # Read frames
            frames = wav.readframes(nframes)
        
        # Convert to numpy array
        if sampwidth == 1:
            dtype = np.uint8
        elif sampwidth == 2:
            dtype = np.int16
        else:
            dtype = np.int32
            
        audio_array = np.frombuffer(frames, dtype=dtype)
        
        # If stereo, take one channel for visualization
        if nchannels == 2:
            audio_array = audio_array[::2]  # Take left channel
        
        # Calculate time axis
        time = np.linspace(0, nframes / framerate, num=len(audio_array))
        
        # Plot waveform
        plt.figure(figsize=figsize)
        plt.plot(time, audio_array, color='blue', alpha=0.7)
        plt.title(f"Audio Waveform: {os.path.basename(audio_path)}")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Amplitude")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Print audio info
        print(f"Audio: {os.path.basename(audio_path)}")
        print(f"Channels: {nchannels}")
        print(f"Sample width: {sampwidth} bytes")
        print(f"Frame rate: {framerate} Hz")
        print(f"Duration: {nframes / framerate:.2f} seconds")
        
    except Exception as e:
        print(f"Error displaying audio waveform: {str(e)}")

def analyze_stego_effectiveness(original_path, stego_path, data_size):
    """
    Analyze and display statistics about the steganography effectiveness.
    
    Args:
        original_path: Path to the original carrier file
        stego_path: Path to the steganographic file
        data_size: Size of the hidden data in bytes
    """
    # Get file sizes
    original_size = os.path.getsize(original_path)
    stego_size = os.path.getsize(stego_path)
    
    # Calculate statistics
    size_diff = stego_size - original_size
    size_diff_percent = (size_diff / original_size) * 100
    data_to_carrier_ratio = (data_size / original_size) * 100
    
    # Print statistics
    print("Steganography Effectiveness Analysis")
    print("-----------------------------------")
    print(f"Original file size: {original_size:,} bytes")
    print(f"Stego file size: {stego_size:,} bytes")
    print(f"Size difference: {size_diff:,} bytes ({size_diff_percent:.2f}%)")
    print(f"Hidden data size: {data_size:,} bytes")
    print(f"Data to carrier ratio: {data_to_carrier_ratio:.2f}%")
    
    # For image files, calculate PSNR if possible
    if original_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        try:
            import numpy as np
            from PIL import Image
            from math import log10
            
            # Load images
            img1 = np.array(Image.open(original_path)).astype(float)
            img2 = np.array(Image.open(stego_path)).astype(float)
            
            # Calculate MSE
            mse = np.mean((img1 - img2) ** 2)
            if mse == 0:
                psnr = float('inf')
            else:
                max_pixel = 255.0
                psnr = 20 * log10(max_pixel / (mse ** 0.5))
                
            print(f"PSNR (Peak Signal-to-Noise Ratio): {psnr:.2f} dB")
            
            # PSNR interpretation
            if psnr > 40:
                quality = "Excellent (differences are imperceptible)"
            elif psnr > 30:
                quality = "Good (differences are barely noticeable)"
            elif psnr > 20:
                quality = "Acceptable (differences may be noticeable)"
            else:
                quality = "Poor (differences are clearly visible)"
                
            print(f"Image quality: {quality}")
            
        except Exception as e:
            print(f"Could not calculate PSNR: {str(e)}")
