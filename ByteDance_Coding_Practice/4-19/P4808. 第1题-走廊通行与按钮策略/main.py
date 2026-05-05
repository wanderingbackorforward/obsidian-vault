import sys


# 判断当前持续时间 x 是否可行
def check(a, n, k, x):
    # cnt 表示已经使用的按钮次数
    cnt = 0
    # cover 表示当前按钮效果最远覆盖到的位置（1-based）
    cover = 0

    # 按顺序扫描每一扇门
    for i in range(1, n + 1):
        # 如果当前门已经被之前的按钮覆盖，则直接通过
        if i <= cover:
            continue

        # 如果当前门未被覆盖且是关闭状态，则必须在这里按按钮
        if a[i - 1] == 1:
            cnt += 1
            cover = i + x - 1

            # 如果按钮次数已经超过 K，则当前 x 不可行
            if cnt > k:
                return False

    return True


def solve():
    input = sys.stdin.readline
    t = int(input().strip())
    ans = []

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        # 如果所有门本来都打开，则不需要按按钮，答案为 0
        if 1 not in a:
            ans.append("0")
            continue

        # 二分最小可行的 x
        left, right = 1, n
        while left < right:
            mid = (left + right) // 2
            if check(a, n, k, mid):
                right = mid
            else:
                left = mid + 1

        ans.append(str(left))

    print("\n".join(ans))


if __name__ == "__main__":
    solve()
