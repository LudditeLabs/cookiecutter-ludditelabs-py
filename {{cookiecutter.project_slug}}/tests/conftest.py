from pathlib import Path

from dotenv import load_dotenv

# pytest_plugins = "conftest_plugins"


def pytest_plugin_registered(plugin, manager):
    # Load tests settings.
    load_dotenv(Path(__file__).parent / "settings.env")


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks a test as slow")
    config.addinivalue_line("markers", "integration: marks a test as integration")
    config.addinivalue_line("markers", "skip_in_ci: skip a test in CI")
