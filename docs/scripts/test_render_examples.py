import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import render_examples


class RenderPageTests(unittest.TestCase):
    def test_fence_is_longer_than_every_backtick_run(self):
        cases = [
            ("", 3),
            ("print('hello')\n", 3),
            ("`", 3),
            ("``", 3),
            ("```", 4),
            ("````", 5),
            ("````````", 9),
            ("`inline`\n````\n```\n``````\n``\n", 7),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            src = root / "example.py"
            with patch.object(render_examples, "REPO_DIR", root):
                for code, fence_length in cases:
                    with self.subTest(code=code):
                        src.write_text(code)
                        page = render_examples._render_page(
                            src, "Example", "python", "example", "Python SDK"
                        )
                        fence = "`" * fence_length
                        expected_block = (
                            f"\n{fence}python\n"
                            + code.rstrip("\n")
                            + f"\n{fence}\n\nSource: "
                        )
                        self.assertIn(expected_block, page)


if __name__ == "__main__":
    unittest.main()
