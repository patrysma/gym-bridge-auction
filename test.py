import gym_bridge_auction
import gym

"""Przykład użycia środowiska dla losowych działań agentów i interfejsu graficznego (opcja 'console')"""

PLAYERS_NAMES = ['N', 'E', 'S', 'W']

for i_episode in range(5):
    env = gym.make('BridgeAuction-v0')
    observation = env.reset()
    hands = {}
    print(env.metadata)

    for number, player in enumerate(PLAYERS_NAMES):
        hands[player] = observation['Players hands'][number]

    env.render('console')
    print('Observation space:')
    print(observation)

    for i in range(100):
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        env.render('console')
        print('Observation space:')
        print(observation)
        print('Reward: ' + str(reward))

        if done:
            print("Episode {} finished after {} timesteps".format(i_episode + 1, i + 1))
            break

env.close()
