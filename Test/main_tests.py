import unittest
from pathlib import Path


def main():
    test_dir = Path(__file__).resolve().parent

    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=str(test_dir),
        pattern="*_tests.py",
        top_level_dir=str(test_dir.parent)
    )

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    main()