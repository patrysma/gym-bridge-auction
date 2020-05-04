import gym
import gym_bridge_auction

env = gym.make('BridgeAuction-v0')

for i_episode in range(5):
    observation = env.reset()
    env.render()
    print('Observation space:')
    print(observation)

    for i in range(100):
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        env.render()
        print('Observation space:')
        print(observation)
        print('Reward: ' + str(reward))

        if done:
            print("Episode finished after {} timesteps".format(i + 1))
            break

env.close()



