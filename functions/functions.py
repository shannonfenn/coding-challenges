from dataclasses import dataclass


@dataclass
class FunctionDefinition:
    name: str
    start_line: int
    end_line: int | None = None

    def is_valid(self) -> bool:
        return self.end_line is not None and self.end_line >= self.start_line


def get_function_definitions(source: list[str]) -> list[FunctionDefinition]:
    """
    Assumptions:
     - syntactically valid code
     - no leading or trailing whitespace
     - function definitions end with (
     - only one function definition per line
    """
    stack = []
    results = []

    for i, line in enumerate(source):
        line_no = i + 1
        line = line.strip()
        if line.startswith('def '):
            name = line[4:-1]
            stack.append(FunctionDefinition(name=name, start_line=line_no))
        else:
            for c in line:
                if c == '(':
                    # append open parens
                    stack.append(c)
                elif c == ')':
                    # check close parens
                    if not stack:
                        # no open parens/funcs on the stack -> this close paren is unmatched
                        raise ValueError(f'Unmatched parenthesis on line {line_no}')
                    top = stack.pop()
                    if top != '(':
                        # handle function def
                        top.end_line = line_no
                        results.append(top)
    # eof: if stack is non-empty then we have unmatched open parens
    if stack:
        raise ValueError(f'Unmatched open parentheses. Final stack contents: {stack}')

    return results
