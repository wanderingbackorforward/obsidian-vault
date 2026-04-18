def c2num(c):
    return ord(c)-ord('a')
def to_num(s):
    res = 0
    while s:
        c = s[0]
        res = res*26+c2num(c)
        s = s[1:]
    return res

def solve(n,s1,s2):
    if s1==s2:
        return 0
    n1 = to_num(s1)
    n2 = to_num(s2)
    return n2-n1-1 if n2>=n1 else 0

def main():
    T = int(input())
    results = []
    for _ in range(T):
        n,s1,s2 = input().split()
        results.append(solve(n,s1,s2))
    for res in results:
        print(res)

if __name__ =="__main__":
    main()