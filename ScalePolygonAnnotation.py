#!/usr/bin/env python3
"""
Scale API Polygon Annotation Script

This script creates a polygon annotation task using the Scale API.
It sends an image to Scale for annotation and receives a task ID back.

Usage:
    python3 ScalePolygonAnnotation.py

Environment Variables Required:
    SCALE_API_KEY: Your Scale API key for authentication

Author: Josie Barth
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional, Union

import requests


def validate_environment() -> str:
    """
    Validate that all required environment variables are set.
    
    Returns:
        str: The Scale API key
        
    Raises:
        SystemExit: If required environment variables are missing
    """
    api_key = os.environ.get('SCALE_API_KEY')
    if not api_key:
        print("Error: SCALE_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set it with: export SCALE_API_KEY='your_scale_api_key'", file=sys.stderr)
        sys.exit(1)
    return api_key


def create_scale_task(
    callback_url: str = 'https://scale-demo.herokuapp.com/scale/callback',
    objects_to_annotate: Optional[List[str]] = None,
    attachment: str = 'https://scale.com/static/img/website/index/example-ia-boxes.jpg',
    instruction: str = 'Draw a tight polygon around every **car** in the image.',
    with_labels: bool = True,
    attachment_type: str = 'image',
    api_key: Optional[str] = None
) -> Dict[str, Union[str, int]]:
    """
    Create a polygon annotation task using the Scale API.
    
    Args:
        callback_url: URL where Scale will send the completed task results
        objects_to_annotate: List of object types to annotate (defaults to ['car', 'suv'])
        attachment: URL of the image to annotate
        instruction: Instructions for the annotators
        with_labels: Whether to include labels in the annotation
        attachment_type: Type of attachment (image, video, etc.)
        api_key: Scale API key (if not provided, will get from environment)
        
    Returns:
        Dict containing the task_id and any other response data
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails
        KeyError: If the response doesn't contain expected fields
        ValueError: If the API returns an error response
    """
    # Set default objects to annotate if not provided
    if objects_to_annotate is None:
        objects_to_annotate = ['car', 'suv']
    
    # Get API key from environment if not provided
    if api_key is None:
        api_key = validate_environment()
    
    # Prepare the payload for the Scale API
    payload = {
        'callback_url': callback_url,
        'objects_to_annotate': objects_to_annotate,
        'attachment': attachment,
        'with_labels': with_labels,
        'instruction': instruction,
        'attachment_type': attachment_type
    }

    # Set headers for the request
    headers = {"Content-Type": "application/json"}

    try:
        # Make the HTTP request to Scale API
        print(f"Sending request to Scale API with payload: {json.dumps(payload, indent=2)}")
        
        task_request = requests.post(
            "https://api.scale.com/v1/task/polygonannotation",
            json=payload,
            headers=headers,
            auth=(api_key, ''),
            timeout=30  # Add timeout to prevent hanging
        )
        
        # Check if the request was successful
        task_request.raise_for_status()
        
        # Parse the JSON response
        task_response = task_request.json()
        
        # Validate that we received a task_id
        if 'task_id' not in task_response:
            raise ValueError(f"Unexpected response format: {task_response}")
            
        return task_response
        
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please check your network connection.", file=sys.stderr)
        raise
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to Scale API. Please check your network connection.", file=sys.stderr)
        raise
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {e.response.status_code} - {e.response.text}", file=sys.stderr)
        raise
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed - {str(e)}", file=sys.stderr)
        raise
    except (KeyError, ValueError) as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        raise


def main() -> None:
    """
    Main function to create a Scale polygon annotation task.
    
    This function validates environment variables, creates a Scale task,
    and prints the resulting task ID.
    """
    # Parse command line arguments (for future extensibility)
    parser = argparse.ArgumentParser(
        description='Create a polygon annotation task using Scale API'
    )
    parser.add_argument(
        '--callback-url',
        default='https://scale-demo.herokuapp.com/scale/callback',
        help='Callback URL for Scale to send results'
    )
    parser.add_argument(
        '--objects',
        nargs='+',
        default=['car', 'suv'],
        help='Objects to annotate in the image'
    )
    parser.add_argument(
        '--image-url',
        default='https://scale.com/static/img/website/index/example-ia-boxes.jpg',
        help='URL of the image to annotate'
    )
    parser.add_argument(
        '--instruction',
        default='Draw a tight polygon around every **car** in the image.',
        help='Instructions for the annotators'
    )
    
    args = parser.parse_args()
    
    print("Starting Scale polygon annotation with S3 callback")
    
    try:
        # Create the Scale task with provided or default parameters
        task_response = create_scale_task(
            callback_url=args.callback_url,
            objects_to_annotate=args.objects,
            attachment=args.image_url,
            instruction=args.instruction
        )
        
        # Extract and display the task ID
        task_id = {'task_id': task_response['task_id']}
        print(f"Task created successfully: {task_id}")
        
        # Print additional response information if available
        if 'status' in task_response:
            print(f"Task status: {task_response['status']}")
            
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"Failed to create Scale task: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
