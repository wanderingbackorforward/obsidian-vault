import sys


# 构造一个长度为 x 的子串对应的新字符串
def build_new_string(sub, x):
    # k 表示前一半字符的长度，题意中的 i / 2 取整即可
    k = x // 2

    # 第一部分：前 k 个字符升序排序
    part1 = ''.join(sorted(sub[:k]))

    # 第二部分：整个子串降序排序
    part2 = ''.join(sorted(sub, reverse=True))

    # 第三部分：剩余字符升序排序
    part3 = ''.join(sorted(sub[k:]))

    # 按顺序拼接
    return part1 + part2 + part3


# 处理一组测试数据
def solve_case(n, x, s):
    # 用集合保存不同的新字符串
    st = set()

    # 枚举所有长度为 x 的子串
    for i in range(n - x + 1):
        sub = s[i:i + x]
        st.add(build_new_string(sub, x))

    # 返回不同结果的数量
    return len(st)


def main():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    idx = 1
    ans = []

    for _ in range(t):
        n = int(data[idx])
        x = int(data[idx + 1])
        s = data[idx + 2]
        idx += 3

        ans.append(str(solve_case(n, x, s)))

    print('\n'.join(ans))


if __name__ == "__main__":
    main()
