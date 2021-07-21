def main():
    import random

    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "X", "Y", "Z"]
    numbers = [1,2,3,4,5,6,7,8,9]

    password = ""
    length = 12

    for i in range(length):
        x = random.randint(1,10)
        if x in range(1, 4):
            password += str(random.choice(numbers))
        else:
            y = random.randint(1,10)
            if y in range(1,6):
                password += str(random.choice(alphabet))
            elif y in range(6,11):
                password += str(random.choice(alphabet)).lower()

    return(password)
