
def encryption(cipher):
    abc = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
           "u", "v", "w", "x", "y", "z","A","B","C","D","E","F","G","H","I","J",
           "K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    size = len(cipher)
    size2 = len(abc)
    new_word=""
    x = 0
    for i in cipher:
        for x in range(size2):
            if (i == "z"):
                new_word += "b"
                break;
            elif (i == "y"):
                new_word += "a"
            elif (i == "Z"):
                new_word += "B"
                break;
            elif (i == "Y"):
                new_word += "A"
                break;
            elif (i == ' '):
                new_word += ' '
                break;
            elif (i == abc[x]):
                new_word += abc[x + 2]
    print(new_word)
    return new_word;

