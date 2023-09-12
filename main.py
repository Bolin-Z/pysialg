from random import random, seed

if __name__ == "__main__":
    # a = [[ _ + j for j in range(4)] for _ in range(3)]
    # print(a)
    # print(len(a))
    t = 5
    for i in range(5):
        t += i
        if t > 10:
            print(t)
            break
        print(i)