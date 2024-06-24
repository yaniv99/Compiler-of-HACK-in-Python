import sys
#gets the console argument
#inp = sys.argv[1]
inp = input("Enter a file name: ")


#if it's C type there is 3 functions
#1. getting the instruction's dest field
def dest(line,dest_table):
        return  dest_table[line]

#2. getting the instruction's comp field
def comp(line,comp_table):
        return comp_table[line]

#3. getting the instruction's jump field
def jump(line,jump_table):
        return jump_table[line]

#write the binary of the c instruction by the order
def c_ins_write_to_file(dest_str,comp_str,jump_str, output_file):
        if dest_str == "":
                dest_str="000"
        if jump_str == "":
                jump_str="000"
        output_file.write("111")
        output_file.write(comp_str)
        output_file.write(dest_str)
        output_file.write(jump_str)
        output_file.write("\n")

# all the binary value of jump
def jump_ins_table():
        return {
                "null": "000",
                "JGT": "001",
                "JEQ": "010",
                "JGE": "011",
                "JLT": "100",
                "JNE": "101",
                "JLE": "110",
                "JMP": "111"
        }

#all the binary value of ALU output
def comp_ins_table():
        return {
                "0": "0101010",
                "1": "0111111",
                "-1": "0111010",
                "D": "0001100",
                "A": "0110000",
                "!D": "0001101",
                "!A": "0110001",
                "-D": "0001111",
                "-A": "0110011",
                "D+1": "0011111",
                "A+1": "0110111",
                "D-1": "0001110",
                "A-1": "0110010",
                "D+A": "0000010",
                "D-A": "0010011",
                "A-D": "0000111",
                "D&A": "0000000",
                "D|A": "0010101",
                "M": "1110000",
                "!M": "1110001",
                "-M": "1110011",
                "M+1": "1110111",
                "M-1": "1110010",
                "D+M": "1000010",
                "D-M": "1010011",
                "M-D": "1000111",
                "D&M": "1000000",
                "D|M": "1010101",
        }

#all the binary value of dest
def dest_ins_table():
        return {
                "null": "000",
                "M": "001",
                "D": "010",
                "MD": "011",
                "A": "100",
                "AM": "101",
                "AD": "110",
                "ADM": "111",
        }

#all the pre defined symbols of hack
def preDefinedSymbols():
        return {
                "R0": 0,
                "R1": 1,
                "R2": 2,
                "R3": 3,
                "R4": 4,
                "R5": 5,
                "R6": 6,
                "R7": 7,
                "R8": 8,
                "R9": 9,
                "R10": 10,
                "R11": 11,
                "R12": 12,
                "R13": 13,
                "R14": 14,
                "R15": 15,
                "SCREEN": 16384,
                "KBD": 24576,
                "SP": 0,
                "LCL": 1,
                "ARG": 2,
                "THIS": 3,
                "THAT": 4
        }


#add symbol to the symbols table 
def addEntry(table,symbol,bit_num):
        table[symbol] = bit_num



#check if a given symbol is already in the symbols table    
def contains(table,symbol,num):
        if table.get(symbol) is None:
                addEntry(table,symbol,num)
                return 1 #add 1 to the bit_num in main
        return 0


#get a value from the symbols table by a given key(symbol)
def getValue(symbol,table):
        return int(table[symbol])

#check if the comment is after the instruction
#return the index where the comment start
def commentOnLineEnd(line):
        if line.count("//") != 0:
                return line.index("//")
        return -1



#check if the line is blanc, comment or instruction
def whatType(line):
        ret=""
        new_line = line.strip(" \t")
        ind = commentOnLineEnd(new_line)
        # if it's no blank
        if new_line:
                if new_line.strip(" ")[0] == "@":
                        ret="A_ins"
                elif new_line.strip(" ")[0] == "(":
                        ret="L_ins"
                elif new_line.strip(" ")[0] == "/":
                        ret="comment"
                elif new_line.strip(" ")[0] == "\n":
                        ret = "blank"
                else:
                        ret="C_ins"
        return ret,ind

#return the string between parenthesis
def inParenthesis(line):
        temp=line.index(")")
        return line[1:temp]

#deal with the A instructions
def a_ins(line,table,write_file):
        #if the A instruction contain a number
        t_num=0
        try:
                num = int(line)
                binary_convertor(num,write_file)
        # if the A instruction contain a symbol
        except ValueError:
                t_num = getValue(line,table)
                binary_convertor(t_num,write_file)

#check if the instruction is symbol or a number
def what_the_A_ins(line, table, bit_value):
        if line.isnumeric():
                return 0
        else:
                return contains(table,line,bit_value)


#convert a given line to binary and write it into a file
def binary_convertor(num,write_file):
        bin_num=0
        i = 0
        while num > 0:
                bin_num = bin_num + (num%2)*(10**i)
                num//=2
                i+=1
        bin_num = ("%016d\n"%bin_num)
        write_file.write(bin_num)
        return bin_num




def main():

        line_cnt = 0
        bit_value = 16
        table = preDefinedSymbols()
        dest_table = dest_ins_table()
        comp_table = comp_ins_table()
        jump_table = jump_ins_table()
        sym=""
        ind=-1
        c_ind1=0
        c_ind2=0
        finel_dest=""
        finel_comp=""
        finel_jump=""
        write_file = inp.replace(".asm",".hack")
        with open(inp,'r') as input_file, open(write_file, "w") as output_file:
                #first iteration to count the instruction's lines and add to symbols table
                for line in input_file:
                        line=line.strip(" \t")
                        t=whatType(line) #t=(ret,int)
                        if not(t[1]==0 or t[0]=="blank" or t[0]=="L_ins"):
                                line_cnt+=1
                        if t[0] == "L_ins":
                                sym = inParenthesis(line)
                                contains(table, sym, line_cnt)

                #back to the start of the file
                input_file.seek(0)
                # second iteration to calculate instructions into binary and write to file
                for line in input_file:
                        finel_dest=""
                        finel_jump=""
                        line = line.strip(" \t\n")
                        t = whatType(line)  # t=(ret,int)
                        ind = commentOnLineEnd(line)  # to know where the parenthesis start
                        if ind != -1:
                                line = line[:ind].strip(" \t\n")      
                        if t[0] == "A_ins":
                                #ind = commentOnLineEnd(line)  # to know where the parenthesis start
                                #line = line[:ind].strip(" \t\n")
                                bit_value += what_the_A_ins(line[1:], table, bit_value)
                                a_ins(line[1:],table,output_file)
                        if t[0]=="C_ins":
                                if line.count("=") != 0:
                                        c_ind1 = line.index("=")
                                        finel_dest = dest(line[:c_ind1],dest_table)
                                if line.count(";") != 0:
                                        c_ind2 = line.index(";")
                                        finel_jump = jump(line[c_ind2 + 1:],jump_table)
                                        if line.count("=") == 0:
                                                finel_comp = comp(line[:c_ind2],comp_table) #if it's comp;jmp
                                        else:
                                                finel_comp = comp(line[c_ind1+1:c_ind2],comp_table) #if it's dest=comp;jmp
                                #there isn't jump instruction(dest=comp)
                                if line.count("=")!=0 and line.count(";") == 0: 
                                        finel_comp = comp(line[c_ind1+1:],comp_table)
                                c_ins_write_to_file(finel_dest,finel_comp,finel_jump,output_file)

main()