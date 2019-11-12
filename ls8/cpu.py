"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #memory - 256 bits
        self.memory = [0] * 256
        #general purpose register
        self.reg = [0] * 8
        #program counter
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            #self.ram[address] = instruction
            
            self.memory[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, mar):
        """
        Should accept the address to read and return the value stored there
        mar = memory address register -> contains the address that is being read or written to 
        MAR will be passed in, will retrun MDR
        mdr = contains the data that was read or the data to write
        """
        value = self.memory[mar]
        return value

    def ram_write(self, mar, mdr):
        """
        Should accept a value to write, and the address to write it to
        mar = memory address register -> contains the address that is being read or written to 
        mdr = memory data register -> contains the data that was read or the data to write
        """
        #memory at the passed in address is not the passed in value to be written
        self.memory[mar] = mdr
    def run(self):
        """
        Run the CPU
        """
        #* Ends CPU operations
        HLT = 0b00000001
        #* Sets a specified register to a specified value, 3 byte instruction
        LDI = 0b10000010
        #* Prints the value of a register - 2 byte instruction
        PRN = 0b01000111

        #Loop flag
        halted = False

        while not halted:
            #store the insturction --- at current(pc) of list in memory
            instruction = self.memory[self.pc]
            #if instruction is halt, then exit
            if instruction == HLT:
                halted = True
                
                self.pc += 1
            #LDI takes LDI command, register, value
            elif instruction == LDI:
                reg_num = self.memory[self.pc + 1]
                value = self.memory[self.pc + 2]
                self.reg[reg_num] = value

                self.pc += 3
            elif instruction == PRN:
                #PC at current is the command(PRN, or 3 in this case) pc + 1 is the operands for command
                reg_num = self.memory[self.pc + 1]
                print(self.reg[reg_num])

                self.pc += 2
            

            #catch all
            else:
                print(f"Uknown instruction at indexd {self.pc}")
                halted = True

