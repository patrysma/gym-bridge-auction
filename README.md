# Środowisko do licytacji brydżowej

Środowisko wieloagentowe (czterech graczy) symulujące licytację brydżową wykorzystujące interfejs biblioteki Gym. Jest to przykład środowiska, gdzie poszczególni agenci nie posiadają pełnego zestawu informacji na temat stanu gry. Mają dostęp tylko do historii licytacji oraz własnych kart, ręce przeciwników nie są znane.
    
Gracze w ustalonej kolejności zegarowej (rozpoczyna rozdający) wykonują pojedyncze akcje wybierane z dostępnej 
przestrzeni (licytują). Działania agentów są wartościowane za pomocą nagrody oceniającej skuteczność licytacji. W każdym kroku zwracana jest różnica od przypadku idealnego. Definiując funkcję nagrody wspomagano się dostępnymi narzędziami, tj. Double Dummy Solver Bo Haglunda. Cel każdego z epizodów to ustalenie kontraktu, który stanowi zobowiązanie do wzięcia określonej liczby lew przez parę wygrywającą licytację.

## Wymagania wstępne

W pierwszej kolejności należy pobrać środowisko z tego repozytorium. Projekt można pobrać jako archiwum ZIP lub korzystając z opcji `clone`, ale wymagane jest wtedy posiadanie Gita:

```
git clone https://github.com/patrysma/gym-bridge-auction.git
```

Następnie należy spełnić poniższe warunki, aby środowisko mogło działać poprawnie.

- Rekomendowanym systemem operacyjnym jest Linux ze względu na to, że implementację i testy przeprowadzono na jego dystrybucji Ubuntu. Do testowania wykorzystano również serwer CentOS 7. Dodatkowo systemami wspieranymi przez OpenAI Gym są Linux i OS X. Systemu Windows można używać na własne ryzyko, jednak nie zagwarantowano poprawności działania wszystkich dostępnych opcji.

- Posiadanie zainstalowanego Pythona 3.5+.

- Wymagana instalacja następujących bibliotek Pythona: `pygame`, `cppyy`, `gym` i `numpy`. Można je zainstalować przy wykorzystaniu pakietu PIP w następujący sposób (przykład dla narzędzia OpenAI Gym):

```
python3 -m pip install gym
```

- Konieczna jest również instalacja biblioteki Double Dummy Solver oraz przygotowanego do niej wrappera - pliki `libdds.so` i `libddswrapper.so`. Można to zrobić na podstawie instrukcji opisanej poniżej. Narzędzia Double Dummy Solver nie trzeba pobierać z oficjalnej strony, bo w repozytorium projektu zamieszczono wszystkie niezbędne pliki, które otrzymano po kompilacji biblioteki (ścieżka `/gym_bridge_auction/envs/solver/dds` w repozytorium).
1. Najprostszym sposobem instalacji jest przekopiowanie `libdds.so` i `libddswrapper.so` do domyślnej lokalizacji, gdzie szukane są pliki bibliotek. Dla systemu Linux domyślne katalogi to `/usr/lib` lub `/lib`. Poniżej przedstawiono sposób instalacji biblioteki poprzez kopiowanie pliku `libdds.so` do folderu `/usr/lib`. Do realizacji wymagane są uprawnienia administratora. Podczas kopiowania podajemy odpowiednią ścieżkę do pliku.

```
sudo cp /home/patrycja/PycharmProjects/gym_bridge_auction/gym_bridge_auction/envs/solver/dds/src/libdds.so /usr/lib
```

2. Następnie należy uruchomić narzędzie `ldconfig`, które zaktualizuje pamięć podręczną bibliotek dostępnych w standardowych katalogach systemowych.

```
sudo ldconfig
```

3. Teraz można sprawdzić, czy pamięć podręczna została zaktualizowana za pomocą następującej komendy. 

```
ldconfig -p|grep dds
```

   Przedstawiony sposób instalacji biblioteki przez kopiowanie do standardowego katalogu jest najprostszy, ale istnieją też inne. Dodatkowo da się również definiować własne ścieżki poszukiwań plików bibliotek, zapisując je do pliku `/etc/ld.so.conf`.

- Po pobraniu środowiska z repozytorium trzeba je zainstalować, aby możliwe było jego użycie. W tym celu należy przejść w terminalu do folderu `gym-bridge-auction`, gdzie umieszczono wszystkie pliki ze środowiskiem oraz służący do instalacji `setup.py` (nazwę folderu głównego ustawić na `gym-bridge-auction`, jeśli jest inna). Następnie dokonać instalacji w następujący sposób:

```
python3 -m pip install gym-bridge-auction 
```

lub

```
python3 -m pip install -e .
```

  Korzystając z drugiego sposobu oprócz środowiska zainstalują się niezbędne biblioteki  `pygame` , `cppyy` , `gym` i `numpy`.

## Przykładowy kod prezentujący działanie środowiska

Aby przetestować działanie środowiska z interfejsem konsolowym można użyć poniższego kodu. Do testów wykorzystujących wersję graficzną należy przy renderowaniu podać opcję `'human'`, czyli: `env.render('human')`. Poniższy kod przedstawia działanie środowiska dla losowych działań agentów bez implementacji żadnego systemu uczącego.

```python
import gym_bridge_auction
import gym

PLAYERS_NAMES = ['N', 'E', 'S', 'W']

for i_episode in range(5):
    env = gym.make('BridgeAuction-v0')
    observation = env.reset()
    hands = {}
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
```

## Działanie środowiska

Poniżej przedstawiono wynik działania opisanego w poprzednim punkcie proframu dla jednego z epizodów i wersji konsolowej.
```
Dealer: W 
N hand:
♠ 9 7
♥ Q 9 6 3
♦ 10 9 3
♣ A 8 7 5
E hand:
♠ K Q 8 4 3
♥ K J 10
♦ J 6
♣ Q 6 4
S hand:
♠ J
♥ A 8 7 2
♦ A 5 2
♣ K 10 9 3 2
W hand:
♠ A 10 6 5 2
♥ 5 4
♦ K Q 8 7 4
♣ J

Observation space:
{'whose turn': None, 'whose next turn': 3, 'LAST_contract': None, 'Player_contract': None, 'winning_pair': None, 'double/redouble': 0, 'Players hand': [[0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0], [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1]]}

LAST_contract: 3NT
Pair: N/S E/W
Score: 100 -100
Optimum score: 420 -420

NORTH_contract: None
EAST_contract: None
SOUTH_contract: None
WEST_contract: 3NT

Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 21, 'double/redouble': 0, 
 'Player_contract': 21, 'winning_pair': 1}
Reward: [-320, 320]

LAST_contract: 6NT
Pair: N/S E/W
Score: -300 300
Optimum score: 420 -420

NORTH_contract: 6NT
EAST_contract: None
SOUTH_contract: None
WEST_contract: 3NT

Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 6, 'double/redouble': 0, 
 'Player_contract': 6, 'winning_pair': 0}
Reward: [-720, 720]

LAST_contract: 7NT
Pair: N/S E/W
Score: 300 -300
Optimum score: 420 -420

NORTH_contract: 6NT
EAST_contract: 7NT
SOUTH_contract: None
WEST_contract: 3NT

Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 1, 'double/redouble': 0, 
 'Player_contract': 1, 'winning_pair': 1}
Reward: [-120, 120]

LAST_contract: 7NT
Pair: N/S E/W
Score: 300 -300
Optimum score: 420 -420

NORTH_contract: 6NT
EAST_contract: 7NT
SOUTH_contract: pass
WEST_contract: 3NT

Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 1, 'double/redouble': 0, 
 'Player_contract': 0, 'winning_pair': 1}
Reward: [-120, 120]

LAST_contract: 7NT
Pair: N/S E/W
Score: 300 -300
Optimum score: 420 -420

NORTH_contract: 6NT
EAST_contract: 7NT
SOUTH_contract: pass
WEST_contract: pass

Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 0, 
 'Player_contract': 0, 'winning_pair': 1}
Reward: [-120, 120]

LAST_contract: 7NT
Pair: N/S E/W
Score: 300 -300
Optimum score: 420 -420

NORTH_contract: pass
EAST_contract: 7NT
SOUTH_contract: pass
WEST_contract: pass

Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 1, 'double/redouble': 0, 
 'Player_contract': 0, 'winning_pair': 1}
Reward: [-120, 120]
Episode 2 finished after 6 timesteps

```

Poniższy filmik ukazuje działanie środowiska dla tego samego rozdania. Wtedy `gym.make('BridgeAuction-v0')` umieszcza się przed pętlą.

[![Watch the video](https://i.imgur.com/UIgSQDV.jpg)](https://youtu.be/VSm32FQY6Bk)
