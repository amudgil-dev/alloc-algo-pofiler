# calculate the slopes

import random

arrival_rate = 0.37796447300922725  # self.arrival_rate/self.n
d_n = 10


# def speedUp(allocated_servers):
#     return allocated_servers**0.5


def getPStarVector(d_n, arrival_rate, speedUp):
    slopes = []
    for i in range(1, d_n + 1):
        slopes.append(speedUp(i) / i)
    # print("slopes", slopes)
    # case 1: lambda below last slope
    # print(f"arrival rate is {arrival_rate} last P_star is {slopes[-1]}")
    if arrival_rate < slopes[-1]:
        # print("in case 1")
        y_star = [0] * d_n
        y_star[d_n - 1] = arrival_rate / speedUp(d_n)
        # print(" in getPstarVector", y_star)

    # case 2: lambda matches slope ASK ABOUT ROUNDING
    elif arrival_rate in slopes:
        i = 0
        # get max(i) if arrival rate matches multiple slopes
        for a, x in enumerate(slopes):
            if x == arrival_rate:
                i = a

        y_star = [0] * d_n
        y_star[i] = arrival_rate / speedUp(i + 1)
        # print("in case 2")

    # case 3: lambda is between 2 slopes
    else:
        # print("in case 3")
        y_star = [0] * d_n
        for i, x in enumerate(slopes[:-1]):
            if slopes[i + 1] < arrival_rate < slopes[i]:
                y_star[i] = (
                    (arrival_rate - slopes[i + 1])
                    / (slopes[i] - slopes[i + 1])
                    / (i + 1)
                )
                y_star[i + 1] = (
                    (slopes[i] - arrival_rate) / (slopes[i] - slopes[i + 1]) / (i + 2)
                )

        # print(y_star)

    p_star = [0] * d_n
    for i, x in enumerate(y_star):
        p_star[i] = x * speedUp(i + 1) / arrival_rate
    # print(p_star)
    return p_star


def getPstar_p1(p_star):

    p1 = [0, 0]
    # print("in getPstar_p1", p_star)
    for index, x in enumerate(p_star):
        if x != 0:
            p1[0] = x
            p1[1] = index + 1
            break
    # print("in getPstar_p1, returning p1: ", p1)
    return p1


def init_Pstar(d_n, arrival_rate, speedUp):
    p_star = getPStarVector(d_n, arrival_rate, speedUp)
    # print("in init_Pstar printing p_star", p_star)
    p1 = getPstar_p1(p_star)  # return p1 array
    # print("in init_Pstar printing p1", p1)
    return p1


def getOptimalServerNum(p1):
    random_num = random.uniform(0, 1)
    # print(random_num)
    if random_num < p1[0]:
        return p1[1]
    else:
        return p1[1] + 1


# p1 = init_Pstar(d_n, arrival_rate, speedUp)
# allocatedServers = getOptimalServerNum(p1)

# print(allocatedServers)
