"""
Random Joke Generator using JokeAPI
This module provides functionality to fetch random jokes from an external API.
"""

import requests
import json
from typing import Dict, Optional


class JokeGenerator:
    """A class to generate random jokes using the JokeAPI."""
    
    BASE_URL = "https://v2.jokeapi.dev/joke"
    
    def __init__(self):
        """Initialize the JokeGenerator with API configuration."""
        self.timeout = 10  # Request timeout in seconds
    
    def get_random_joke(self, joke_type: str = "Any") -> Optional[Dict]:
        """
        Fetch a random joke from the API.
        
        Args:
            joke_type (str): Type of joke - "Any", "General", "Knock-Knock", "Programming", "Dark"
                           Defaults to "Any" which returns any type of joke.
        
        Returns:
            dict: A dictionary containing the joke data with keys:
                  - 'type': 'single' for one-liner jokes, 'twopart' for setup-delivery
                  - 'joke': The complete joke (if type is 'single')
                  - 'setup': The setup (if type is 'twopart')
                  - 'delivery': The punchline (if type is 'twopart')
                  - 'category': The joke category
                  Returns None if the request fails.
        
        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        try:
            url = f"{self.BASE_URL}/{joke_type}"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if the API returned an error
            if data.get("error"):
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return None
            
            return data
        
        except requests.exceptions.Timeout:
            print("Error: Request timed out. The API took too long to respond.")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Failed to connect to the API. Check your internet connection.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch joke - {str(e)}")
            return None
        except json.JSONDecodeError:
            print("Error: Failed to parse API response.")
            return None
    
    def format_joke(self, joke_data: Dict) -> str:
        """
        Format the joke data into a readable string.
        
        Args:
            joke_data (dict): The joke data dictionary from the API.
        
        Returns:
            str: A formatted joke string.
        """
        if not joke_data:
            return "Could not retrieve a joke."
        
        category = joke_data.get("category", "Unknown")
        joke_type = joke_data.get("type", "unknown")
        
        if joke_type == "single":
            joke_text = joke_data.get("joke", "No joke available")
            return f"[{category}]\n{joke_text}"
        
        elif joke_type == "twopart":
            setup = joke_data.get("setup", "")
            delivery = joke_data.get("delivery", "")
            return f"[{category}]\n{setup}\n\n{delivery}"
        
        else:
            return "Unknown joke format."
    
    def get_joke_by_category(self, categories: list) -> Optional[Dict]:
        """
        Fetch a random joke from specific categories.
        
        Args:
            categories (list): List of categories. Example: ["General", "Programming"]
        
        Returns:
            dict: Joke data or None if request fails.
        """
        try:
            category_string = ",".join(categories)
            url = f"{self.BASE_URL}/{category_string}"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("error"):
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return None
            
            return data
        
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch joke - {str(e)}")
            return None


def main():
    """Main function to demonstrate the JokeGenerator."""
    print("=" * 50)
    print("Welcome to the Random Joke Generator!")
    print("=" * 50)
    
    generator = JokeGenerator()
    
    # Get a random joke of any type
    print("\n1. Random Joke (Any Type):")
    print("-" * 50)
    joke = generator.get_random_joke()
    print(generator.format_joke(joke))
    
    # Get a programming joke
    print("\n2. Programming Joke:")
    print("-" * 50)
    joke = generator.get_random_joke("Programming")
    print(generator.format_joke(joke))
    
    # Get a knock-knock joke
    print("\n3. Knock-Knock Joke:")
    print("-" * 50)
    joke = generator.get_random_joke("Knock-Knock")
    print(generator.format_joke(joke))
    
    # Get a joke from multiple categories
    print("\n4. Random Joke (General or Dark):")
    print("-" * 50)
    joke = generator.get_joke_by_category(["General", "Dark"])
    print(generator.format_joke(joke))
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
