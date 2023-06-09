def cpu_bound_function(num: int):
    total = 0
    arrange = range(1, num + 1)
    for i in arrange:
        for j in arrange:
            for k in arrange:
                total += i + j + k

    return total


if __name__ == "__main__":
    result = cpu_bound_function(500)
    print(result)
