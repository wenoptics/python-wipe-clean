import importlib
import inspect
import re
import sys
import textwrap
from pathlib import Path

CUR_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = (CUR_DIR / '..').resolve()


def extract_examples():
    """Extract example code from the unit tests"""

    test_cases = [
        'test_cli_usage',
        'test_example_brush',
        'test_example_path',
    ]

    file_name = 'test_readme_examples'
    py_file = PROJECT_ROOT / 'tests' / f'{file_name}.py'
    assert py_file.is_file()

    # This looks anti-pattern but it gets the job done.
    sys.path.append(str(py_file.parent))
    imported_tests = importlib.import_module(file_name)

    pattern = getattr(imported_tests, 'EXTRACTION_PATTERN')

    ret = {}
    for case in test_cases:
        case_fn = getattr(imported_tests, case)

        # Get source code from the function
        code_str = inspect.getsource(case_fn)

        # Extract the example block
        example_block = re.search(pattern, code_str, re.DOTALL)
        if not example_block:
            raise RuntimeError('No extraction point matched.')
        example_block = example_block.group(1)

        ret[case] = textwrap.dedent(example_block).strip()

    return ret


if __name__ == '__main__':
    import pprint

    _ = extract_examples()
    pprint.pprint(_)
    assert len(_) == 3
