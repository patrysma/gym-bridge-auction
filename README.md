# Środowisko do licytacji brydżowej

Środowisko wieloagentowe (czterech graczy) symulujące licytację brydżową wykorzystujące interfejs biblioteki Gym.

W tym środowisku agenci wykonują kolejno pojedyńcze akcje (licytują). Dlatego funkcja `step()` przyjmuje tylko jedno działanie agenta, który zgodnie z ustaloną kolejnością powinien licytować i zwraca jedną obserwację, nagrodę i informację czy należy zresetować środowisko (czy otrzymano 3 pasy po kolei, czyli zakończono licytację). 

Przestarzeń akcji zdefiniowano następująco: `self.action_space = spaces.Discrete(36)`.

Działanie środowiska przetestowano w systemie Linux.

Aby użyć środowiska konieczne jest zainstalowanie następujących bibliotek: `pygame` , `cppyy` i `gym`.

Należy również przekopiować następujące pliki: `libdds.so` i `libddswrapper.so` do folderu `\usr\lib\` w swoim systemie.

Aby przetestować działanie środowiska w wersji konsolowej można użyć poniższego kodu. Do testów wykorzystujących interfejs graficzny należy przy renderowaniu podać opcję `'human'`, czyli: `env.render('human')`.

```python
import gym
import gym_bridge_auction

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

Działanie opcji z interfejsem graficznym:

[![Watch the video](https://i.imgur.com/058RZlw.jpg)](https://youtu.be/DybSAue5bYY)  
