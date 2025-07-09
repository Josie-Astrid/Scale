#!/usr/bin/env python3
"""
Simple unit tests for ScalePolygonAnnotation.py

This test file validates the core functionality of the Scale polygon annotation script
without requiring actual API calls.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add the current directory to the path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ScalePolygonAnnotation import validate_environment, create_scale_task


class TestScalePolygonAnnotation(unittest.TestCase):
    """Test cases for Scale polygon annotation functionality."""

    def test_validate_environment_with_api_key(self):
        """Test that validate_environment returns API key when set."""
        with patch.dict(os.environ, {'SCALE_API_KEY': 'test_api_key'}):
            api_key = validate_environment()
            self.assertEqual(api_key, 'test_api_key')

    def test_validate_environment_without_api_key(self):
        """Test that validate_environment exits when API key is not set."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                validate_environment()

    @patch('ScalePolygonAnnotation.requests.post')
    def test_create_scale_task_success(self, mock_post):
        """Test successful task creation."""
        # Mock successful response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'task_id': 'test_task_123'}
        mock_post.return_value = mock_response

        result = create_scale_task(api_key='test_api_key')
        
        self.assertEqual(result['task_id'], 'test_task_123')
        mock_post.assert_called_once()

    @patch('ScalePolygonAnnotation.requests.post')
    def test_create_scale_task_http_error(self, mock_post):
        """Test handling of HTTP errors."""
        # Mock HTTP error response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            create_scale_task(api_key='test_api_key')

    def test_create_scale_task_default_parameters(self):
        """Test that default parameters are properly set."""
        with patch('ScalePolygonAnnotation.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {'task_id': 'test_task_123'}
            mock_post.return_value = mock_response

            create_scale_task(api_key='test_api_key')
            
            # Check that the call was made with correct default parameters
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            
            self.assertEqual(payload['objects_to_annotate'], ['car', 'suv'])
            self.assertEqual(payload['with_labels'], True)
            self.assertEqual(payload['attachment_type'], 'image')


if __name__ == '__main__':
    unittest.main()