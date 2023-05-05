import random

def generatecode3() -> str:
    code = str(random.randint(1000, 9999))
    r2 = random.randint(1, 3)
    if r2 == 1:
        code = f"{code[1]}{code[1]}{code[2]}{code[3]}"
    elif r2 == 2:
        code = f"{code[0]}{code[2]}{code[2]}{code[3]}"
    else:
        code = f"{code[0]}{code[1]}{code[3]}{code[3]}"
    return code
