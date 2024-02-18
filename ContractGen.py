import random
import string
import uuid

function_names = []  # Global list to track generated function names
returning_functions = []  # Track functions that return a value (func_name, return_type)
non_returning_functions = []  # Track functions that do not return a value

def genInt():
    _64bitMask = 0b11111111_11111111_11111111_11111111_11111111_11111111_11111111_11111111
    x, y = uuid.uuid4(), uuid.uuid4()
    a = x.int >> 64
    b = x.int & _64bitMask
    c = y.int >> 64
    d = y.int & _64bitMask
    return [a, b, c, d]

fxnCnt = 0
varCnt = 0
#no more random name just increment variables
def generate_func_name():
    global fxnCnt
    res = "FXN_" + str(fxnCnt)
    fxnCnt += 1
    return res

def generate_var_name():
    global varCnt
    res = "VAR_" + str(varCnt)
    varCnt += 1
    return res

def generate_type_specific_value(var_type):
    values = genInt()
    if var_type in ["uint64", "int64"]:
        return str(values[0] & ((1 << 64) - 1))
    elif var_type in ["uint128", "int128"]:
        return f"(({values[1]} << 64) | {values[0]})"
    elif var_type in ["uint192", "int192"]:
        return f"(({values[2]} << 128) | ({values[1]} << 64) | {values[0]})"
    elif var_type in ["uint256", "int256"]:
        return f"(({values[0]} << 64) + {values[1]} << 128) + (({values[2]} << 64) + {values[3]})"
    elif var_type == "bool":
        return "true" if values[0] & 1 == 0 else "false"
    elif var_type == "address":
        return f"address(0x{values[0] & ((1 << 160) - 1):040x})"
    else:
        return "0"

def add_function_name(func_name, var_type, will_return):
    """Track newly generated functions, distinguishing those with return values."""
    function_info = (func_name, var_type)
    if will_return:
        returning_functions.append(function_info)
    else:
        non_returning_functions.append(func_name)

def get_random_function_call():
    if not function_names:
        return ""
    func_name = random.choice(returning_functions)
    return f"{func_name}();"

def generate_arithmetic_operation():
    ops = ["+", "-", "*", "/"]
    op = random.choice(ops)
    num1, num2 = random.randint(1, 100), random.randint(1, 100)
    return f"{num1} {op} {num2}"

def generate_arithmetic_operation_with_variables():
    var_types = ["uint64", "int64", "uint128", "int128", "uint192", "int192", "uint256", "int256"]
    var_type = random.choice(var_types)
    var_name1 = generate_var_name()
    var_name2 = generate_var_name()

    value1 = generate_type_specific_value(var_type)
    value2 = generate_type_specific_value(var_type)
    
    operation = random.choice(["+", "-", "*", "/"])
    operation_result = f"{var_type} {var_name1} = {value1};\n    {var_type} {var_name2} = {value2};\n    {var_name1} = {var_name1} {operation} {var_name2};"
    
    return operation_result, var_name1, var_type

def generate_function():
    func_name = generate_func_name()
    var_type = random.choice(["uint64", "int64", "uint128", "int128", "uint192", "int192", "uint256", "int256"])
    will_return = random.choice([True, False])
    
    # Keep track of functions that return a value
    if will_return:
        returning_functions.append((func_name, var_type))
    else:
        non_returning_functions.append(func_name)
    
    operations_results = []
    last_var_name, last_var_type = "", ""
    
    for _ in range(random.randint(1, 3)):  # Fewer operations for simplicity
        operation_result, last_var, var_type = generate_arithmetic_operation_with_variables()
        operations_results.append(operation_result)
        last_var_name, last_var_type = last_var, var_type

    # Optionally include a function call with assignment
    if returning_functions:  # Ensure there's at least one function that returns a value
        call_assignment, _ = generate_function_call_with_assignment(returning_functions)
        operations_results.append(call_assignment)

    operations_code = "\n    ".join(operations_results)
    return_statement = f"    return {last_var_name};" if will_return else ""
    returns_modifier = f"returns ({last_var_type})" if will_return else ""

    add_function_name(func_name, var_type, will_return)  # Track the new function

    func_declaration = f"""
function {func_name}() public {returns_modifier} {{
    {operations_code}
    {return_statement}
}}
"""
    return func_declaration, func_name, var_type, will_return

def generate_function_call_with_assignment(returning_functions):
    """Generates a variable assignment from a function call, given functions that have return values."""
    if not returning_functions or len(returning_functions) < 2:
        return "", ""
    
    # Choose a function that returns a value
    func_name, return_type = random.choice(returning_functions[0:fxnCnt-2])
    var_name = generate_var_name()
    
    # Create an assignment statement using the function call
    assignment_statement = f"{return_type} {var_name} = {func_name}();"
    return assignment_statement, var_name

def generate_struct():
    struct_name = generate_random_name().capitalize()
    num_fields = random.randint(2, 5)
    field_types = ["uint", "int", "bool", "address", "uint256", "int256"]
    fields = [f"    {random.choice(field_types)} {generate_random_name()};" for _ in range(num_fields)]
    struct_definition = f"struct {struct_name} {{\n" + "\n".join(fields) + "\n}}"
    return struct_definition

def generate_contract(num_funcs=20):
    contract_name = generate_random_name().capitalize()

    functions = [generate_function() for _ in range(num_funcs)]

    contract = f"""
pragma solidity =0.8.21;

contract {contract_name} {{
    {''.join(f[0] for f in functions)}
}}
"""
    return contract

# Generate and print a sample contract
print(generate_contract())
