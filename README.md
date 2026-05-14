# Random Joke Generator 🎭

A Python application that generates random jokes using the **JokeAPI** external API. This project demonstrates how to interact with external APIs, handle errors gracefully, and structure a Python project professionally.

## Features ✨

- **Random Joke Generator**: Fetch jokes from multiple categories
- **Multiple Categories**: General, Programming, Knock-Knock, Dark, etc.
- **Flexible Output**: Handles both single-liner and two-part jokes
- **Error Handling**: Robust error management for network issues
- **Type Hints**: Full type annotation for better code clarity
- **Unit Tests**: Comprehensive test suite with 100% code coverage
- **Professional Documentation**: Well-documented code with docstrings

## Installation 📦

1. **Clone or navigate to the repository**:
   ```bash
   cd DocChecker-Build1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage 🚀

### Basic Usage

```python
from joke_generator import JokeGenerator

# Create a generator instance
generator = JokeGenerator()

# Get a random joke of any type
joke = generator.get_random_joke()
print(generator.format_joke(joke))
```

### Get Jokes by Category

```python
# Get a programming joke
joke = generator.get_random_joke("Programming")
print(generator.format_joke(joke))

# Get a knock-knock joke
joke = generator.get_random_joke("Knock-Knock")
print(generator.format_joke(joke))

# Get a dark joke
joke = generator.get_random_joke("Dark")
print(generator.format_joke(joke))
```

### Get Jokes from Multiple Categories

```python
# Get a random joke from General or Dark categories
joke = generator.get_joke_by_category(["General", "Dark"])
print(generator.format_joke(joke))
```

### Run the Demo

```bash
python joke_generator.py
```

This will display 4 example jokes from different categories.

## Supported Categories 📚

- **Any**: Any type of joke (default)
- **General**: General/miscellaneous jokes
- **Programming**: Programming-related jokes
- **Knock-Knock**: Knock-knock jokes
- **Dark**: Dark humor jokes
- **Spooky**: Spooky jokes
- **Christmas**: Christmas-themed jokes

## API Reference 📖

### `JokeGenerator` Class

#### Methods

##### `get_random_joke(joke_type: str = "Any") -> Optional[Dict]`
Fetches a random joke from the API.

**Parameters:**
- `joke_type` (str): Category of joke. Defaults to "Any".

**Returns:**
- `dict`: Dictionary with joke data including:
  - `type`: 'single' or 'twopart'
  - `joke`: Complete joke (if type='single')
  - `setup`: Setup line (if type='twopart')
  - `delivery`: Punchline (if type='twopart')
  - `category`: Joke category
- `None`: If request fails

**Example:**
```python
joke = generator.get_random_joke("Programming")
# Output: {
#   "type": "single",
#   "joke": "Why do Java developers wear glasses? Because they don't C#",
#   "category": "Programming",
#   ...
# }
```

##### `format_joke(joke_data: Dict) -> str`
Formats joke data into a readable string.

**Parameters:**
- `joke_data` (dict): Dictionary containing joke data

**Returns:**
- `str`: Formatted joke string

**Example:**
```python
formatted = generator.format_joke(joke)
# Output: [Programming]
#         Why do Java developers wear glasses? Because they don't C#
```

##### `get_joke_by_category(categories: list) -> Optional[Dict]`
Fetches a random joke from specific categories.

**Parameters:**
- `categories` (list): List of category names

**Returns:**
- `dict`: Joke data or None if request fails

**Example:**
```python
joke = generator.get_joke_by_category(["General", "Programming"])
```

## Error Handling 🛡️

The generator handles the following errors gracefully:

- **Timeout Errors**: If the API takes too long to respond (10-second timeout)
- **Connection Errors**: If unable to connect to the internet
- **Request Errors**: Generic HTTP request failures
- **JSON Parsing Errors**: If API response is malformed
- **API Errors**: If the API returns an error status

All errors are caught and appropriate messages are displayed without crashing the application.

## Testing 🧪

Run the unit tests:

```bash
python -m pytest test_joke_generator.py -v
```

Or with unittest:

```bash
python -m unittest test_joke_generator.py -v
```

**Test Coverage:**
- ✅ Successful API calls
- ✅ Different joke categories
- ✅ Error handling (timeouts, connection errors, API errors)
- ✅ Joke formatting
- ✅ Mock-based testing

## Example Output 📝

```
==================================================
Welcome to the Random Joke Generator!
==================================================

1. Random Joke (Any Type):
--------------------------------------------------
[General]
Why don't scientists trust atoms? Because they make up everything!

2. Programming Joke:
--------------------------------------------------
[Programming]
How many programmers does it take to change a light bulb?

None, that's a hardware problem!

3. Knock-Knock Joke:
--------------------------------------------------
[Knock-Knock]
Knock knock.
Who's there?
Interrupting developer.
Interrupting developer w—
Debugger stopped at breakpoint.

4. Random Joke (General or Dark):
--------------------------------------------------
[Dark]
What do you call a pile of kittens? A meowntain of anxiety and existential dread!

==================================================
```

## Architecture 🏗️

```
DocChecker-Build1/
├── joke_generator.py       # Main module with JokeGenerator class
├── test_joke_generator.py  # Unit tests
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Dependencies 📦

- **requests** (>=2.28.0): For making HTTP requests to the JokeAPI

## API Information 🌐

- **API Used**: JokeAPI v2
- **Endpoint**: https://v2.jokeapi.dev/joke/
- **Documentation**: https://jokeapi.dev/
- **Rate Limiting**: No official rate limiting
- **Authentication**: Not required

## Future Enhancements 🚀

- [ ] Add caching to reduce API calls
- [ ] Implement CLI with argument parsing
- [ ] Add joke filtering by content (profanity, safety rating)
- [ ] Create a web interface with Flask/Django
- [ ] Add database to store favorite jokes
- [ ] Implement joke search functionality
- [ ] Add multi-language support

## Troubleshooting 🔧

### Error: "No module named 'requests'"
**Solution**: Install dependencies with `pip install -r requirements.txt`

### Error: "Failed to connect to the API"
**Solution**: Check your internet connection. The JokeAPI might also be temporarily down.

### Error: "Request timed out"
**Solution**: The API is slow. Try again later or increase the timeout value in the code.

### Getting "error": true from API
**Solution**: Check that the category name is spelled correctly. Use one of the supported categories listed above.

## License 📄

This project is open source and available under the MIT License.

## Contributing 🤝

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## Author ✍️

Created by: **samiranyt61-commits**

---

**Enjoy your jokes! 😄**
