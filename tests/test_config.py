"""
Tests that JSON config files (tags.json) load correctly without a Discord token.
Run with: python tests/test_config.py
"""

import json
import os
import sys


def test_tags_json():
    """Verify tags.json exists and is valid JSON containing a dict."""
    tags_path = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tags.json')
    )
    with open(tags_path, 'r') as f:
        tags = json.load(f)
    assert isinstance(tags, dict), "tags.json must contain a JSON object (dict)"
    print(f"tags.json OK: {len(tags)} tag(s) loaded")


if __name__ == "__main__":
    try:
        test_tags_json()
        print("All config checks passed!")
    except AssertionError as e:
        print(f"Config check failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during config check: {e}", file=sys.stderr)
        sys.exit(1)
