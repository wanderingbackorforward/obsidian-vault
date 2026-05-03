from collections import Counter
from math import comb

def main():
    res = 0
    n = int(input())
    a = list(map(int,input().split()))

    cnt = Counter(a)
    freqs = cnt.values()
    m=len(freqs)
    for i in range(m):
        for j in range(i+1,m):
            freq_2i = comb(freqs[i],2)
            freq_3i = comb(freqs[i],3)
            freq_2j = comb(freqs[j],2)
            freq_3j = comb(freqs[j],3)
            res += ((freq_2i*freq_3j)+(freq_3i*freq_2j))

    print(res)
    
if __name__ == "__main__":
    main()