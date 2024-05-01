#Jake Kraemer
# CS 420 Final Project
# 824475048
#
# StackFuns is an esoteric programming language used to manipulate, store, print etc.
# items in a stack. StackFuns will have a first-in, last-out stack data structure that can store
# strings and integers. Two registers will be available and operations can be performed on
# these registers to manipulate items in the stack. Operations will be available for the user to
# take items from and place items into the stack. Print instructions will be available to print
# items in the stack. Loops and other control structures will be provided to perform complex
# operations on items in the stack. The languages’ goal is to simplify operations on a list of
# objects.
# 
### INIT { ... }
# EXAMPLE: INIT {'Tree', 7, 9, 'Fire'}
# This initializes the stack with the value of integers and strings within the brackets of init. 
#
### ASSIGN var = ...
# EXAMPLES: ASSIGN POINT = X, ASSIGN Z = 6 / 2 * 5 - 3, 
# These types of statements assign a value to a variable. Assignment can have multiple operators in expression.
# Assignment can have another variable in the expression.
#
### POP var | POP var POINT
# EXAMPLES: POP A POINT, POP B
# These statements will take a variable from the stack and move it to the variable given. If the POP statement includes POINT
# the value taken from the stack will be at points index. If no point is given the first item in the stack is taken. 
#
### PUSH var | PUSH var POINT
# EXAMPLES: PUSH X POINT, PUSH 'CRAZY', PUSH 22
# These statements adds a value to the stack. This can push a variables value, a string literal or a int literal to the stack. 
# If a point is given then the value is added to the stack at the points index. If no point is given the value is added to the front of the stack. 
#
### PEAK
# This statement prints the items in the stack as a comma seperated list. 

#Function varmap takes in the traget variable and the the state
def varmap(targetVar, state):
    #If target variable is in state return the value
    if targetVar in state:
        return state[targetVar]
    #If the target variable is not in map return "Var not found"
    else:
        raise ValueError("Error: Var not found")
    
def stackmap(targetVal, stack):
    if targetVal in stack:
        index = stack[targetVal]
        return stack[index]
    else:
        raise ValueError("Error: Value is not in stack")
    
def doMath(ops, digits):
    r1 = (int)(digits[0])
    r2 = (int)(digits[1])
    i = 1
    for op in ops:
        if op == "+":
           newVal = r1 + r2
        elif op == "-":
            newVal = r1 - r2
        elif op == "*":
            newVal = r1 * r2
        elif op == "/":
            newVal = int(r1 / r2)
        elif op == "%":
            newVal = r1 % r2
        try:
            i = i + 1
            r1 = newVal
            r2 = (int)(digits[i])
        except:
            continue
    return newVal

def boolMath(ops, vars):
    before_bool = []
    after_bool = []
    boolFound = False
    for k in range(len(ops)):
        if ops[k] in boolops:
            boolFound = True
            this_op = ops[k].replace("'", "")
        elif boolFound == False:
            before_bool.append(ops[k])
        elif boolFound == True:
            after_bool.append(ops[k])

    if len(before_bool) > 0:
        before_bool_value = doMath(before_bool, vars[0:(len(before_bool) + 1)])
    else:
        before_bool_value = vars[0]
    if len(after_bool) > 0:
        after_bool_value = doMath(after_bool, vars[len(before_bool) + 1: len(before_bool) + len(after_bool) + 2])
    else:
        after_bool_value = vars[len(before_bool) + 1]

    if this_op == "==":
        return (before_bool_value == after_bool_value)
    elif this_op == ">":
        return (before_bool_value > after_bool_value)
    elif this_op == "<":
        return (before_bool_value < after_bool_value)
    elif this_op == ">=":
        return (before_bool_value >= after_bool_value)
    elif this_op == "<=":
        return (before_bool_value <= after_bool_value)
    

state = dict()
stack = list()


def execute_program(program, state, stack):
    If_Over = False
    INIF = False
    pc = 0

    for line in program.splitlines():

        try:
            instruction, rest = line.split(" ", 1)
        except:
            instruction = line

        if instruction != "ELIF" and instruction != "ELSE" and INIF and instruction != "]":
            pass

        elif instruction == "IF" or instruction == "ELIF":
            
            if If_Over:
                INIF = True
                pass
            else:
                ops = []
                vars = []

                rest = rest.replace(" [", "")

                for things in rest.split(" "):
                    if things in operators or things in boolops:
                        ops.append(things)
                    elif things.isdigit():
                        vars.append(int(things))
                    elif str(state[things]).isdigit():
                        vars.append(state[things])
                    else:
                        things = things.replace("'", "")
                        vars.append(things)

                statement = boolMath(ops, vars)

                run_bracket = False

                if statement and If_Over == False:
                    If_Over = True
                    run_bracket = True

                if run_bracket:

                    this_pc = 0
                    ifBool = False
                    inBrackets = ""
                    for line in program.splitlines():
                        try:
                            instruction_copy, others = line.split(" ", 1)
                        except:
                            instruction_copy = line

                        if (instruction_copy == "IF" or instruction_copy == "ELIF") and (pc == this_pc):
                            ifBool = True
                        elif instruction_copy == "]":
                            ifBool = False
                        elif ifBool == True:
                            inBrackets = inBrackets + line + "\n"
                        
                        this_pc = this_pc + 1
                    
                    execute_program(inBrackets, state, stack)
                
                INIF = True

        elif instruction == "ELSE":
            if If_Over == False:
                this_pc = 0
                ifBool = False
                inBrackets = ""
                for line in program.splitlines():
                    try:
                        instruction_copy, others = line.split(" ", 1)
                    except:
                        instruction_copy = line

                    if instruction_copy == "ELSE" and pc == this_pc:
                        ifBool = True
                    elif instruction_copy == "]":
                        ifBool = False
                    elif ifBool == True:
                        inBrackets = inBrackets + line + "\n"
                    
                    this_pc = this_pc + 1
                
                execute_program(inBrackets, state, stack)
                If_Over = False
            
            INIF = True
            If_Over = False

        elif instruction == "INIT":
            rest = rest.replace(",", "")
            rest = rest.replace("{", "")
            rest = rest.replace("}", "")
            rest = rest.replace("'", "")
            for inits in rest.split():
                if inits.isdigit():
                    stack.append(int(inits))
                else:
                    stack.append(inits)

        elif instruction == "ASSIGN":
            ops = []
            digits = []
            var, expr = rest.split(' = ')
            for vals in expr.split(" "):
                if vals in operators:
                    ops.append(vals)
                elif vals.isdigit():
                    digits.append(vals)
                elif str(state[vals]).isdigit():
                    digits.append(state[vals])
                
            if len(digits) == 1:
                state[var] = int(digits[0])
            else:
                new_val = doMath(ops, digits)
                state[var] = new_val

        elif instruction == "POP":
            if rest.find("POINT") != -1:
                var, point = rest.split(" ")
                point = varmap("POINT", state)
                try:
                    newVal = stack[int(point)]
                    stack.pop(int(point))
                    state[var] = newVal
                except:
                    raise ValueError("POINT is out of bounds for current stack")
            else:
                newVal = stack[0]
                stack.pop(0)
                state[rest] = newVal

        elif instruction == "PUSH":
            if rest.find("POINT") != -1:
                var, point = rest.split(" ")
                point = varmap("POINT", state)
                if rest.isdigit():
                    stack.insert(point, int(rest))
                else:
                    if var in state:
                        stack.insert(point, state[var])
                    else:
                        stack.insert(point, var)
            else:
                if rest.isdigit():
                    stack.insert(0, int(rest))
                else:
                    rest = rest.replace("'", "")
                    stack.insert(0, rest)

        elif instruction == "PEAK":
            for i in range(len(stack)):
                if i != len(stack) - 1:
                    print(f"{stack[i]}, ", end = "")
                else:
                    print(stack[i])

        elif instruction == "PRINT":
            ops = []
            digits = []

            for vals in rest.split(" "):
                if vals in operators:
                    ops.append(vals)
                elif vals.isdigit():
                    digits.append(vals)
                elif vals in state:
                    digits.append(state[vals])
                else:
                    rest = rest.replace("'", "")
                    print(rest)
                    break

            if len(digits) == 1:
                print(int(digits[0]))
            elif len(digits) > 1:
                new_val = doMath(ops, digits)
                print(new_val)

        elif instruction == "FOR":
            rest = rest.replace(" {", "")
            rest = rest.replace(":", " ")
            rest = rest.replace(" IN", "")

            forVar, ranges = rest.split(" ", 1)
            start, end = ranges.split(" ")
            startMath = []
            for ops in operators:
                if start.find(ops) != -1:
                    x, y = start.split(ops)
                    if x.isdigit():
                        startMath.append(x)
                    elif x in state:
                        startMath.append(state[x])
                    if y.isdigit():
                        startMath.append(y)
                    elif y in state:
                        startMath.append(state[y])
                    start = doMath(ops, startMath)
                    break

            new_program = ""
            pc_copy = 0
            inLoop = False
            forCount  = 0
            closeBracketCount  = 0

            for line in program.splitlines():
                try:
                    instruction_copy, others = line.split(" ", 1)
                except:
                    instruction_copy = line
                
                if pc_copy == pc and instruction_copy == "FOR":
                    inLoop = True
                    forCount  = forCount + 1
                elif instruction_copy == "FOR" and pc_copy > pc:
                    forCount = forCount + 1
                elif instruction_copy == "}":
                    closeBracketCount = closeBracketCount + 1
                    if forCount == closeBracketCount:
                        inLoop = False                
                    
                if inLoop and pc != pc_copy:
                    new_program = new_program + line + "\n"

                pc_copy = pc_copy + 1

            start = int(start)
            end = int(end)
            for k in range(start, end):
                state[forVar] = k
                execute_program(new_program, state, stack)
                

        elif instruction == "]":
            INIF = False
        
        pc = pc + 1

            

                 
operators = ["+", "-", "*", "/", "%"]
boolops = ["==", "<=", ">=", ">", "<"]

program1 = """INIT {7, 'Tree', 20, 50, 'Dog'}
ASSIGN X = 2
ASSIGN Y = 6 / 2
ASSIGN Z = 6 / 2 * 5 - 3
ASSIGN POINT = X
POP A POINT
POP B
ASSIGN POINT = 1
PUSH X POINT
PUSH 'Crazy'
PUSH 22
PEAK
PRINT A
PRINT B
PRINT 30 + Y
PRINT 60
PRINT 'Cat'
"""

program2 = """INIT { }
FOR X IN 1:100 {
ASSIGN POINT = X
IF X % 15 == 0 [
PUSH 'FizzBuzz' POINT
]
ELIF X % 10 == 0 [
PUSH 'Buzz' POINT
]
ELIF X % 5 == 0 [
PUSH 'Fizz' POINT
]
ELSE [
PUSH X POINT
]
}
PEAK
"""

program3 = """INIT { }
FOR X IN 0:1 {
FOR J IN 0:2 {
PRINT 'TEST'
PRINT 'PASS'
}
}
"""

program4 = """INIT { }
ASSIGN X = 2
ASSIGN Y = 4
IF Y + 3 < X [
PRINT 'Test1'
]
ELIF X < Y [
PRINT 'test2'
]
ELSE [
PRINT 'test3'
]
PRINT 'IF test4'
"""

program5 = """INIT {4, 8, 2, 1, 0, 5}
FOR I IN 0:5 {
ASSIGN MIN_IDX = I
FOR IDX IN I+1:6 {
ASSIGN POINT = IDX
POP ARRAY_IDX POINT
ASSIGN TEMP = ARRAY_IDX
PUSH TEMP POINT
ASSIGN POINT = MIN_IDX
POP ARRAY_MIN_IDX POINT
ASSIGN TEMP = ARRAY_MIN_IDX
PUSH TEMP POINT
IF ARRAY_IDX < ARRAY_MIN_IDX [
ASSIGN MIN_IDX = IDX
]
}
ASSIGN POINT = I
POP ARRAY_I POINT
ASSIGN TEMP = ARRAY_I
PUSH TEMP POINT
ASSIGN POINT = MIN_IDX
POP ARRAY_MIN_IDX POINT
ASSIGN TEMP = ARRAY_MIN_IDX
PUSH TEMP POINT
ASSIGN TEMP = ARRAY_I
ASSIGN POINT = MIN_IDX
POP TEMP2 POINT
PUSH TEMP POINT
ASSIGN POINT = I
POP TEMP POINT
PUSH TEMP2 POINT
}
PEAK
"""

execute_program(program5, state, stack)