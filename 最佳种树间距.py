# 输入获取
n = int(input("请输入第一行："))
positions = list(map(int, input("请输入第一行：").split()))
m = int(input("请输入第一行："))


def check(minDis):
    count = 1
    curPos = positions[0]

    for i in range(1, n):
        if positions[i] - curPos >= minDis:
            count += 1
            curPos = positions[i]

    return count >= m


# 算法入口
def getResult():
    positions.sort()

    low = 1
    high = positions[-1] - positions[0]
    ans = 0

    while low <= high:
        mid = (low + high) >> 1

        if check(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1

    return ans


# 算法调用
print(getResult())