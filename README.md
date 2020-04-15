# gym_bridge_auction
Środowisko do licytacji brydżowej

Działanie środowiska przetestowano w systemie Linux.

Aby użyć środowiska konieczne jest zainstalowanie następujących bibliotek: `pygame` , `cppyy` i `gym`.

Należy również przekopiować następujące pliki: `libdds.so` i `libddswrapper.so` do folderu `\usr\lib`

```
import gym
import gym_bridge_auction
import pygame

env = gym.make('BridgeAuction-v0')

for i_episode in range(5):
    observation = env.reset()
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
            print("Episode finished after {} timesteps".format(i + 1))
            break

env.close()
```
