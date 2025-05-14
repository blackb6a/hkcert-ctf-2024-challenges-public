# compile: python -m compileall sser.py

import marshal, dis
from types import CodeType

f = open("__pycache__/sser.cpython-312.pyc", "rb")

s = f.read()

f.close()

magic = s[:16]
code: CodeType = marshal.loads(s[16:])

print(code.co_code)


# modify:
import opcode

co_code = code.co_code

payload = [
    # opcode.opmap["LOAD_CONST"],
    # 124,
    # opcode.opmap["POP_TOP"],
    # 0,
    
    opcode.opmap["LOAD_CONST"],
    4,
    opcode.opmap["CALL_INTRINSIC_1"],
    1,
    opcode.opmap["POP_TOP"],
    0,
]
payload2 = [opcode.opmap["BUILD_STRING"], 0]
co_code = (
    co_code[:38] + bytes(payload) + co_code[38:48] + bytes(payload2) + co_code[50:]
)

import random

print(code.co_varnames)
code2 = CodeType(
    code.co_argcount,
    code.co_posonlyargcount,
    code.co_kwonlyargcount,
    code.co_nlocals,
    code.co_stacksize,
    code.co_flags,
    co_code,
    code.co_consts,
    code.co_names,
    code.co_varnames,
    code.co_filename,
    code.co_name,
    code.co_qualname,
    code.co_firstlineno,
    # code.co_linetable,
    b'\0', # pylingual disabler
    code.co_exceptiontable,
    code.co_freevars,
    code.co_cellvars,
)

# print(dis.dis(code2))
f = open("sser.cpython-312.pyc", "wb")
s = marshal.dumps(code2)
f.write(magic)
f.write(s)
f.close()
