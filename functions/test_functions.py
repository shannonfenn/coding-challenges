import pytest

from functions.functions import FunctionDefinition, get_function_definitions

test_cases = [
    # Test case 1: Multiple functions at the same level
    (
        ['def func1(', ')', 'def func2(', ')'],
        [FunctionDefinition('func1', 1, 2), FunctionDefinition('func2', 3, 4)],
    ),
    # Test case 2: Nested functions with body content
    (
        [
            'def outer(',
            '  def inner(',
            "    print('inner')",
            '  )',
            "  print('outer')",
            ')',
        ],
        [FunctionDefinition('outer', 1, 6), FunctionDefinition('inner', 2, 4)],
    ),
    # Test case 3: Function with lines before and after
    (
        ["print('start')", 'def func(', "  print('func')", ')', "print('end')"],
        [FunctionDefinition('func', 2, 4)],
    ),
    # Test case 4: Empty source
    ([], []),
    # Test case 5: Source with no functions
    (["print('hello')", "print('world')"], []),
    # Test case 6: Function with extra spaces
    (['  def func1(  ', '  )  '], [FunctionDefinition('func1', 1, 2)]),
    # Test case 7: Function name with underscores
    (['def my_func2(', ')'], [FunctionDefinition('my_func2', 1, 2)]),
    # Test case 8: Multiple levels of nesting
    (
        [
            'def outer(',
            '  def inner1(',
            "    print('inner1')",
            '  )',
            '  def inner2(',
            '    def inner3(',
            "      print('inner3')",
            '    )',
            "    print('inner2')",
            '  )',
            "  print('outer')",
            ')',
        ],
        [
            FunctionDefinition('outer', 1, 12),
            FunctionDefinition('inner1', 2, 4),
            FunctionDefinition('inner2', 5, 10),
            FunctionDefinition('inner3', 6, 8),
        ],
    ),
    # Test case 9: Nested and sequential functions at the same level
    (
        ['def a(', '  def b(', '  )', '  def c(', '  )', ')'],
        [
            FunctionDefinition('a', 1, 6),
            FunctionDefinition('b', 2, 3),
            FunctionDefinition('c', 4, 5),
        ],
    ),
    # Test case 10: Functions with code between them
    (
        ['def func(', ')', 'some code', 'def func2(', ')'],
        [FunctionDefinition('func', 1, 2), FunctionDefinition('func2', 4, 5)],
    ),
]


@pytest.mark.parametrize('source, expected', test_cases)
def test_get_function_definitions(source, expected):
    result = get_function_definitions(source)
    # returned list can be in any order
    assert sorted(result, key=lambda fd: fd.start_line) == sorted(
        expected, key=lambda fd: fd.start_line
    )
