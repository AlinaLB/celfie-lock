"""
Celfie Lock - Image Protection with Steganography

This module provides functions to hide secret messages and links inside images
using LSB (Least Significant Bit) steganography with encryption.

Author: Celfie Lock Team
License: MIT
Support: https://ko-fi.com/celfielock

Usage:
    from celfie import encode, decode
    
    # Hide a message
    encode("input.jpg", "protected.png", "Secret message", link="https://example.com")
    
    # Reveal the message
    message = decode("protected.png")
"""

from PIL import Image, ImageDraw, ImageFont
import os
import struct
import zlib
import base64
import hashlib
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Constants for steganography implementation
SIGNATURE = "CELFIE"
VERSION = 1
HEADER_SIZE = 74  # 6+4+32+16+8+8 = 74 bytes for signature+version+key+salt+length+delimiter
DELIMITER = b'\x00\xFF\x00\xFF\x00\xFF\x00\xFF'  # Distinct delimiter pattern


def derive_key_from_image(image_data, salt=None):
    """
    Derive encryption key from image content and optional salt.
    Creates a unique key based on the image itself.
    
    Args:
        image_data: Raw bytes of image pixel data
        salt: Optional salt bytes (16 bytes recommended)
    
    Returns:
        tuple: (encryption_key, salt)
    """
    if salt is None:
        salt = secrets.token_bytes(16)
    
    # Create hash from image pixel data
    image_hash = hashlib.sha256(image_data).digest()
    
    # Use PBKDF2 to derive a proper encryption key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(image_hash))
    return key, salt


def add_watermark(img, text, position="bottom-right", opacity=0.8, font_name="Arial", font_size=20):
    """
    Add a visible watermark to an image.
    
    Args:
        img: PIL Image object
        text: Watermark text
        position: Position string (top-left, top-right, bottom-left, bottom-right, center)
        opacity: Transparency level (0.0 to 1.0)
        font_name: Font family name
        font_size: Font size in pixels
    
    Returns:
        PIL Image with watermark applied
    """
    try:
        # Create a copy to work with
        watermarked = img.copy()
        draw = ImageDraw.Draw(watermarked)
        
        # Try to load font, fallback to default if not available
        try:
            font = ImageFont.truetype(f"{font_name}.ttf", font_size)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Get text dimensions
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = len(text) * 8
            text_height = 16
        
        # Calculate position
        width, height = img.size
        padding = 20
        
        positions = {
            'top-left': (padding, padding),
            'top-right': (width - text_width - padding, padding),
            'bottom-left': (padding, height - text_height - padding),
            'bottom-right': (width - text_width - padding, height - text_height - padding),
            'center': ((width - text_width) // 2, (height - text_height) // 2)
        }
        
        pos = positions.get(position, positions['bottom-right'])
        
        # Draw text shadows for visibility
        for offset_x, offset_y in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            if font:
                draw.text((pos[0] + offset_x, pos[1] + offset_y), text, font=font, fill=(0, 0, 0))
            else:
                draw.text((pos[0] + offset_x, pos[1] + offset_y), text, fill=(0, 0, 0))
        
        # Draw main text
        if font:
            draw.text(pos, text, font=font, fill=(255, 255, 255))
        else:
            draw.text(pos, text, fill=(255, 255, 255))
        
        return watermarked
    
    except Exception as e:
        print(f"Watermark error: {e}")
        return img


def encode(input_path, output_path, message, link="", watermark_text=None,
           watermark_position="bottom-left", watermark_opacity=0.8, 
           watermark_font="Arial", watermark_size=20):
    """
    Hide a message and optional link in an image using LSB steganography with encryption.
    
    Args:
        input_path (str): Path to the original image
        output_path (str): Path where to save the encoded image
        message (str): Message to hide in the image
        link (str, optional): URL link to hide in the image
        watermark_text (str, optional): Text to display as visible watermark
        watermark_position (str): Position of watermark 
            (top-left, top-right, bottom-left, bottom-right, center)
        watermark_opacity (float): Opacity of watermark (0.0-1.0)
        watermark_font (str): Font family for watermark
        watermark_size (int): Font size for watermark
    
    Returns:
        bool: True if successful, raises exception on failure
    
    Example:
        >>> encode("photo.jpg", "protected.png", "My secret", link="https://example.com")
        True
    """
    print(f"Encoding image: {input_path} -> {output_path}")
    print(f"Message: '{message}'")
    if link:
        print(f"Link: '{link}'")
    
    # Verify input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")
    
    # Open the image and convert to RGB
    img = Image.open(input_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    width, height = img.size
    print(f"Image dimensions: {width}x{height}")
    
    # Apply watermark if specified
    if watermark_text:
        print(f"Applying watermark: '{watermark_text}'")
        img = add_watermark(img, watermark_text, watermark_position, 
                           watermark_opacity, watermark_font, watermark_size)
    
    # Force PNG format for output (required to preserve hidden data)
    if not output_path.lower().endswith('.png'):
        output_path = os.path.splitext(output_path)[0] + '.png'
        print(f"Note: Output forced to PNG format to preserve hidden data")
    
    # Combine message and link
    full_message = message
    if link:
        full_message = f"{message}\nLINK:{link}"
    
    # Prepare data for encoding
    message_bytes = full_message.encode('utf-8')
    compressed_data = zlib.compress(message_bytes, level=9)
    
    # Generate random encryption key
    random_key = secrets.token_bytes(32)
    encryption_key = base64.urlsafe_b64encode(random_key)
    salt = secrets.token_bytes(16)
    
    # Encrypt the compressed data
    fernet = Fernet(encryption_key)
    encrypted_data = fernet.encrypt(compressed_data)
    
    print(f"Data encrypted: {len(compressed_data)} -> {len(encrypted_data)} bytes")
    
    # Create header structure
    signature_bytes = SIGNATURE.encode('utf-8')
    header = struct.pack(
        "<6sI32s16sQ8s",
        signature_bytes,      # "CELFIE" signature
        VERSION,              # Version number
        random_key,           # Encryption key
        salt,                 # Salt for security
        len(encrypted_data),  # Data length
        DELIMITER             # Delimiter pattern
    )
    
    # Combine header and encrypted data
    data_to_hide = header + encrypted_data
    binary_data = ''.join(format(b, '08b') for b in data_to_hide)
    
    # Check image capacity
    capacity = width * height * 3
    if len(binary_data) > capacity:
        raise ValueError(f"Message too large for this image. Need {len(binary_data)} bits, have {capacity} bits")
    
    # Get pixel data
    pixels = list(img.getdata())
    flat_img = []
    for pixel in pixels:
        flat_img.extend(pixel)
    
    # Encode data into image LSBs
    for i, bit in enumerate(binary_data):
        if i < len(flat_img):
            flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
    
    # Reconstruct image
    channels = len(img.getbands())
    new_pixels = []
    for i in range(0, len(flat_img), channels):
        pixel = tuple(flat_img[i:i+channels])
        new_pixels.append(pixel)
    
    encoded_img = Image.new(img.mode, (width, height))
    encoded_img.putdata(new_pixels)
    
    # Save as PNG
    encoded_img.save(output_path, format='PNG', optimize=False, compress_level=0)
    
    # Verify output
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Failed to create output image: {output_path}")
    
    print(f"Successfully encoded message into: {output_path}")
    return True


def decode(image_path):
    """
    Extract a hidden message from a Celfie-encoded image.
    
    Args:
        image_path (str): Path to the image with the hidden message
    
    Returns:
        str: The hidden message, or None if not found/invalid
    
    Example:
        >>> message = decode("protected.png")
        >>> print(message)
        "My secret
        LINK:https://example.com"
    """
    print(f"Decoding image: {image_path}")
    
    # Verify file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Open the image
    img = Image.open(image_path)
    print(f"Image mode: {img.mode}, Size: {img.size}")
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Get pixel data
    pixels = list(img.getdata())
    flat_img = []
    for pixel in pixels:
        flat_img.extend(pixel)
    
    # Extract header bits
    header_bits = ''.join(str(flat_img[i] & 1) for i in range(HEADER_SIZE * 8))
    header_bytes = bytearray()
    for i in range(0, len(header_bits), 8):
        if i + 8 <= len(header_bits):
            byte = header_bits[i:i+8]
            header_bytes.append(int(byte, 2))
    
    # Verify signature
    try:
        signature = header_bytes[:6].decode('utf-8')
        if signature != SIGNATURE:
            print(f"Invalid signature: '{signature}'")
            return None
        
        print(f"Found Celfie signature!")
        
        # Extract header components
        version = struct.unpack("<I", bytes(header_bytes[6:10]))[0]
        encryption_key = bytes(header_bytes[10:42])
        salt = bytes(header_bytes[42:58])
        data_length = struct.unpack("<Q", bytes(header_bytes[58:66]))[0]
        
        print(f"Version: {version}, Data length: {data_length}")
        
        # Validate data length
        max_data = len(flat_img) - HEADER_SIZE * 8
        if data_length > max_data or data_length > 10_000_000:
            print(f"Invalid data length: {data_length}")
            return None
        
        # Extract encrypted data
        data_start = HEADER_SIZE * 8
        data_bits = ''.join(str(flat_img[i] & 1) for i in range(data_start, data_start + data_length * 8))
        
        encrypted_data = bytearray()
        for i in range(0, len(data_bits), 8):
            if i + 8 <= len(data_bits):
                byte = data_bits[i:i+8]
                encrypted_data.append(int(byte, 2))
        
        # Decrypt
        fernet_key = base64.urlsafe_b64encode(encryption_key)
        fernet = Fernet(fernet_key)
        compressed_data = fernet.decrypt(bytes(encrypted_data))
        
        # Decompress
        message = zlib.decompress(compressed_data).decode('utf-8')
        
        print(f"Successfully decoded message!")
        return message
    
    except struct.error as e:
        print(f"Header parsing error: {e}")
        return None
    except Exception as e:
        print(f"Decoding error: {e}")
        return None


def verify_image(image_path):
    """
    Check if an image contains Celfie-encoded data.
    
    Args:
        image_path: Path to the image to verify
    
    Returns:
        bool: True if the image contains valid Celfie data
    """
    try:
        result = decode(image_path)
        return result is not None
    except:
        return False


# Example usage
if __name__ == "__main__":
    print("Celfie Lock - Image Protection with Steganography")
    print("=" * 50)
    print()
    print("Usage:")
    print("  from celfie import encode, decode")
    print()
    print("  # Hide a message")
    print('  encode("input.jpg", "protected.png", "My secret message")')
    print()
    print("  # Reveal the message")
    print('  message = decode("protected.png")')
    print()
    print("Support this project: https://ko-fi.com/celfielock")
