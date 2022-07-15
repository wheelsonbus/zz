from constant import *


class Program:
    def __init__(self, path):
        self.registers = bytearray(8)
        self.memory = bytearray(256)
        self.load(path)

    # Increments instruction pointer
    def inc_ip(self):
        self.registers[C.R_IP] += 1

    # Returns value at instruction pointer
    def at_ip(self):
        return self.memory[self.registers[C.R_IP]]

    # For each bit enabled in 'flag', sets the corresponding bit in the flag register to the given value
    def set_flag(self, flag, value):
        if value:
            self.registers[C.R_FL] |= flag
        else:
            self.registers[C.R_FL] &= ~flag

    # For the given result of an operation, sets the zero and carry flags, and returns the result kept within a byte
    def operate(self, x):
        self.set_flag(C.FL_Z, False)
        self.set_flag(C.FL_C, False)

        if x == 0:
            self.set_flag(C.FL_Z, True)
        elif x > 255 or x < 0:
            self.set_flag(C.FL_C, True)
            return x % 256

        return x

    # Loads contents of file at the given path into memory and resets registers
    # TODO: Needs program data size handling
    def load(self, path):
        self.registers = bytearray(7)
        self.memory = bytearray(256)

        self.registers[C.R_SP] = 0xFF
        with open(path, 'rb') as f:
            i = 0
            while byte := f.read(1):
                self.memory[i] = int.from_bytes(byte, 'big')
                i += 1

    # Executes one step worth of instruction; returns zero if the program should continue
    def step(self):
        match self.memory[self.registers[C.R_IP]]:
            # Halt opcode
            case C.OP_HLT:
                return 1

            # Move opcodes
            case C.OP_MOV_R_R:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.registers[self.at_ip()]
                self.inc_ip()
            case C.OP_MOV_R_M:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.memory[self.at_ip()]
                self.inc_ip()
            case C.OP_MOV_R_I:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.at_ip()
                self.inc_ip()
            case C.OP_MOV_M_R:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.memory[d] = self.registers[self.at_ip()]
                self.inc_ip()
            case C.OP_MOV_M_I:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.memory[d] = self.at_ip()
                self.inc_ip()

            # Increment and decrement register opcodes
            case C.OP_INC_R:
                self.inc_ip()
                self.registers[self.at_ip()] += 1
                self.inc_ip()
            case C.OP_DEC_R:
                self.inc_ip()
                self.registers[self.at_ip()] -= 1
                self.inc_ip()

            # Add to register opcodes
            case C.OP_ADD_R_R:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] + self.registers[self.at_ip()])
                self.inc_ip()
            case C.OP_ADD_R_M:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] + self.memory[self.at_ip()])
                self.inc_ip()
            case C.OP_ADD_R_I:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] + self.at_ip())
                self.inc_ip()

            # Subtract from register opcodes
            case C.OP_SUB_R_R:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] - self.registers[self.at_ip()])
                self.inc_ip()
            case C.OP_SUB_R_M:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] - self.memory[self.at_ip()])
                self.inc_ip()
            case C.OP_SUB_R_I:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] - self.at_ip())
                self.inc_ip()

            # Bitwise AND opcodes
            case C.OP_AND_R_R:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] & self.registers[self.at_ip()])
                self.inc_ip()
            case C.OP_AND_R_M:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] & self.memory[self.at_ip()])
                self.inc_ip()
            case C.OP_AND_R_I:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] & self.at_ip())
                self.inc_ip()

            # Bitwise OR opcodes
            case C.OP_OR_R_R:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] | self.registers[self.at_ip()])
                self.inc_ip()
            case C.OP_OR_R_M:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] | self.memory[self.at_ip()])
                self.inc_ip()
            case C.OP_OR_R_I:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] | self.at_ip())
                self.inc_ip()

            # Bitwise XOR opcodes
            case C.OP_XOR_R_R:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] ^ self.registers[self.at_ip()])
                self.inc_ip()
            case C.OP_XOR_R_M:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] ^ self.memory[self.at_ip()])
                self.inc_ip()
            case C.OP_XOR_R_I:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.registers[d] = self.operate(self.registers[d] ^ self.at_ip())
                self.inc_ip()

            # Equality comparison opcodes
            case C.OP_CMP_R_R:
                self.inc_ip()
                a = self.registers[self.at_ip()]
                self.inc_ip()
                self.operate(a - self.registers[self.at_ip()])
                self.inc_ip()
            case C.OP_CMP_R_M:
                self.inc_ip()
                a = self.registers[self.at_ip()]
                self.inc_ip()
                self.operate(a - self.memory[self.at_ip()])
                self.inc_ip()
            case C.OP_CMP_R_I:
                self.inc_ip()
                a = self.registers[self.at_ip()]
                self.inc_ip()
                self.operate(a - self.at_ip())
                self.inc_ip()

            # Instruction jump opcodes
            case C.OP_JMP_I:
                self.inc_ip()
                self.registers[C.R_IP] = self.at_ip()

        return 0

    # Program entry point: loads then steps through program at a given path
    def run(self):
        while self.step() == 0:
            print(self.registers)
