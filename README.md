# Środowisko do licytacji brydżowej

Środowisko wieloagentowe (czterech graczy) symulujące licytację brydżową wykorzystujące interfejs biblioteki Gym. Jest to przykład środowiska, gdzie poszczególni agenci nie posiadają pełnego zestawu informacji na temat stanu gry. Mają dostęp tylko do historii licytacji oraz własnych kart, ręce przeciwników nie są znane.
    
Gracze w ustalonej kolejności zegarowej (rozpoczyna rozdający) wykonują pojedyńcze akcje wybierane z dostępnej 
przestrzeni (licytują). Działania agentów są wartościowane za pomocą nagrody oceniającej skuteczność licytacji. W każdym kroku zwracana jest różnica od przypadku idealnego. Definiując funkcję nagrody wspomagano się dostępnymi narzędziami, tj. Double Dummy Solver Bo Haglunda. Cel każdego z epizodów to ustalenie kontraktu, który stanowi zobowiązanie do wzięcia określonej liczby lew przez parę wygrywającą licytację.

## Wymagania wstępne

System operacyjny Linux (testy i implementacja na Ubuntu). 

Wersja Python 3.5+.

Wymagana jest instalacja następujących bibliotek: `pygame` , `cppyy` , `gym` i `numpy`.

Należy również przekopiować następujące pliki: `libdds.so` i `libddswrapper.so` do folderu `/usr/lib` lub `/lib`w swoim systemie, aby zaintalować biblioteki konieczne do użycia Double Dummy Solver. Można to zrobić w następujący sposób:

```
sudo cp /home/patrycja/PycharmProjects/gym_bridge_auction/gym_bridge_auction/envs/solver/dds_wrapper/libddswrapper.so /usr/lib

sudo ldconfig

ldconfig -p|grep ddswrapper
```

Podczas kopiowania podajemy odpowiednią ścieżkę do pliku.

Opisany powyżej sposób z kopiowaniem bibliotek jest najprostszy, można zastosować też inne nie przedstawione w tym dokumencie.

Po pobraniu środowiska z repozytorium należy je zaintalować, aby możliwe było jego użycie. W tym celu należy przejść w terminalu do folderu, gdzie umieszczono rozpakowane pliki ze środowiskiem (nazwę folderu podrzędnego ustawić na `gym-bridge-auction`, jeśli jest inna). Następnie dokonać instalacji w następujący sposób (posiadając wersję Python 3.5+):

```
python3 -m pip install gym-bridge-auction 
```

lub

```
python3 -m pip install -e .
```

Korzystając z  drugiego sposobu oprócz środowiska zainstalują się niezbędne biblioteki  `pygame` , `cppyy` , `gym` i `numpy`.

## Praca

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

## Działanie środowiska z interfejsem graficznym

Działanie kodu z poprzedniego punktu przedstawiono na poniższym filmiku.

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



