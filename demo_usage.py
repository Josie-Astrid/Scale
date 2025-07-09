#!/usr/bin/env python3
"""
Example usage of the improved ScalePolygonAnnotation.py script.

This script demonstrates the new configurable features and proper error handling.
"""

import os
from ScalePolygonAnnotation import create_scale_task, validate_environment


def demo_basic_usage():
    """Demonstrate basic usage with default parameters."""
    print("=== Demo: Basic Usage ===")
    try:
        # This will fail if SCALE_API_KEY is not set
        api_key = validate_environment()
        print(f"✓ API key validated (first 8 chars): {api_key[:8]}...")
        
        # This would create a task with default parameters
        # (commented out to avoid actual API calls)
        # result = create_scale_task(api_key=api_key)
        # print(f"✓ Task created: {result['task_id']}")
        
    except SystemExit:
        print("✗ SCALE_API_KEY environment variable not set")


def demo_custom_configuration():
    """Demonstrate usage with custom parameters."""
    print("\n=== Demo: Custom Configuration ===")
    
    custom_config = {
        'callback_url': 'https://my-custom-server.com/callback',
        'objects_to_annotate': ['car', 'truck', 'bus'],
        'attachment': 'https://example.com/my-image.jpg',
        'instruction': 'Please annotate all vehicles in the image with precise polygons.',
        'with_labels': True,
        'attachment_type': 'image',
        'api_key': 'demo_key_for_testing'
    }
    
    print("Custom configuration:")
    for key, value in custom_config.items():
        print(f"  {key}: {value}")
    
    # This would create a task with custom parameters
    # (commented out to avoid actual API calls)
    # try:
    #     result = create_scale_task(**custom_config)
    #     print(f"✓ Custom task created: {result['task_id']}")
    # except Exception as e:
    #     print(f"✗ Task creation failed: {e}")


def demo_error_handling():
    """Demonstrate error handling capabilities."""
    print("\n=== Demo: Error Handling ===")
    
    # Test environment validation
    original_key = os.environ.get('SCALE_API_KEY')
    
    # Temporarily remove the API key
    if 'SCALE_API_KEY' in os.environ:
        del os.environ['SCALE_API_KEY']
    
    try:
        validate_environment()
        print("✗ Should have failed validation")
    except SystemExit:
        print("✓ Properly detected missing API key")
    
    # Restore the original key if it existed
    if original_key:
        os.environ['SCALE_API_KEY'] = original_key


if __name__ == '__main__':
    print("ScalePolygonAnnotation.py Usage Examples")
    print("=" * 50)
    
    demo_basic_usage()
    demo_custom_configuration()
    demo_error_handling()
    
    print("\n=== Command Line Usage Examples ===")
    print("1. Basic usage:")
    print("   python3 ScalePolygonAnnotation.py")
    print("\n2. Custom objects:")
    print("   python3 ScalePolygonAnnotation.py --objects car truck bus")
    print("\n3. Custom callback URL:")
    print("   python3 ScalePolygonAnnotation.py --callback-url https://myserver.com/callback")
    print("\n4. Custom image URL:")
    print("   python3 ScalePolygonAnnotation.py --image-url https://example.com/image.jpg")
    print("\n5. All custom parameters:")
    print("   python3 ScalePolygonAnnotation.py \\")
    print("     --callback-url https://myserver.com/callback \\")
    print("     --objects car truck bus \\")
    print("     --image-url https://example.com/image.jpg \\")
    print("     --instruction 'Annotate all vehicles'")