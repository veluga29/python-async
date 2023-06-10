import time
import os
import threading

nums = [50, 63, 32]
# nums = [30] * 100


def cpu_bound_func(num):
    print(f"process id : {os.getpid()} | thread id: {threading.get_ident()}")
    numbers = range(1, num)
    total = 1
    for i in numbers:
        for j in numbers:
            for k in numbers:
                total *= i * j * k
    return total


def main():
    results = [cpu_bound_func(num) for num in nums]
    # print(results)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 12
