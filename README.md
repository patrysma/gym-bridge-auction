# Środowisko do licytacji brydżowej

Środowisko wieloagentowe (czterech graczy) symulujące licytację brydżową wykorzystujące interfejs biblioteki Gym. Jest to przykład środowiska, gdzie poszczególni agenci nie posiadają pełnego zestawu informacji na temat stanu gry. Mają dostęp tylko do historii licytacji oraz własnych kart, ręce przeciwników nie są znane.
    
Gracze w ustalonej kolejności zegarowej (rozpoczyna rozdający) wykonują pojedyńcze akcje wybierane z dostępnej 
przestrzeni (licytują). Działania agentów są wartościowane za pomocą nagrody oceniającej skuteczność licytacji. W każdym kroku zwracana jest różnica od przypadku idealnego. Definiując funkcję nagrody wspomagano się dostępnymi narzędziami, czyli Double Dummy Solver. Cel każdego z epizodów to ustalenie kontraktu, który stanowi zobowiązanie do wzięcia określonej liczby lew przez parę wygrywającą licytację.

## Wymagania wstępne

W tym środowisku agenci wykonują kolejno pojedyńcze akcje (licytują). Dlatego funkcja `step()` przyjmuje tylko jedno działanie agenta, który zgodnie z ustaloną kolejnością powinien licytować i zwraca jedną obserwację, nagrodę i informację czy należy zresetować środowisko (czy otrzymano 3 pasy po kolei po zgłoszonej odzywce, czyli zakończono licytację lub nikt nie zdeklarował kontraktu - wszyscy spasowali). 

Przestarzeń akcji zdefiniowano następująco: 
```python 
spaces.Dynamic(38)
``` 
Poszczególne liczby oznaczają różne odzywki licytacyjne oraz zapowiedzi: pas, kontra, rekontra. Przestrzeń akcji zmniejsza się (gdy agenci nie pasują, bądź nie kontrują i nie rekontrują) w każdym kroku o odzywki niższe od ostatniej wypowiedzianej.  Dodatkowo dostępna są zapowiedzi kontra i rekontra. Kontra dostępna jest dla przeciwników pary, która zgłosiła ostatnią odzywkę. Natomiast rekontra pojawia się dla pary z najwyższą obecnie zgłoszoną odzywką po kontrze przeciwników. Tak zmieniającą się przestrzeń akcji zapewnia zdefiniowana klasa `Dynamic` dziedzicząca po `Discrete`.  Oznaczenia przedstawiono poniżej.

| Liczba | Działanie |
| ------ | --------- |
| 0 | pass |
| 1 | 7NT |
| 2 |  7S |
| 3 | 7H |
| 4 | 7D |
| 5 | 7C |
| . | . |
| . | . |
| 31 | 1NT |
| 32 | 1S |
| 33 | 1H |
| 34 | 1D |
| 35 | 1C |
| 36 | double |
| 37 | redouble |

Przestrzeń obserwacji zdefiniowano następująco:

```python
spaces.Dict({'whose turn': spaces.Discrete(self._n_players),
             'whose next turn': spaces.Discrete(self._n_players),
             'LAST_contract': spaces.Discrete(36),
             'NORTH_contract': spaces.Discrete(36),
             'EAST_contract': spaces.Discrete(36),
             'SOUTH_contract': spaces.Discrete(36),
             'WEST_contract': spaces.Discrete(36),
             'winning_pair': spaces.Discrete(self._n_players / 2),
             'double/redouble': spaces.Discrete(3)})
```
- Stan 'whose turn' oznacza kto licytował. Oznaczenia poszczególnych liczb przedstawiono poniżej.

| Liczba | Nazwa gracza |
| ------ | ------------ |
| 0 | N |
| 1 | E |
| 2 | S |
| 3 | W |

- Stan 'whose next turn' oznacza gracza, który następny w kolejności ma licytować. Oznaczenia liczb zgodne ze stanem 'whose turn'.
- Stan 'LAST_contract' oznacza ostateczny kontrakt po każdym z kroków. Oznaczenia liczb są zgodne z tymi przyjętymi w przestrzeni akcji.
- Stany 'NORTH_contract', 'EAST_contract', 'SOUTH_contract', 'WEST_contract' są to odzywki poszczególnych graczy. Zmieniają się one, gdy odpowiedni gracz zalicytuje. Oznaczenia liczb są zgodne z tymi przyjętymi w przestrzeni akcji.
- Stan 'winning_pair' oznacza która z par graczy ma w danym kroku najwyższy kontrakt. Oznaczenia liczb są następujące:

| Liczba | Nazwa pary |
| ------ | ---------- |
| 0 | N/S |
| 1 | E/W |

- Stan 'double/redouble' oznacza czy wystąpiła kontra, rekontra lub żadne z nich. Oznaczenia przedstawiono poniżej.

| Liczba | Działanie |
| ------ | ---------- |
| 0 | no double/redouble |
| 1 | double - 'X' |
| 2 | redouble - 'XX' |

Działanie środowiska przetestowano w systemie Linux.

Aby użyć środowiska konieczne jest zainstalowanie następujących bibliotek: `pygame` , `cppyy` i `gym`.

Należy również przekopiować następujące pliki: `libdds.so` i `libddswrapper.so` do folderu `/usr/lib` w swoim systemie, aby zaintalować biblioteki konieczne do użycia Double Dummy Solver. Można to zrobić w następujący sposób:

```
sudo cp /home/patrycja/PycharmProjects/gym_bridge_auction/gym_bridge_auction/envs/solver/dds_wrapper/libddswrapper.so /usr/lib

sudo ldconfig

ldconfig -p|grep ddswrapper
```

Podczas kopiowania podajemy odpowiednią ścieżkę występowania pliku.


Aby przetestować działanie środowiska w wersji konsolowej można użyć poniższego kodu. Do testów wykorzystujących interfejs graficzny należy przy renderowaniu podać opcję `'human'`, czyli: `env.render('human')`. Poniższy kod przedstawia działanie środowiska dla losowych działań agentów.

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

# Działanie środowiska z interfejsem graficznym

[![Watch the video](https://i.imgur.com/UIgSQDV.jpg)](https://youtu.be/VSm32FQY6Bk)

Poniżej przedstawiono wartości nagrody i przestrzeń obserwacji dla powyższego działania.

Pierwszy epizod:

```
Observation space:
{'whose turn': None, 'whose next turn': 2, 'LAST_contract': None, 'Player_contract': None, 'winning_pair': None, 'double/redouble': 0, 'Players hand': [[0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]], 'pair score/optimum score': array([   0,    0, -300,  300])}
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 20, 'double/redouble': 0, 'Player_contract': 20, 'winning_pair': 0, 'pair score/optimum score': array([-450,  450, -300,  300])}
Reward: [-150, 150]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 14, 'double/redouble': 0, 'Player_contract': 14, 'winning_pair': 1, 'pair score/optimum score': array([ 150, -150, -300,  300])}
Reward: [450, -450]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 7, 'double/redouble': 0, 'Player_contract': 7, 'winning_pair': 0, 'pair score/optimum score': array([-200,  200, -300,  300])}
Reward: [100, -100]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 7, 'double/redouble': 1, 'Player_contract': 36, 'winning_pair': 0, 'pair score/optimum score': array([-800,  800, -300,  300])}
Reward: [-500, 500]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 7, 'double/redouble': 2, 'Player_contract': 37, 'winning_pair': 0, 'pair score/optimum score': array([-1600,  1600,  -300,   300])}
Reward: [-1300, 1300]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 0, 'Player_contract': 1, 'winning_pair': 1, 'pair score/optimum score': array([ 200, -200, -300,  300])}
Reward: [500, -500]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 1, 'double/redouble': 0, 'Player_contract': 0, 'winning_pair': 1, 'pair score/optimum score': array([ 200, -200, -300,  300])}
Reward: [500, -500]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 1, 'double/redouble': 0, 'Player_contract': 0, 'winning_pair': 1, 'pair score/optimum score': array([ 200, -200, -300,  300])}
Reward: [500, -500]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 36, 'winning_pair': 1, 'pair score/optimum score': array([ 800, -800, -300,  300])}
Reward: [1100, -1100]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 2, 'Player_contract': 37, 'winning_pair': 1, 'pair score/optimum score': array([ 1600, -1600,  -300,   300])}
Reward: [1900, -1900]
Episode 1 finished after 10 timesteps
```

Drugi epizod:

```
Observation space:
{'whose turn': None, 'whose next turn': 2, 'LAST_contract': None, 'Player_contract': None, 'winning_pair': None, 'double/redouble': 0, 'Players hand': [[0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]], 'pair score/optimum score': array([   0,    0, -300,  300])}
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 35, 'double/redouble': 0, 'Player_contract': 35, 'winning_pair': 0, 'pair score/optimum score': array([-300,  300, -300,  300])}
Reward: [0, 0]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 15, 'double/redouble': 0, 'Player_contract': 15, 'winning_pair': 1, 'pair score/optimum score': array([  50,  -50, -300,  300])}
Reward: [350, -350]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 15, 'double/redouble': 1, 'Player_contract': 36, 'winning_pair': 1, 'pair score/optimum score': array([ 100, -100, -300,  300])}
Reward: [400, -400]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 10, 'double/redouble': 0, 'Player_contract': 10, 'winning_pair': 1, 'pair score/optimum score': array([ 100, -100, -300,  300])}
Reward: [400, -400]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 6, 'double/redouble': 0, 'Player_contract': 6, 'winning_pair': 0, 'pair score/optimum score': array([-400,  400, -300,  300])}
Reward: [-100, 100]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 5, 'double/redouble': 0, 'Player_contract': 5, 'winning_pair': 1, 'pair score/optimum score': array([ 150, -150, -300,  300])}
Reward: [450, -450]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 5, 'double/redouble': 1, 'Player_contract': 36, 'winning_pair': 1, 'pair score/optimum score': array([ 500, -500, -300,  300])}
Reward: [800, -800]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 2, 'double/redouble': 0, 'Player_contract': 2, 'winning_pair': 1, 'pair score/optimum score': array([ 400, -400, -300,  300])}
Reward: [700, -700]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 2, 'double/redouble': 1, 'Player_contract': 36, 'winning_pair': 1, 'pair score/optimum score': array([ 2000, -2000,  -300,   300])}
Reward: [2300, -2300]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 2, 'double/redouble': 2, 'Player_contract': 37, 'winning_pair': 1, 'pair score/optimum score': array([ 4000, -4000,  -300,   300])}
Reward: [4300, -4300]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 2, 'double/redouble': 2, 'Player_contract': 0, 'winning_pair': 1, 'pair score/optimum score': array([ 4000, -4000,  -300,   300])}
Reward: [4300, -4300]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 2, 'double/redouble': 2, 'Player_contract': 0, 'winning_pair': 1, 'pair score/optimum score': array([ 4000, -4000,  -300,   300])}
Reward: [4300, -4300]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 1, 'double/redouble': 0, 'Player_contract': 1, 'winning_pair': 0, 'pair score/optimum score': array([-450,  450, -300,  300])}
Reward: [-150, 150]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 0, 'Player_contract': 0, 'winning_pair': 0, 'pair score/optimum score': array([-450,  450, -300,  300])}
Reward: [-150, 150]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 1, 'double/redouble': 0, 'Player_contract': 0, 'winning_pair': 0, 'pair score/optimum score': array([-450,  450, -300,  300])}
Reward: [-150, 150]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 36, 'winning_pair': 0, 'pair score/optimum score': array([-2300,  2300,  -300,   300])}
Reward: [-2000, 2000]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 0, 'pair score/optimum score': array([-2300,  2300,  -300,   300])}
Reward: [-2000, 2000]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 0, 'pair score/optimum score': array([-2300,  2300,  -300,   300])}
Reward: [-2000, 2000]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 0, 'pair score/optimum score': array([-2300,  2300,  -300,   300])}
Reward: [-2000, 2000]
Episode 2 finished after 19 timesteps
```

Trzeci epizod:

```
Observation space:
{'whose turn': None, 'whose next turn': 2, 'LAST_contract': None, 'Player_contract': None, 'winning_pair': None, 'double/redouble': 0, 'Players hand': [[0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]], 'pair score/optimum score': array([   0,    0, -300,  300])}
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 32, 'double/redouble': 0, 'Player_contract': 32, 'winning_pair': 0, 'pair score/optimum score': array([ 110, -110, -300,  300])}
Reward: [410, -410]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 0, 'Player_contract': 1, 'winning_pair': 1, 'pair score/optimum score': array([ 200, -200, -300,  300])}
Reward: [500, -500]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 36, 'winning_pair': 1, 'pair score/optimum score': array([ 800, -800, -300,  300])}
Reward: [1100, -1100]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 1, 'pair score/optimum score': array([ 800, -800, -300,  300])}
Reward: [1100, -1100]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 1, 'pair score/optimum score': array([ 800, -800, -300,  300])}
Reward: [1100, -1100]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 1, 'pair score/optimum score': array([ 800, -800, -300,  300])}
Reward: [1100, -1100]
Episode 3 finished after 6 timesteps
```

Czwarty epizod:

```
Observation space:
{'whose turn': None, 'whose next turn': 2, 'LAST_contract': None, 'Player_contract': None, 'winning_pair': None, 'double/redouble': 0, 'Players hand': [[0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]], 'pair score/optimum score': array([   0,    0, -300,  300])}
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 23, 'double/redouble': 0, 'Player_contract': 23, 'winning_pair': 0, 'pair score/optimum score': array([-150,  150, -300,  300])}
Reward: [150, -150]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 19, 'double/redouble': 0, 'Player_contract': 19, 'winning_pair': 1, 'pair score/optimum score': array([ 100, -100, -300,  300])}
Reward: [400, -400]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 13, 'double/redouble': 0, 'Player_contract': 13, 'winning_pair': 0, 'pair score/optimum score': array([-250,  250, -300,  300])}
Reward: [50, -50]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 8, 'double/redouble': 0, 'Player_contract': 8, 'winning_pair': 1, 'pair score/optimum score': array([ 350, -350, -300,  300])}
Reward: [650, -650]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 8, 'double/redouble': 1, 'Player_contract': 36, 'winning_pair': 1, 'pair score/optimum score': array([ 1700, -1700,  -300,   300])}
Reward: [2000, -2000]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 0, 'Player_contract': 1, 'winning_pair': 1, 'pair score/optimum score': array([ 200, -200, -300,  300])}
Reward: [500, -500]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 36, 'winning_pair': 1, 'pair score/optimum score': array([ 800, -800, -300,  300])}
Reward: [1100, -1100]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 1, 'pair score/optimum score': array([ 800, -800, -300,  300])}
Reward: [1100, -1100]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 1, 'pair score/optimum score': array([ 800, -800, -300,  300])}
Reward: [1100, -1100]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 2, 'Player_contract': 37, 'winning_pair': 1, 'pair score/optimum score': array([ 1600, -1600,  -300,   300])}
Reward: [1900, -1900]
Episode 4 finished after 10 timesteps
```

Piąty epizod:

```
Observation space:
{'whose turn': None, 'whose next turn': 2, 'LAST_contract': None, 'Player_contract': None, 'winning_pair': None, 'double/redouble': 0, 'Players hand': [[0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]], 'pair score/optimum score': array([   0,    0, -300,  300])}
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 21, 'double/redouble': 0, 'Player_contract': 21, 'winning_pair': 0, 'pair score/optimum score': array([-250,  250, -300,  300])}
Reward: [50, -50]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 3, 'double/redouble': 0, 'Player_contract': 3, 'winning_pair': 1, 'pair score/optimum score': array([ 400, -400, -300,  300])}
Reward: [700, -700]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 2, 'double/redouble': 0, 'Player_contract': 2, 'winning_pair': 0, 'pair score/optimum score': array([-250,  250, -300,  300])}
Reward: [50, -50]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 2, 'double/redouble': 0, 'Player_contract': 0, 'winning_pair': 0, 'pair score/optimum score': array([-250,  250, -300,  300])}
Reward: [50, -50]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 1, 'double/redouble': 0, 'Player_contract': 1, 'winning_pair': 0, 'pair score/optimum score': array([-450,  450, -300,  300])}
Reward: [-150, 150]
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 36, 'winning_pair': 0, 'pair score/optimum score': array([-2300,  2300,  -300,   300])}
Reward: [-2000, 2000]
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 0, 'pair score/optimum score': array([-2300,  2300,  -300,   300])}
Reward: [-2000, 2000]
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 0, 'pair score/optimum score': array([-2300,  2300,  -300,   300])}
Reward: [-2000, 2000]
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 1, 'double/redouble': 1, 'Player_contract': 0, 'winning_pair': 0, 'pair score/optimum score': array([-2300,  2300,  -300,   300])}
Reward: [-2000, 2000]
Episode 5 finished after 9 timesteps
```



