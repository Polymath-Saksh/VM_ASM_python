import sys
#Take input from command line while execution
input_file = sys.argv[1]

class VMTranslator:
    

    def __init__(self):#Constructor
        self.asm_code = []  
        self.jump_count = 0
        self.current_function = ''

    
    def translate(self, vm_code):
        ARITHMETIC_COMMANDS=['add','sub','neg','eq','gt','lt','and','or','not']
        BRANCHING_COMMANDS=['label','goto','if-goto']
        lines = vm_code.split('\n') #Splitting lines
        for line in lines: #Traversing lines
            line = line.strip() #Remove leading and trailing spaces
            if line and not line.startswith('//'): #Line is command and not comment
                tokens = line.split(' ')
                command = tokens[0]

                if command == 'push':
                    segment = tokens[1]
                    index = tokens[2]
                    self.translate_push(segment, index)

                elif command == 'pop':
                    segment = tokens[1]
                    index = tokens[2]
                    self.translate_pop(segment, index)

                elif command in ARITHMETIC_COMMANDS:
                    self.translate_arithmetic(command)
                elif command in BRANCHING_COMMANDS:
                    self.translate_branching(command, tokens[1])
    
    def translate_push(self, segment, index):
        if segment == 'constant':
            self.asm_code.append(f'@{index}')
            self.asm_code.append('D=A')
        else:
            segment_pointer = self.get_segment_pointer(segment, index)
            self.asm_code.append(f'@{segment_pointer}')
            if segment in ('temp', 'pointer', 'static'):
                self.asm_code.append('D=M')
            else:
                self.asm_code.append('D=M')
                self.asm_code.append(f'@{index}')
                self.asm_code.append('A=D+A')
                self.asm_code.append('D=M')

        self.push_d_to_stack()

    def translate_pop(self, segment, index):
        segment_pointer = self.get_segment_pointer(segment, index)
        self.asm_code.append(f'@{segment_pointer}')
        if segment in ('temp', 'pointer', 'static'):
            self.asm_code.append('D=A')
        else:
            self.asm_code.append('D=M')
            self.asm_code.append(f'@{index}')
            self.asm_code.append('D=D+A')

        self.asm_code.append('@R13')
        self.asm_code.append('M=D')

        self.pop_stack_to_d()

        self.asm_code.append('@R13')
        self.asm_code.append('A=M')
        self.asm_code.append('M=D')

    def get_segment_pointer(self, segment, index):
        if segment == 'local':
            return 'LCL'
        elif segment == 'argument':
            return 'ARG'
        elif segment == 'this':
            return 'THIS'
        elif segment == 'that':
            return 'THAT'
        elif segment == 'temp':
            return 'R5'
        elif segment == 'pointer':
            return 'R3' if index == 'this' else 'R4'
        elif segment == 'static':
            return f'STATIC.{index}'
        
    
    def translate_arithmetic(self, command):
        if command == 'add':
            self.pop_stack_to_d()
            self.asm_code.append('A=A-1')
            self.asm_code.append('M=D+M')
        elif command == 'sub':
            self.pop_stack_to_d()
            self.asm_code.append('A=A-1')
            self.asm_code.append('M=M-D')
        elif command == 'neg':
            self.asm_code.append('A=A-1')
            self.asm_code.append('M=-M')
        elif command == 'eq':
            self.translate_comparison('JEQ')
        elif command == 'gt':
            self.translate_comparison('JGT')
        elif command == 'lt':
            self.translate_comparison('JLT')
        elif command == 'and':
            self.pop_stack_to_d()
            self.asm_code.append('A=A-1')
            self.asm_code.append('M=D&M')
        elif command == 'or':
            self.pop_stack_to_d()
            self.asm_code.append('A=A-1')
            self.asm_code.append('M=D|M')
        elif command == 'not':
            self.asm_code.append('A=A-1')
            self.asm_code.append('M=!M')
    
    def translate_comparison(self, jump_type):
        self.jump_count += 1
        jump_label = f'JUMP{self.jump_count}'
        end_label = f'END{self.jump_count}'
        
        self.pop_stack_to_d()
        self.asm_code.append('A=A-1')
        self.asm_code.append('D=M-D')
        self.asm_code.append(f'@{jump_label}')
        self.asm_code.append(f'D;{jump_type}')
        self.asm_code.append('@0')
        self.asm_code.append('D=A')
        self.asm_code.append(f'@{end_label}')
        self.asm_code.append('0;JMP')
        self.asm_code.append(f'({jump_label})')
        self.asm_code.append('D=-1')
        self.asm_code.append(f'({end_label})')
        self.asm_code.append('@0')
        self.asm_code.append('A=A-1')
        self.asm_code.append('M=D')
    
    def push_d_to_stack(self):
        self.asm_code.append('@SP')
        self.asm_code.append('A=M')
        self.asm_code.append('M=D')
        self.asm_code.append('@SP')
        self.asm_code.append('M=M+1')
    
    def pop_stack_to_d(self):
        self.asm_code.append('@SP')
        self.asm_code.append('M=M-1')
        self.asm_code.append('A=M')
        self.asm_code.append('D=M')
    
    def translate_branching(self, command, label):
        if command == 'label':
            self.asm_code.append(f'({label})')
        elif command == 'goto':
            self.asm_code.append(f'@({label})')
            self.asm_code.append('0;JMP')
        elif command == 'if-goto':
            self.pop_stack_to_d()
            self.asm_code.append(f'@({label})')
            self.asm_code.append('D;JNE')

    def get_asm_code(self):
        return '\n'.join(self.asm_code)
    


def fileinput(filepath='Main.vm'):
    with open(filepath,'r') as file:
        lines = file.readlines()
        content=''.join(lines)
    return content

translator=VMTranslator()
translator.translate(fileinput(input_file))
asm=translator.get_asm_code()

output_file = "out.asm"
with open(output_file, "w") as file:
    file.write(asm)
    file.write("(END)\n")
    file.write("@END\n")
    file.write("0;JMP\n")

print(asm)
print('VM to ASM translation successfully done!\n Output file: out.asm')
