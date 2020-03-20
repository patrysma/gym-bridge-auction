import gym
import gym_bridge_auction

env = gym.make('BridgeAuction-v0')
observation = env.reset()
env.render()
for i in range(0,4):
    #env.render()
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    env.render()
    print(observation)
    print(reward)
env.close()




