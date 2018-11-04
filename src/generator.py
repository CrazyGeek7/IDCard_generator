import os

def generator(address_code,birthday_code,sex=""):
    id_list=[]
    if len(address_code)!=6:
        print "address code error"
        return
    if len(birthday_code)!=8:
        print "birthday code error"
        return
    if sex == "":
        for i in range(1,1000):
            i = repair_i(str(i))
            id = address_code + birthday_code + i + cheak(address_code + birthday_code + i)
            id_list.append(id)
    elif sex == "male":
        for i in range(1,1000):
            if i%2 == 0:
                pass
            else:
                i = repair_i(str(i))
                id = address_code + birthday_code + i + cheak(address_code + birthday_code + i)
                id_list.append(id)
    elif sex == "famale":
        for i in range(1,1000):
            if i%2 != 0:
                pass
            else:
                i = repair_i(str(i))
                id = address_code + birthday_code + i + cheak(address_code + birthday_code + i)
                id_list.append(id)
    return id_list

def cheak(s):
    sum = int(s[0]) * 7 + int(s[1]) * 9 + int(s[2]) * 10 + int(s[3]) * 5 + int(s[4]) * 8 + int(s[5]) * 4 + int(
        s[6]) * 2 + int(s[7]) * 1 + int(s[8]) * 6 + int(s[9]) * 3 + int(s[10]) * 7 + int(s[11]) * 9 + int(
        s[12]) * 10 + int(s[13]) * 5 + int(s[14]) * 8 + int(s[15]) * 4 + int(s[16]) * 2
    return '10X98765432'[sum % 11]

def repair_i(i):
    if len(i) == 1:
        i = "00" + i
    elif len(i) == 2:
        i = "0" + i
    return i

def main():
    address = "110105"
    birthday = "20000101"
    sex = "male"
    id_list = generator(address,birthday,sex)
    for i in range(len(id_list)):
        os.system("echo " + id_list[i] + " >> " + "../IDCard_dictionary/" + address + birthday + sex + ".txt")

if __name__ == "__main__":
    main()