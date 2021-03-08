def main():
    import random
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "X", "Y", "Z"]
    numbers = [1,2,3,4,5,6,7,8,9]
    chars = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "{", "}", "[", "]", "|", ":", ";", "'", '"', "<", ">", ",", ".", "?", "/"]

    password = ""

    counter = 0
    counta = 0
    countb = 0
    countc = 0

    length = 12
    lengtha = 6
    lengthb = 4
    lengthc = 2

    while(counter != length):
        lowerorupper = random.randint(0, 1)
        turn = random.randint(1, 3)

        if turn == 1:
            if counta == lengtha:
                continue

            a = random.choice(alphabet)
            counta += 1
            if lowerorupper == 0:
                a = a.lower()
                password += str(a)
            else:
                password += str(a)

        elif turn == 2:
            if countb == lengthb:
                continue
            b = random.choice(numbers)
            countb += 1
            password += str(b)
            b = None
        
        elif turn == 3:
            if countc == lengthc:
                continue
            c = random.choice(chars)
            countc += 1
            password += str(c)
            c = None
        
        counter += 1
    return(password)
