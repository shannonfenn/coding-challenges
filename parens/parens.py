close_open_map = {
    ')': '(',
    ']': '[',
    '}': '{',
}


def check_validity(s: str) -> bool:
    """
    Assumptions:
     - non-parenthetical chars in s can be ignored
    """
    stack = []

    open_set = set(close_open_map.values())

    for c in s:
        if c in open_set:
            # append open parens
            stack.append(c)
        elif c in close_open_map:
            # check close parens
            if not stack:
                # no open parens on the stack -> this close paren is unmatched
                return False
            top = stack.pop()
            expected = close_open_map[c]
            if top != expected:
                # there is an open paren on the top but it doesn't match ours
                return False
    # eos: if the stack has open parens then they are unmatched, otherwise s is valid
    return not stack
