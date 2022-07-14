import constant

registers = bytearray()
memory = bytearray()


# Increments instruction pointer
def inc_ip():
    registers[constant.R_IP] += 1


# Returns value at instruction pointer
def at_ip():
    return memory[registers[constant.R_IP]]


# For each bit enabled in 'flag', sets the corresponding bit in the flag register to the given value
def set_flag(flag, value):
    if value:
        registers[constant.R_FL] |= flag
    else:
        registers[constant.R_FL] &= ~flag


# For the given result of an operation, sets the zero and carry flags, and returns the result kept within a byte
def operate(x):
    set_flag(constant.FL_Z, False)
    set_flag(constant.FL_C, False)

    if x == 0:
        set_flag(constant.FL_Z, True)
    elif x > 255 or x < 0:
        set_flag(constant.FL_C, True)
        return x % 256

    return x


# Loads contents of file at the given path into memory and resets registers
# TODO: Needs program data size handling
def load(path):
    global registers, memory
    registers = bytearray(7)
    memory = bytearray(256)

    registers[constant.R_SP] = 0xFF
    with open(path, 'rb') as f:
        i = 0
        while byte := f.read(1):
            memory[i] = int.from_bytes(byte, 'big')
            i += 1


# Executes one pass of instruction; returns zero if the program should continue
def execute():
    match memory[registers[constant.R_IP]]:
        # Halt opcode
        case constant.OP_HLT:
            return 1

        # Move opcodes
        case constant.OP_MOV_R_R:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = registers[at_ip()]
            inc_ip()
        case constant.OP_MOV_R_M:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = memory[at_ip()]
            inc_ip()
        case constant.OP_MOV_R_I:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = at_ip()
            inc_ip()
        case constant.OP_MOV_M_R:
            inc_ip()
            d = at_ip()
            inc_ip()
            memory[d] = registers[at_ip()]
            inc_ip()
        case constant.OP_MOV_M_I:
            inc_ip()
            d = at_ip()
            inc_ip()
            memory[d] = at_ip()
            inc_ip()

        # Increment and decrement register opcodes
        case constant.OP_INC_R:
            inc_ip()
            registers[at_ip()] += 1
            inc_ip()
        case constant.OP_DEC_R:
            inc_ip()
            registers[at_ip()] -= 1
            inc_ip()

        # Add to register opcodes
        case constant.OP_ADD_R_R:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] + registers[at_ip()])
            inc_ip()
        case constant.OP_ADD_R_M:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] + memory[at_ip()])
            inc_ip()
        case constant.OP_ADD_R_I:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] + at_ip())
            inc_ip()

        # Subtract from register opcodes
        case constant.OP_SUB_R_R:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] - registers[at_ip()])
            inc_ip()
        case constant.OP_SUB_R_M:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] - memory[at_ip()])
            inc_ip()
        case constant.OP_SUB_R_I:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] - at_ip())
            inc_ip()

        # Bitwise AND opcodes
        case constant.OP_AND_R_R:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] & registers[at_ip()])
            inc_ip()
        case constant.OP_AND_R_M:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] & memory[at_ip()])
            inc_ip()
        case constant.OP_AND_R_I:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] & at_ip())
            inc_ip()

        # Bitwise OR opcodes
        case constant.OP_OR_R_R:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] | registers[at_ip()])
            inc_ip()
        case constant.OP_OR_R_M:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] | memory[at_ip()])
            inc_ip()
        case constant.OP_OR_R_I:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] | at_ip())
            inc_ip()

        # Bitwise XOR opcodes
        case constant.OP_XOR_R_R:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] ^ registers[at_ip()])
            inc_ip()
        case constant.OP_XOR_R_M:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] ^ memory[at_ip()])
            inc_ip()
        case constant.OP_XOR_R_I:
            inc_ip()
            d = at_ip()
            inc_ip()
            registers[d] = operate(registers[d] ^ at_ip())
            inc_ip()

        # Equality comparison opcodes
        case constant.OP_CMP_R_R:
            inc_ip()
            a = registers[at_ip()]
            inc_ip()
            operate(a - registers[at_ip()])
            inc_ip()
        case constant.OP_CMP_R_M:
            inc_ip()
            a = registers[at_ip()]
            inc_ip()
            operate(a - memory[at_ip()])
            inc_ip()
        case constant.OP_CMP_R_I:
            inc_ip()
            a = registers[at_ip()]
            inc_ip()
            operate(a - at_ip())
            inc_ip()

        # Instruction jump opcodes
        case constant.OP_JMP_I:
            inc_ip()
            registers[constant.R_IP] = at_ip()

    return 0


# Program entry point: loads then steps through program at a given path
def run(path):
    load(path)
    while execute() == 0:
        print(registers)
    print(registers)
