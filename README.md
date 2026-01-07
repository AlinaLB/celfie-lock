# Celfie Lock - Open Source Image Protection

<p align="center">
  <img src="static/img/logo.png" alt="Celfie Lock Logo" width="200">
</p>

<p align="center">
  <strong>Protect your images with invisible steganography and visible watermarks</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#api">API</a> •
  <a href="#support">Support My Work</a>
</p>

---

## What is Celfie Lock?

Celfie Lock is a Python-based image protection platform that uses **steganography** to hide secret messages, links, and ownership information inside images. Unlike traditional watermarks that can be cropped or removed, Celfie Lock embeds data invisibly within the image pixels themselves.

**Key capabilities:**
- Hide secret messages inside any image
- Embed clickable links for attribution or tracking
- Add visible watermarks with customization options
- Encrypt hidden data for additional security
- Verify image authenticity and ownership

## Features

### Core Steganography Engine
- **LSB (Least Significant Bit) encoding** - Hides data in pixel values without visible changes
- **Zlib compression** - Minimizes data footprint for longer messages
- **Fernet encryption** - Military-grade AES-128 encryption for hidden content
- **Automatic format handling** - Forces PNG output to preserve hidden data

### Watermarking System
- **5 position options** - Top-left, top-right, bottom-left, bottom-right, center
- **Adjustable opacity** - From subtle (30%) to solid (100%)
- **Multiple sizes** - Small, medium, large, extra-large
- **Shadow text** - Ensures visibility on any background

### Security Features
- **Image-derived encryption** - Unique key generation per image
- **PBKDF2 key derivation** - 100,000 iterations for security
- **Signature verification** - Validates Celfie-encoded images
- **Tamper detection** - Identifies modified or corrupted images

## Installation

### Requirements
- Python 3.8+
- PIL (Pillow)
- cryptography
- numpy

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/celfie-lock.git
cd celfie-lock

# Install dependencies
pip install -r requirements.txt

# Run the example
python example.py
```

### Dependencies

```
pillow>=9.0.0
cryptography>=3.4.0
numpy>=1.20.0
```

## Usage

### Basic Encoding

```python
from celfie import encode, decode

# Hide a message in an image
encode(
    input_path="original.jpg",
    output_path="protected.png",
    message="This is my secret message!",
    link="https://mywebsite.com"
)

# Decode the hidden message
message = decode("protected.png")
print(message)  # Output: "This is my secret message!\nLINK:https://mywebsite.com"
```

### With Watermark

```python
from celfie import encode

encode(
    input_path="photo.jpg",
    output_path="protected.png",
    message="Copyright 2025",
    watermark_text="My Brand",
    watermark_position="bottom-right",
    watermark_opacity=0.8,
    watermark_size=24
)
```

### Watermark Positions

| Position | Description |
|----------|-------------|
| `top-left` | Upper left corner |
| `top-right` | Upper right corner |
| `bottom-left` | Lower left corner |
| `bottom-right` | Lower right corner |
| `center` | Center of image |

### Opacity Levels

| Value | Description |
|-------|-------------|
| `0.3` | Subtle (30%) |
| `0.5` | Light (50%) |
| `0.8` | Medium (80%) |
| `1.0` | Solid (100%) |

## API Reference

### `encode(input_path, output_path, message, **options)`

Hides a message inside an image using steganography.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_path` | str | required | Path to source image |
| `output_path` | str | required | Path for protected image |
| `message` | str | required | Secret message to hide |
| `link` | str | `""` | Optional URL to embed |
| `watermark_text` | str | `None` | Visible watermark text |
| `watermark_position` | str | `"bottom-left"` | Watermark placement |
| `watermark_opacity` | float | `0.8` | Watermark transparency (0.0-1.0) |
| `watermark_size` | int | `20` | Font size for watermark |

**Returns:** `bool` - True if successful

### `decode(image_path)`

Extracts the hidden message from a protected image.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `image_path` | str | Path to protected image |

**Returns:** `str` - The hidden message, or `None` if not found

## How It Works

### Steganography Process

1. **Message Preparation**
   - Convert message to bytes
   - Compress using zlib
   - Generate encryption key
   - Encrypt with Fernet (AES-128)

2. **Header Creation**
   - 6-byte signature ("CELFIE")
   - 4-byte version number
   - 32-byte encryption key
   - 16-byte salt
   - 8-byte data length
   - 8-byte delimiter

3. **Pixel Encoding**
   - Flatten image to byte array
   - Replace LSB of each byte with message bit
   - Reconstruct image from modified bytes

4. **Output**
   - Force PNG format (lossless)
   - Verify signature encoding
   - Save protected image

### Why PNG Only?

JPEG and other lossy formats alter pixel values during compression, which destroys the hidden data. Celfie Lock automatically converts all output to PNG to preserve your hidden messages.

## Examples

### Protect a Photo with Attribution

```python
from celfie import encode

encode(
    input_path="vacation.jpg",
    output_path="vacation_protected.png",
    message="Photo by John Doe, 2025. All rights reserved.",
    link="https://johndoe.photography",
    watermark_text="John Doe Photography",
    watermark_position="bottom-right",
    watermark_opacity=0.5
)
```

### Create a Secret Message Image

```python
from celfie import encode, decode

# Create image with hidden message
encode(
    input_path="blank.png",
    output_path="secret.png",
    message="The treasure is buried under the old oak tree!"
)

# Anyone with Celfie can reveal it
secret = decode("secret.png")
print(secret)
```

### Batch Process Multiple Images

```python
import os
from celfie import encode

images = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]

for img in images:
    output = f"protected_{os.path.basename(img).replace('.jpg', '.png')}"
    encode(
        input_path=img,
        output_path=output,
        message="Copyright 2025 - My Studio",
        watermark_text="My Studio"
    )
    print(f"Protected: {output}")
```

## Support My Work

If you find Celfie Lock useful, please consider supporting its development!

### Buy Me a Coffee

<a href="https://ko-fi.com/celfielock" target="_blank">
  <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Support on Ko-fi">
</a>

**Ko-fi:** [https://ko-fi.com/celfielock](https://ko-fi.com/celfielock)

### Other Ways to Support

- Star this repository
- Share Celfie Lock with others
- Report bugs and suggest features
- Contribute code improvements

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python and Pillow
- Encryption powered by the `cryptography` library
- Inspired by classic steganography techniques

---

<p align="center">
  Made with care by the Celfie Lock team
</p>

<p align="center">
  <a href="https://ko-fi.com/celfielock">Support on Ko-fi</a>
</p>
