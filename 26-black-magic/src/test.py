from ctypes import sizeof, POINTER, py_object
# opname is a list of opcode names, where the indexes are the opcode numbers
from opcode import opname
import sys 

# The offset we found using dwarfdump
F_STACKTOP = 64

def get_stack(frame):
    # Getting the address of the stack by adding
    # the address of the frame and the offset of the member
    f_stacktop_addr = id(frame) + F_STACKTOP
    # Initializing a PyObject** directly from memory using ctypes
    return POINTER(py_object).from_address(f_stacktop_addr)
from opcode import opmap
count = 0
def tracefunc(frame, event, arg):
    global count
    count += 1
    # print(frame)
    frame.f_trace_opcodes = True
    opcode = frame.f_code.co_code[frame.f_lasti]
    print(opcode)
    if opcode == opmap["SWAP"]:
        print(get_stack(frame)[-4])
    if event == 'opcode':
        # frame.f_code.co_code is the raw bytecode
        opcode = frame.f_code.co_code[frame.f_lasti]
        stack = get_stack(frame.f_frame)
        # According to the implementation of BINARY_ADD,
        # the last two items in the stack should be the addition operands
        print(stack[-1])
    return tracefunc

sys.settrace(tracefunc)
import a
