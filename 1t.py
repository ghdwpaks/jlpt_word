a = [5, 7, 4, 3, 8]  # 초기 상태
n = len(a)

for i in range(0, n - 1):
    min_index = i
    for j in range(i + 1, n):
        if a[j] < a[min_index]:
            min_index = j
    a[i], a[min_index] = a[min_index], a[i]
    print(f"{i+1}회전 결과: {a}")
