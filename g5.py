from scipy import stats as st
import random
import numpy as np

linear_average_time = 3
tle_average_time = 5

price_energy = 10
price_tle = 5

chest_rewards = {
    "energy": {
        "probability": 40,
        "reward_energy": [5, 6],
        "reward_tle": [0, 0],
    },
    "tle": {
        "probability": 30,
        "reward_energy": [0, 0],
        "reward_tle": [2, 3],
    },
    "energy_tle": {
        "probability": 30,
        "reward_energy": [2, 3],
        "reward_tle": [1, 2],
    }
}

time_short = 10
time_long = 60

win_rate_linear = 1
win_rate_tle = 1


def win_chest(tle=False):
    rate = win_rate_tle if tle else win_rate_linear
    reward_energy = 0
    reward_tle = 0
    win = random.choices([True, False], weights=[rate, 1 - rate], k=1)[0]
    if win:
        chest = "energy" if tle else random.choices(list(chest_rewards.keys()),
                                                    weights=[chest_rewards[i]['probability'] for i in
                                                             chest_rewards.keys()], k=1)[0]
        reward_energy = random.randint(chest_rewards[chest]['reward_energy'][0],
                                       chest_rewards[chest]['reward_energy'][1])
        reward_tle = random.randint(chest_rewards[chest]['reward_tle'][0],
                                    chest_rewards[chest]['reward_tle'][1])
    return reward_energy, reward_tle


"""Simulating the game"""


def simulate_game():
    start_energy = 100
    start_tle = 0
    start_time = 0

    cur_tle = start_tle
    cur_tle_number = 0

    # Simulating short sessions
    for _ in range(4):
        for __ in range(3):
            # Simulating the win
            win_energy, win_tle = win_chest()
            cur_tle += win_tle

    start_time = 0

    game_num = 0
    # Simulating long session
    while start_time < time_long and start_energy >= price_energy:
        game_num += 1

        if cur_tle >= price_tle:
            start_energy -= price_energy
            cur_tle -= price_tle
            cur_tle_number += 1
            # Simulating the win
            win_energy, win_tle = win_chest(tle=True)
            cur_tle += win_tle
            start_energy += win_energy

            start_time += tle_average_time
            start_energy += 1
        else:
            start_energy -= price_energy
            # Simulating the win
            win_energy, win_tle = win_chest()
            cur_tle += win_tle
            start_energy += win_energy

            start_time += linear_average_time
            start_energy += 1

    return cur_tle_number, start_time


results = []
times = []

for i in range(10000):
    s, t = simulate_game()
    results.append(s)
    times.append(t)

results.sort()
print(np.median(results), np.mean(times))
