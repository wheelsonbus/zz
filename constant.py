class C:
    # Opcode enumeration
    OP_HLT = 0x00  # Halts the program
    OP_MOV_R_R = 0x01  # Moves value to register from register
    OP_MOV_R_M = 0x02  # ...to register from memory address
    OP_MOV_R_I = 0x03  # ...to register from immediate
    OP_MOV_M_R = 0x04  # ...to memory address from register
    OP_MOV_M_I = 0x05  # ...to memory address from immediate
    OP_INC_R = 0x06  # Increments register by 1
    OP_DEC_R = 0x07  # Decrements register by 1
    OP_ADD_R_R = 0x08  # Adds value of register to destination register (first operand)
    OP_ADD_R_M = 0x09  # ...of memory address to destination register
    OP_ADD_R_I = 0x0A  # ...of immediate to destination register
    OP_SUB_R_R = 0x0B  # Subtracts value of register from destination register (first operand)
    OP_SUB_R_M = 0x0C  # ...of memory address from destination register
    OP_SUB_R_I = 0x0D  # ...of immediate from destination register
    OP_AND_R_R = 0x0E  # Bitwise-ANDs value of register with destination register (first operand)
    OP_AND_R_M = 0x0F  # ...of memory address with destination register
    OP_AND_R_I = 0x10  # ...of immediate with destination register
    OP_OR_R_R = 0x11  # Bitwise-ORs value of register with destination register (first operand)
    OP_OR_R_M = 0x12  # ...of memory address with destination register
    OP_OR_R_I = 0x13  # ...of immediate with destination register
    OP_XOR_R_R = 0x14  # Bitwise-XORs value of register with destination register (first operand)
    OP_XOR_R_M = 0x15  # ...of memory address with destination register
    OP_XOR_R_I = 0x16  # ...of immediate with destination register
    OP_NOT_R = 0x17  # Bitwise-NOTs value of register
    OP_CMP_R_R = 0x18  # Sets zero flag to true if values of register and register are equal
    OP_CMP_R_M = 0x19  # ...of register and memory address are equal
    OP_CMP_R_I = 0x1A  # ...of register and immediate are equal
    OP_JMP_I = 0x1B  # Unconditionally jumps to instruction at given address
    OP_JZ_I = 0x1C  # Jumps if zero flag is true (equal)
    OP_JNZ_I = 0x1D  # Jumps if zero flag is false (not equal)
    OP_JC_I = 0x1E  # Jumps if carry flag is true (lower than)
    OP_JNC_I = 0x1F  # Jumps if carry flag is false (not lower than)
    OP_JA_I = 0x20  # Jumps if neither carry nor zero flag is true (greater than)
    OP_JNA_I = 0x21  # Jumps if either carry or zero flag is true (not greater than)
    # TODO: Needs conditional jump and stack management operations
    # TODO: Call and return operations?

    # Register enumeration
    R_A = 0x0
    R_B = 0x1
    R_C = 0x2
    R_D = 0x3
    R_IP = 0x4
    R_SP = 0x5
    R_FL = 0x6
    R_HA = 0x7
    # TODO: Higher address byte register for expanded memory?

    # Flag register bits
    FL_Z = 1 << 0
    FL_C = 1 << 1
    FL_ERR = 1 << 2
