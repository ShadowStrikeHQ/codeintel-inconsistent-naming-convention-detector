import argparse
import re
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NamingConventionDetector:
    """
    A tool to detect inconsistencies in naming conventions within Python code.
    """

    def __init__(self, filename, variable_pattern=r"^[a-z][a-z0-9_]*$", function_pattern=r"^[a-z][a-z0-9_]*$"):
        """
        Initializes the NamingConventionDetector.

        Args:
            filename (str): The path to the Python file to analyze.
            variable_pattern (str): Regex for variable naming convention. Default is snake_case.
            function_pattern (str): Regex for function naming convention. Default is snake_case.
        """
        self.filename = filename
        self.variable_pattern = variable_pattern
        self.function_pattern = function_pattern
        self.inconsistencies = []

    def detect_inconsistencies(self):
        """
        Detects naming convention inconsistencies in the given file.
        """
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            logging.error(f"File not found: {self.filename}")
            return

        for i, line in enumerate(lines):
            # Detect variables
            variable_match = re.search(r"(\w+)\s*=", line)
            if variable_match:
                variable_name = variable_match.group(1)
                if not re.match(self.variable_pattern, variable_name):
                    self.inconsistencies.append((i + 1, "Variable", variable_name))
                    logging.warning(f"Inconsistent variable name '{variable_name}' on line {i + 1}")

            # Detect functions
            function_match = re.search(r"def\s+(\w+)\s*\(", line)
            if function_match:
                function_name = function_match.group(1)
                if not re.match(self.function_pattern, function_name):
                    self.inconsistencies.append((i + 1, "Function", function_name))
                    logging.warning(f"Inconsistent function name '{function_name}' on line {i + 1}")

    def get_inconsistencies(self):
        """
        Returns the list of inconsistencies found.

        Returns:
            list: A list of tuples, where each tuple contains the line number, type (Variable/Function), and name.
        """
        return self.inconsistencies


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(description='Detects naming convention inconsistencies in Python code.')
    parser.add_argument('filename', help='The path to the Python file to analyze.')
    parser.add_argument('--variable-pattern', default=r"^[a-z][a-z0-9_]*$",
                        help='Regex for variable naming convention. Default is snake_case.')
    parser.add_argument('--function-pattern', default=r"^[a-z][a-z0-9_]*$",
                        help='Regex for function naming convention. Default is snake_case.')

    return parser


def main():
    """
    The main function of the code intelligence tool.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Input validation
    if not os.path.exists(args.filename):
        logging.error(f"Error: File '{args.filename}' not found.")
        return

    try:
        detector = NamingConventionDetector(args.filename, args.variable_pattern, args.function_pattern)
        detector.detect_inconsistencies()
        inconsistencies = detector.get_inconsistencies()

        if inconsistencies:
            print("Naming convention inconsistencies found:")
            for line_number, type, name in inconsistencies:
                print(f"Line {line_number}: {type} '{name}'")
        else:
            print("No naming convention inconsistencies found.")

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Example Usage:
    # 1. Run on a specific file: python main.py my_code.py
    # 2. Run with custom variable pattern: python main.py my_code.py --variable-pattern "^[A-Z][a-zA-Z]*$"
    # 3. Run with custom function pattern: python main.py my_code.py --function-pattern "^[A-Z][a-zA-Z]*$"
    # 4. Run with both custom patterns: python main.py my_code.py --variable-pattern "^[A-Z][a-zA-Z]*$" --function-pattern "^[A-Z][a-zA-Z]*$"
    main()