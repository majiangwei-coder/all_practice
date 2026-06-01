# def palindrome(st:str):
#     st1 = st[::-1]
#     if st1 == st[::-1]:              # nums[::-1]  步长 -1 .反转序列
#         return True
#
#
# print(palindrome("asdfgfdsa"))

def pa(string:str):
    for i in range(int(len(string)*0.5)):
        if string[i] == string[len(string)-1-i]:
            continue
        return False
    return True
print(pa("asdfgfdsa"))

st = "123456789"
print(st[::-1])