def solve_str(x,s):
    k = x//2
    s1 = ''.join(sorted(s[:k]))
    s2 = ''.join(sorted(s[:k],reverse=True))
    s3 = ''.join(sorted(s[k:]))

    return s1+s2+s3

def solve(n,x,s):
    st=set()
    for i in range(n-x+1):
        new_s1 = s[i,i+x]
        new_s2 = solve_str(x,new_s1)
        st.add(new_s2)
    return len(st)

def main():
    T = int(input())
    for _ in range(T):
        n,x = map(int,input())
        s = input().strip()
        count = sovle(n,x,s)
        print (count)

if __name__ =="__main__":
    main()