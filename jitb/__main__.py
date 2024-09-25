"""Entry level module for the package."""

# Standard
import sys
# Third Party
# Local
from jitb.jitb_main import main


def run_jitb() -> int:
    """Wraps the call to main() translating results into exit codes and exits."""
    return main()


if __name__ == '__main__':
    sys.exit(run_jitb())
