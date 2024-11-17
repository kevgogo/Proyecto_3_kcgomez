import unittest
import os

def run_tests_from_directory(test_dir):
    """Function to discover and run tests from a specific directory."""
    # Discover tests in the specified directory
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern="test_*.py")  # Match test files that start with "test_"
    
    # Run the discovered test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    test_directory = './tests'  # Update this with the folder path where your test files are located
    run_tests_from_directory(test_directory)
