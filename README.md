# Minecraft Username Availability Checker

<p align="center">
![mcnametoolbanner](https://github.com/user-attachments/assets/f22f043d-3568-4f0a-8786-01d1bac38323)
</p>

This Python script allows you to check the availability of Minecraft usernames using the Mojang API. It provides various options for inputting usernames and displays the results in a user-friendly format.

## Features

- Check availability of Minecraft usernames
- Multiple input methods:
  - Manual entry
  - Read from file
  - Generate random usernames
  - Generate maximum usernames for a specific length
- Concurrent API requests for faster checking
- Progress bars for username generation and checking
- Colorful console output for better readability

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - colorama
  - tqdm

## Installation

1. Clone this repository or download the script.
2. Install the required packages:

pip install requests colorama tqdm

## Usage

Run the script using Python:

python mcname_2.0.py

Follow the on-screen prompts to choose your preferred method of inputting usernames and view the results.

## Options

1. **Enter usernames manually**: Type in usernames separated by spaces.
2. **Read usernames from a file**: Provide a filename containing usernames (one per line).
3. **Generate random usernames**: Specify the number and length of usernames to generate.
4. **Generate maximum usernames for a specific length**: Choose a username length (1-6) to generate all possible combinations.
5. **Exit**: Quit the program.

## Output

The script will display:
- Total usernames checked
- Number of unavailable usernames
- Number of available usernames
- List of available usernames (if any)

## Notes

- The script uses the Mojang API, which may have rate limits. Use responsibly.
- Generated usernames are limited to lowercase letters (a-z) to comply with Minecraft username rules.

## License

This project is open-source and available under the MIT License.
