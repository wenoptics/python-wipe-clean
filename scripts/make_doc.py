import importlib
import inspect
import re
import sys
import textwrap
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from marko import Markdown
from marko.ext.toc import Toc

CUR_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = (CUR_DIR / '..').resolve()

env = Environment(
    loader=FileSystemLoader(CUR_DIR/'templates'),
    autoescape=False  # Autoscaping will mess up the example code block
)


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


def make_toc(md_txt: str) -> str:
    """
    Return the 1st-level of table of content of a given Markdown text.

    Return example:
    <p>
    <a href="#install">Install</a> • <a href="#usages">Usages</a> • <a href="#advanced-usages">Advanced usages</a>
     • <a href="#roadmap">Roadmap</a> • <a href="#related-projects">Related projects</a>
    </p>
    """
    opening = "<p>"
    closing = "</p>"
    item_format = '<a href="#{slug}">{text}</a>'

    markdown = Markdown(extensions=[Toc(opening, closing, item_format)])
    markdown(md_txt)
    ret: str = markdown.renderer.render_toc(maxdepth=1)

    # Insert separators
    sep = ' &#8226; '  # This is a dot char
    ret = re.sub(r'</a>\s*<a', f'</a>{sep}<a', ret)
    return ret


def render_readme() -> str:
    tpl_file = CUR_DIR / 'templates' / 'README.md.j2'

    template = env.get_template("README.md.j2")
    with tpl_file.open() as f:
        tpl = f.read()

    ret = template.render(**{
        'toc': make_toc(tpl),
        'test_readme_examples': extract_examples()
    })

    header = '''
    <!-- -------------------------------------------------------------

    README.md is auto-generated. DO NOT MODIFY THIS FILE MANUALLY.
    
    --------------------------------------------------------------- -->
    '''  # noqa: W293
    return textwrap.dedent(header) + '\n\n' + ret


if __name__ == '__main__':

    # with (PROJECT_ROOT / 'README.preview.md').open('w') as _:
    with (PROJECT_ROOT / 'README.md').open('w') as _:
        _.write(render_readme())
