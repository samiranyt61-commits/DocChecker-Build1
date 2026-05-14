"""
Unit tests for the Random Joke Generator
Tests cover all functionality including API calls, error handling, and formatting.
"""

import unittest
from unittest.mock import patch, MagicMock
import requests
from joke_generator import JokeGenerator


class TestJokeGenerator(unittest.TestCase):
    """Test cases for the JokeGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = JokeGenerator()
    
    # Tests for get_random_joke
    
    @patch('joke_generator.requests.get')
    def test_get_random_joke_success(self, mock_get):
        """Test successful retrieval of a random joke."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "single",
            "joke": "Why don't scientists trust atoms? Because they make up everything!",
            "category": "General"
        }
        mock_get.return_value = mock_response
        
        result = self.generator.get_random_joke()
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "single")
        self.assertIn("joke", result)
    
    @patch('joke_generator.requests.get')
    def test_get_programming_joke(self, mock_get):
        """Test retrieval of a programming joke."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "single",
            "joke": "Why do Java developers wear glasses? Because they don't C#",
            "category": "Programming"
        }
        mock_get.return_value = mock_response
        
        result = self.generator.get_random_joke("Programming")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["category"], "Programming")
    
    @patch('joke_generator.requests.get')
    def test_get_twopart_joke(self, mock_get):
        """Test retrieval of a two-part joke."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "twopart",
            "setup": "Why did the developer go broke?",
            "delivery": "Because they lost their cache!",
            "category": "Programming"
        }
        mock_get.return_value = mock_response
        
        result = self.generator.get_random_joke("Programming")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "twopart")
        self.assertIn("setup", result)
        self.assertIn("delivery", result)
    
    @patch('joke_generator.requests.get')
    def test_get_random_joke_timeout(self, mock_get):
        """Test handling of timeout errors."""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        result = self.generator.get_random_joke()
        
        self.assertIsNone(result)
    
    @patch('joke_generator.requests.get')
    def test_get_random_joke_connection_error(self, mock_get):
        """Test handling of connection errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        result = self.generator.get_random_joke()
        
        self.assertIsNone(result)
    
    @patch('joke_generator.requests.get')
    def test_get_random_joke_request_exception(self, mock_get):
        """Test handling of generic request exceptions."""
        mock_get.side_effect = requests.exceptions.RequestException("Generic error")
        
        result = self.generator.get_random_joke()
        
        self.assertIsNone(result)
    
    @patch('joke_generator.requests.get')
    def test_get_random_joke_api_error(self, mock_get):
        """Test handling of API errors."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "error": True,
            "message": "Invalid category"
        }
        mock_get.return_value = mock_response
        
        result = self.generator.get_random_joke("InvalidCategory")
        
        self.assertIsNone(result)
    
    @patch('joke_generator.requests.get')
    def test_get_random_joke_json_decode_error(self, mock_get):
        """Test handling of JSON decode errors."""
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        result = self.generator.get_random_joke()
        
        self.assertIsNone(result)
    
    # Tests for format_joke
    
    def test_format_single_joke(self):
        """Test formatting of a single-liner joke."""
        joke_data = {
            "type": "single",
            "joke": "Why don't scientists trust atoms? Because they make up everything!",
            "category": "General"
        }
        
        result = self.generator.format_joke(joke_data)
        
        self.assertIn("[General]", result)
        self.assertIn("Why don't scientists trust atoms?", result)
    
    def test_format_twopart_joke(self):
        """Test formatting of a two-part joke."""
        joke_data = {
            "type": "twopart",
            "setup": "Why did the developer go broke?",
            "delivery": "Because they lost their cache!",
            "category": "Programming"
        }
        
        result = self.generator.format_joke(joke_data)
        
        self.assertIn("[Programming]", result)
        self.assertIn("Why did the developer go broke?", result)
        self.assertIn("Because they lost their cache!", result)
    
    def test_format_none_joke(self):
        """Test formatting when joke_data is None."""
        result = self.generator.format_joke(None)
        
        self.assertEqual(result, "Could not retrieve a joke.")
    
    def test_format_unknown_type_joke(self):
        """Test formatting with unknown joke type."""
        joke_data = {
            "type": "unknown",
            "category": "General"
        }
        
        result = self.generator.format_joke(joke_data)
        
        self.assertIn("Unknown joke format", result)
    
    # Tests for get_joke_by_category
    
    @patch('joke_generator.requests.get')
    def test_get_joke_by_category_success(self, mock_get):
        """Test retrieval of joke by specific categories."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "single",
            "joke": "A joke from selected categories",
            "category": "General"
        }
        mock_get.return_value = mock_response
        
        result = self.generator.get_joke_by_category(["General", "Programming"])
        
        self.assertIsNotNone(result)
        self.assertIn("joke", result)
    
    @patch('joke_generator.requests.get')
    def test_get_joke_by_category_error(self, mock_get):
        """Test error handling in get_joke_by_category."""
        mock_get.side_effect = requests.exceptions.RequestException("Error")
        
        result = self.generator.get_joke_by_category(["General"])
        
        self.assertIsNone(result)
    
    @patch('joke_generator.requests.get')
    def test_get_joke_by_category_api_error(self, mock_get):
        """Test API error handling in get_joke_by_category."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "error": True,
            "message": "Invalid input"
        }
        mock_get.return_value = mock_response
        
        result = self.generator.get_joke_by_category(["Invalid"])
        
        self.assertIsNone(result)
    
    # Tests for timeout value
    
    def test_timeout_value(self):
        """Test that timeout value is set correctly."""
        self.assertEqual(self.generator.timeout, 10)
    
    def test_base_url(self):
        """Test that base URL is set correctly."""
        self.assertEqual(self.generator.BASE_URL, "https://v2.jokeapi.dev/joke")


if __name__ == "__main__":
    unittest.main()
