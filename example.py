"""
Celfie Lock - Example Usage

This script demonstrates how to use Celfie Lock for image protection.

Support this project: https://ko-fi.com/celfielock
"""

from celfie import encode, decode
import os


def main():
    print("=" * 60)
    print("Celfie Lock - Image Protection Demo")
    print("=" * 60)
    print()
    
    # Example 1: Basic encoding
    print("Example 1: Basic Message Encoding")
    print("-" * 40)
    
    # Check if we have a sample image
    sample_images = ["sample.jpg", "sample.png", "test.jpg", "test.png"]
    input_image = None
    
    for img in sample_images:
        if os.path.exists(img):
            input_image = img
            break
    
    if not input_image:
        print("Note: No sample image found.")
        print("Create a sample.jpg or sample.png to test encoding.")
        print()
        print("You can still import and use the functions:")
        print()
        print('  from celfie import encode, decode')
        print('  encode("your_image.jpg", "protected.png", "Secret message")')
        print('  message = decode("protected.png")')
        print()
        return
    
    # Encode a message
    output_image = "protected_demo.png"
    secret_message = "This is a secret message hidden by Celfie Lock!"
    secret_link = "https://ko-fi.com/celfielock"
    
    print(f"Input image: {input_image}")
    print(f"Output image: {output_image}")
    print(f"Message: {secret_message}")
    print(f"Link: {secret_link}")
    print()
    
    try:
        success = encode(
            input_image,
            output_image,
            secret_message,
            link=secret_link,
            watermark_text="Protected by Celfie",
            watermark_position="bottom-right",
            watermark_opacity=0.7
        )
        print(f"Encoding successful: {success}")
    except Exception as e:
        print(f"Encoding failed: {e}")
        return
    
    print()
    print("Example 2: Decoding the Message")
    print("-" * 40)
    
    try:
        decoded_message = decode(output_image)
        print(f"Decoded message:")
        print(decoded_message)
    except Exception as e:
        print(f"Decoding failed: {e}")
    
    print()
    print("Example 3: Verifying an Image")
    print("-" * 40)
    
    # Verify by attempting to decode
    is_celfie = decoded_message is not None
    print(f"Is Celfie-encoded: {is_celfie}")
    
    print()
    print("=" * 60)
    print("Demo complete!")
    print()
    print("Support Celfie Lock: https://ko-fi.com/celfielock")
    print("=" * 60)


if __name__ == "__main__":
    main()
