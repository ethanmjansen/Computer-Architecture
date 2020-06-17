"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.sp = 7
        self.reg[self.sp] = 0xf4

        self.branch_table = {
             0b10000010: self.LDI,
             0b01000111: self.PRN,
             0b00000001: self.HLT,
             0b10100010: self.MUL,
             0b01000101: self.PUSH,
             0b01000110: self.POP
        }
        

    def load(self):
        """Load a program into memory."""

        filename = sys.argv[1]
        
        # TODO: error checking on sys.argv
        address = 0

        with open(filename, 'r') as f:

            for line in f:

                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    
                    continue

                self.ram[address] = int(line, 2)
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]

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
        """mar = Memory Address Register"""

        return self.ram[mar]

    
    def ram_write(self, mar, mdr):
        """mdr = Memory Data Register"""

        self.ram[mar] = mdr


    def LDI(self, a=None, b=None):
        """Load Register Immediate"""

        self.reg[a] = b
        self.pc += 3


    def PRN(self, a=None, b=None):
        """Print"""

        print(self.reg[a])
        self.pc += 2


    def HLT(self, a=None, b=None):
        """Halt"""

        self.running = False


    def MUL(self, a=None, b=None):
        """Multiply"""

        self.alu('MUL', a, b)
        self.pc += 3


    def PUSH(self, a=None, b=None):
        """Add to the Stack."""

        self.reg[self.sp] -= 1 # decrement sp

        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]

        top_of_stack_addr = self.reg[self.sp]

        self.ram[top_of_stack_addr] = value

        self.pc += 2


    def POP(self, a=None, b=None):
        """Take off the top of the Stack."""

        top_of_stack_addr = self.reg[self.sp]

        value = self.ram[top_of_stack_addr]

        reg_num = self.ram[self.pc +1]
        self.reg[reg_num] = value

        self.reg[self.sp] += 1 # increment sp

        self.pc += 2


    def run(self):
        """Run the CPU."""

        while self.running:

            IR = self.ram_read(self.pc) # Instruction Register

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.branch_table[IR](operand_a, operand_b)
