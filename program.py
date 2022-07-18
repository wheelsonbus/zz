import os

from constant import *


class Program:
    def __init__(self, path):
        self.registers = bytearray(8)
        self.memory = bytearray(256 * 256)
        self.load(path)

    # Increments instruction pointer
    def inc_ip(self):
        self.registers[C.R_IP] += 1

    # Returns value at instruction pointer
    def at_ip(self):
        return self.memory[self.registers[C.R_IP]]

    # Gets bit value of flag register given by 'flag'
    # TODO: Needs handling for flag input with multiple bits enabled
    def get_flag(self, flag):
        return self.registers[C.R_FL] & flag != 0

    # For each bit enabled in 'flag', sets the corresponding bit in the flag register to the given value
    def set_flag(self, flag, value):
        if value:
            self.registers[C.R_FL] |= flag
        else:
            self.registers[C.R_FL] &= ~flag

    # Returns value at given memory address
    def fetch(self, x):
        return self.memory[self.registers[C.R_HA] + x]

    # For the given result of an operation, sets the zero and carry flags, and returns the result clamped within a byte
    def operate(self, x):
        self.set_flag(C.FL_Z, False)
        self.set_flag(C.FL_C, False)

        if x == 0:
            self.set_flag(C.FL_Z, True)
        elif x > 255 or x < 0:
            self.set_flag(C.FL_C, True)
            return x % 256

        return x

    # Jumps to given address if legal
    def jump(self, address):
        if 0 <= address < 256:
            self.registers[C.R_IP] = address
        else:
            self.throw('Attempted to jump to invalid address: ' + address)

    # Throws an error
    def throw(self, s):
        print(s)
        self.set_flag(C.FL_ERR, True)

        for x in range(0xf000, 0x10000):
            print(self.memory[x], end='')

    # Loads contents of file at the given path into memory and resets registers
    # TODO: Needs program data size handling
    def load(self, path):
        self.registers = bytearray(8)
        self.memory = bytearray(256 * 256)

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
                self.registers[d] = self.fetch(self.at_ip())
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
                self.memory[self.registers[C.R_HA] + d] = self.registers[self.at_ip()]
                self.inc_ip()
            case C.OP_MOV_M_I:
                self.inc_ip()
                d = self.at_ip()
                self.inc_ip()
                self.memory[self.registers[C.R_HA] + d] = self.at_ip()
                self.inc_ip()

            # Increment and decrement register opcodes
            case C.OP_INC_R:
                self.inc_ip()
                r = self.at_ip()
                self.registers[r] = self.operate(self.registers[r] + 1)
                self.inc_ip()
            case C.OP_DEC_R:
                self.inc_ip()
                r = self.at_ip()
                self.registers[r] = self.operate(self.registers[r] - 1)
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
                self.registers[d] = self.operate(self.registers[d] + self.fetch(self.at_ip()))
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
                self.registers[d] = self.operate(self.registers[d] - self.fetch(self.at_ip()))
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
                self.registers[d] = self.operate(self.registers[d] & self.fetch(self.at_ip()))
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
                self.registers[d] = self.operate(self.registers[d] | self.fetch(self.at_ip()))
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
                self.registers[d] = self.operate(self.registers[d] ^ self.fetch(self.at_ip()))
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
                self.operate(a - self.fetch(self.at_ip()))
                self.inc_ip()
            case C.OP_CMP_R_I:
                self.inc_ip()
                a = self.registers[self.at_ip()]
                self.inc_ip()
                self.operate(a - self.at_ip())
                self.inc_ip()

            # Jump opcodes
            case C.OP_JMP_I:
                self.inc_ip()
                self.jump(self.at_ip())
            case C.OP_JZ_I:
                self.inc_ip()
                if self.get_flag(C.FL_Z):
                    self.jump(self.at_ip())
                else:
                    self.inc_ip()
            case C.OP_JNZ_I:
                self.inc_ip()
                if not self.get_flag(C.FL_Z):
                    self.jump(self.at_ip())
                else:
                    self.inc_ip()
            case C.OP_JC_I:
                self.inc_ip()
                if self.get_flag(C.FL_C):
                    self.jump(self.at_ip())
                else:
                    self.inc_ip()
            case C.OP_JNC_I:
                self.inc_ip()
                if not self.get_flag(C.FL_C):
                    self.jump(self.at_ip())
                else:
                    self.inc_ip()
            case C.OP_JA_I:
                self.inc_ip()
                if not (self.get_flag(C.FL_Z) or self.get_flag(C.FL_C)):
                    self.jump(self.at_ip())
                else:
                    self.inc_ip()
            case C.OP_JNA_I:
                self.inc_ip()
                if self.get_flag(C.FL_Z) or self.get_flag(C.FL_C):
                    self.jump(self.at_ip())
                else:
                    self.inc_ip()

        return self.registers[C.R_FL] & C.FL_ERR != 0

    # Program entry point: loads then steps through program at a given path
    def run(self):
        while self.step() == 0:
            print(self.registers)
