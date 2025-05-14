from types import CodeType
from opcode import opmap, _nb_ops

import importlib

# def test_oob():
#     class MockBuiltins(dict):
#         def __getitem__(self, k):
#             if type(k) == str:
#                 return k

#     # LOAD_CONST
#     # LOAD_NAME co_names
#     # LOAD_FAST co_varnames
#     # LOAD_DEREF fast local stack
#     import sys
#     n = int(sys.argv[1])
#     code = [
#         *([opmap["EXTENDED_ARG"], n // 256] if n // 256 != 0 else []),
#         opmap["LOAD_FAST"],
#         n % 256,
#         opmap["RETURN_VALUE"],
#         0,
#     ]

#     c = CodeType(
#         0,
#         0,
#         0,
#         0,
#         0,
#         3,
#         bytes(code),
#         (),
#         (),
#         (),
#         "<sandbox>",
#         "<eval>",
#         "",
#         0,
#         b"",
#         b"",
#         (),
#         (),
#     )

#     ret = eval(c, {"__builtins__": MockBuiltins()})
#     if ret:
#         print(f"{n}: {ret}")
#     return ret
import opcode

PRELOAD_INDEX = [6]
STACK_SIZE = 0

PRELOAD_STACK = {
    "_frozen_importlib_external": 0
}


def debug_stack(count = 100):
    INTRINSIC_PRINT = 1
    return [
        # opmap["FORMAT_VALUE"], 0,
        opmap["CALL_INTRINSIC_1"], INTRINSIC_PRINT,
        opmap["POP_TOP"], 0
    ] * count

def get_zero():
    return [
        # *module__frozen_importlib_external(),
        opmap["BUILD_TUPLE"], 0,
        opmap["GET_LEN"], 0,
        opmap["SWAP"], 2,
        opmap["POP_TOP"], 0,
    ]

def get_one():
    return [
        *get_zero(),
        opmap["UNARY_INVERT"], 0,
        opmap["UNARY_NEGATIVE"], 0,
    ]

def get_int(i):
    if i == 0:
        return get_zero()
    if i == 1:
        return get_one()
    
    is_neg = False
    if i < 0:
        is_neg = True
        n = bin(-i)[2:]
    else:
        n = bin(i)[2:]
    payload = []
    if n[0] == "0":
        payload.extend(get_zero())
    else:
        payload.extend(get_one())

    # import dis

    for k in n[1:]:
        # << 1
        payload.extend([
            *get_one(),
            opmap["BINARY_OP"], 3, 0, 0
        ])
        
        # print(payload)
        # print(dis.dis(bytes(payload)))
        if k == "1":
            # +1
            payload.extend([
                *get_one(),
                opmap["BINARY_OP"], 0, 0, 0
            ])
    if is_neg:
        payload.extend([
            opmap["UNARY_NEGATIVE"], 0
        ])
    return payload

def get_true():
    return [
        *get_zero(),
        opmap["UNARY_NOT"], 0,
    ]

def get_false():
    return [
        *get_one(),
        opmap["UNARY_NOT"], 0,
    ]


def get_set_char():
    return [
        opmap["BUILD_SET"], 0,
        opmap["FORMAT_VALUE"], 0,
        *get_zero(),
        *get_int(3),
        opmap["BUILD_SLICE"], 2,
        opmap["BINARY_SUBSCR"], 0, 0, 0
    ]

# charset:
# True
# False
# 0123456789
# -
# set()
# , from tuple

# dir

def get_locals():
    return [
        opmap["LOAD_LOCALS"], 0
    ]

def get_builtins():
    return [
        *get_locals(),
        opmap["FORMAT_VALUE"], 1,
        *get_int(195),
        *get_int(207),
        opmap["BUILD_SLICE"], 2,
        opmap["BINARY_SUBSCR"], 0, 0, 0,
        opmap["STORE_DEREF"], 7,
        *get_locals(),
        opmap["LOAD_DEREF"], 7,
        opmap["BINARY_SUBSCR"], 0, 0, 0
    ]

def get_fn_from_builtins(fnname):
    return [

    ]


# [('NB_ADD', '+'), ('NB_AND', '&'), ('NB_FLOOR_DIVIDE', '//'), ('NB_LSHIFT', '<<'), ('NB_MATRIX_MULTIPLY', '@'), ('NB_MULTIPLY', '*'), ('NB_REMAINDER', '%'), ('NB_OR', '|'), ('NB_POWER', '**'), ('NB_RSHIFT', '>>'), ('NB_SUBTRACT', '-'), ('NB_TRUE_DIVIDE', '/'), ('NB_XOR', '^'), ('NB_INPLACE_ADD', '+='), ('NB_INPLACE_AND', '&='), ('NB_INPLACE_FLOOR_DIVIDE', '//='), ('NB_INPLACE_LSHIFT', '<<='), ('NB_INPLACE_MATRIX_MULTIPLY', '@='), ('NB_INPLACE_MULTIPLY', '*='), ('NB_INPLACE_REMAINDER', '%='), ('NB_INPLACE_OR', '|='), ('NB_INPLACE_POWER', '**='), ('NB_INPLACE_RSHIFT', '>>='), ('NB_INPLACE_SUBTRACT', '-='), ('NB_INPLACE_TRUE_DIVIDE', '/='), ('NB_INPLACE_XOR', '^=')]
def get_num_char(c: str):
    assert len(c) == 1
    return [
        *get_int(int(c)),
        opmap["FORMAT_VALUE"], 1,
    ]

def get_true_char(c: str):
    assert len(c) == 1
    assert c in 'True'
    pos = 'True'.find(c)
    return [
        *get_true(),
        opmap["FORMAT_VALUE"], 1,
        *get_int(pos),
        opmap["BINARY_SUBSCR"], 0, 0, 0,
    ]

def get_false_char(c: str):
    assert len(c) == 1
    assert c in 'False'
    pos = 'False'.find(c)
    return [
        *get_false(),
        opmap["FORMAT_VALUE"], 1,
        *get_int(pos),
        opmap["BINARY_SUBSCR"], 0, 0, 0,
    ]


LOCALS_PREFIX = "{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourcelessFileLoader object at 0x74b8b55bb6b0>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': '/"
LOCALS_SUFFIX = ".pyc', '__cached__': None}"
def get_char_from_locals(c: str):
    assert len(c) == 1
    assert c in LOCALS_PREFIX or c in LOCALS_SUFFIX
    pos = LOCALS_PREFIX.find(c)
    if pos == -1:
        pos = len(LOCALS_SUFFIX) - LOCALS_SUFFIX.find(c)
        pos = 291 - pos
    return [
        *get_locals(),
        opmap["FORMAT_VALUE"], 1,
                        # opmap["COPY"], 1,
                        # *debug_stack(1),
        *get_int(pos),
        opmap["BINARY_SUBSCR"], 0, 0, 0,
    ]

def get_str(target: str):
    mapper = {
        '0123456789': get_num_char,
        'True': get_true_char,
        'False': get_false_char,
        LOCALS_SUFFIX: get_char_from_locals,
        LOCALS_PREFIX: get_char_from_locals,
    }
    
    payload = []
    start = True
    for c in target:
        done = False
        for k in mapper:
            if c in k:
                payload.extend(mapper[k](c))
                if start:
                    start = False
                else:
                    payload.extend([
                        # opmap["COPY"], 1,
                        # *debug_stack(1),
                        opmap["LOAD_DEREF"], 7,
                        opmap["SWAP"], 2,
                        opmap["BUILD_STRING"], 2,
                    ])
                payload.extend([
                    opmap["STORE_DEREF"], 7,
                ])
                done = True
                break
        if not done:
            msg = f"NotImplemented: do not have a way to construct {c}"
            raise Exception(msg)
    payload.extend([
        opmap["LOAD_DEREF"], 7,
    ])
    # size = len(target)
    # # payload.extend([
    # #     *([opmap["EXTENDED_ARG"], size // 256] if size // 256 != 0 else []),
    # #     opmap["BUILD_STRING"],
    # #     size % 256
    # # ])
    return payload

def checkflag_char(char, ind):
    payload = [
        *get_str(char),
        *get_int(ind),
        opmap["LOAD_DEREF"], 10,
        opmap["SWAP"], 2,
        opmap["BINARY_SUBSCR"], 0, 0, 0,
        opmap["COMPARE_OP"], 40, 0, 0,
        opmap["POP_JUMP_IF_TRUE"], 2,
        # fail case:
        opmap["EXTENDED_ARG"], 255,
        opmap["JUMP_BACKWARD"], 255,
        # opmap["CALL_INTRINSIC_1"], 0,
        # true case:
        # *get_str("1234")
        
    ]
    return payload


import sys
def checkflag():
    payload = [
        opmap["STORE_DEREF"], 10,
    ]
    flag = "hkcert24{u_r_r34l_py7h0n1c_by43c0d3_m4st3r}"

    for i in range(len(flag)):
        payload += checkflag_char(flag[i], i)

    payload += [
        *get_str("you passed"),
        *debug_stack(1),
    ]

    return payload

# def get_builtins_key(key):
#     return [
#         *module__frozen_importlib_external(),
#         *get_str(key),
#         opmap["BINARY_SUBSCR"], 0, 0, 0
#     ]


def build_prog():
    # insts = [
    #     opmap["PUSH_NULL"], 0,
    #     *get_builtins_key("print"),
    #     *get_builtins_key("print"),
    #     opmap["RETURN_VALUE"], 0
    # ]

    import sys


    # test

    n = int(sys.argv[1])
    insts = [
        # *presetup_stack(),
        
        # *get_str("_1234", 0),
        # *([opmap["EXTENDED_ARG"], n // 256] if n // 256 != 0 else []),
        # opmap["LOAD_CONST"], n % 256,



        *get_str('input'),
        opmap["STORE_DEREF"], 7,
        opmap["LOAD_DEREF"], 9,
        opmap["LOAD_DEREF"], 7,
        opmap["BINARY_SUBSCR"], 0, 0, 0,
        opmap["PUSH_NULL"], 0,
        opmap["SWAP"], 2,
        opmap["CALL"], 0, 0, 0, 0, 0, 0, 0, 0, 0,
        # opmap["STORE_NAME"], 9,
        # opmap["COPY"], 1,
        # opmap["SWAP"], 2,

        # linear structures
        *checkflag(),

        # *get_str("no"),
        # opmap["COPY"], 2,
        # opmap["STORE_FAST"], 99,

        # opmap["LOAD_FAST"], 99,
        # opmap["LOAD_FAST"], 99,

        # opmap["POP_TOP"], 0,
        # opmap["STORE_DEREF"], 7,
        # opmap["PUSH_NULL"], 0,
        # opmap["LOAD_DEREF"], 7,
        
        
        # *get_builtins(),
        # opmap["BUILD_TUPLE"], 1,
        # *get_str("print"),

        # opmap["STORE_FAST"], 100,
        # opmap["PUSH_NULL"], 0,
        # opmap["LOAD_FAST"], 100,
        # opmap["LOAD_FAST"], 99,
        # opmap["CALL"], 2,
        
        
        
        # *get_str('dir'),
        # opmap["CALL_INTRINSIC_1"], 2,
        # opmap["STORE_NAME"], int(sys.argv[1]),
        # *get_builtins(),
        # opmap["LOAD_ATTR"], int(sys.argv[1]),

        # opmap["COPY"], 1,
        # *get_locals(),

        # opmap["LOAD_FAST"], 10,
        # opmap["LOAD_FAST"], 37,
        # opmap["STORE_NAME"], 4,
        # opmap["LOAD_NAME"], 4,
        # *get_set_char(),
        # *get_int(70),
        # *get_int(71),
        # opmap["BUILD_STRING"], 2,
        # *module__frozen_importlib_external(),
        # opmap["BUILD_SET"], 0,
        # opmap["FORMAT_VALUE"], 0,
        # opmap["BINARY_SUBSCR"], 0, 0, 0,
        # *get_one(),
        # opmap["BINARY_OP"], 0,

        # *debug_stack(2),
        # *debug_stack(),
        opmap["RETURN_VALUE"], 0
    ]

    print(int(sys.argv[1]))

    return bytes(insts)

# ret = test_oob()

payload = build_prog()
code = CodeType(0, 0, 0, 0, 0, 0, payload, (), (), (), "", "", "", 0, b"\0", b"", (), ())

import dis
print(dis.dis(payload))

pyc_data = importlib._bootstrap_external._code_to_timestamp_pyc(code)

with open('a.pyc', 'wb') as f:
    f.write(pyc_data)
