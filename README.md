# Środowisko do licytacji brydżowej

Środowisko wieloagentowe (czterech graczy) symulujące licytację brydżową wykorzystujące interfejs biblioteki Gym.

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
spaces.Dict({'whose turn': spaces.Discrete(self.n_players),
             'whose next turn': spaces.Discrete(self.n_players),
             'LAST_contract': spaces.Discrete(36),
             'NORTH_contract': spaces.Discrete(36),
             'EAST_contract': spaces.Discrete(36),
             'SOUTH_contract': spaces.Discrete(36),
             'WEST_contract': spaces.Discrete(36),
             'winning_pair': spaces.Discrete(self.n_players / 2),
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

# Działanie z kontrą i rekontrą

[![Watch the video](https://i.imgur.com/aTB0rmc.jpg)](https://youtu.be/zd-wa3wE75I)

Poniżej przedstawiono wartości nagrody i przestrzeń obserwacji dla powyższego działania.

Pierwszy epizod:

```
Observation space:
{'whose turn': None, 'whose next turn': 3, 'LAST_contract': None, 'NORTH_contract': None, 'EAST_contract': None, 'SOUTH_contract': None, 'WEST_contract': None, 'winning_pair': None, 'double/redouble': 0}
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 14, 'double/redouble': 0, 'winning_pair': 1, 'WEST_contract': 14}
Reward: -300
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 7, 'double/redouble': 0, 'winning_pair': 0, 'NORTH_contract': 7}
Reward: -450
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 7, 'double/redouble': 1, 'winning_pair': 0, 'EAST_contract': 36}
Reward: 1000
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 7, 'double/redouble': 1, 'winning_pair': 0, 'SOUTH_contract': 0}
Reward: 0
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 6, 'double/redouble': 0, 'winning_pair': 1, 'WEST_contract': 6}
Reward: -200
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 4, 'double/redouble': 0, 'winning_pair': 0, 'NORTH_contract': 4}
Reward: -300
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 4, 'double/redouble': 1, 'winning_pair': 0, 'EAST_contract': 36}
Reward: 1000
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 2, 'double/redouble': 0, 'winning_pair': 0, 'SOUTH_contract': 2}
Reward: -500
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 0, 'winning_pair': 1, 'WEST_contract': 1}
Reward: -250
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 1, 'double/redouble': 0, 'winning_pair': 1, 'NORTH_contract': 0}
Reward: 0
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 1, 'double/redouble': 0, 'winning_pair': 1, 'EAST_contract': 0}
Reward: 0
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 1, 'double/redouble': 0, 'winning_pair': 1, 'SOUTH_contract': 0}
Reward: 0
Episode finished after 12 timesteps
```

Drugi epizod:

```
Observation space:
{'whose turn': None, 'whose next turn': 3, 'LAST_contract': None, 'NORTH_contract': None, 'EAST_contract': None, 'SOUTH_contract': None, 'WEST_contract': None, 'winning_pair': None, 'double/redouble': 0}
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 17, 'double/redouble': 0, 'winning_pair': 1, 'WEST_contract': 17}
Reward: -50
Observation space:
{'whose turn': 0, 'whose next turn': 1, 'LAST_contract': 2, 'double/redouble': 0, 'winning_pair': 0, 'NORTH_contract': 2}
Reward: -500
Observation space:
{'whose turn': 1, 'whose next turn': 2, 'LAST_contract': 1, 'double/redouble': 0, 'winning_pair': 1, 'EAST_contract': 1}
Reward: -250
Observation space:
{'whose turn': 2, 'whose next turn': 3, 'LAST_contract': 1, 'double/redouble': 1, 'winning_pair': 1, 'SOUTH_contract': 36}
Reward: 1000
Observation space:
{'whose turn': 3, 'whose next turn': 0, 'LAST_contract': 1, 'double/redouble': 2, 'winning_pair': 1, 'WEST_contract': 37}
Reward: 1000
Episode finished after 5 timesteps
```

# Algorytm wyznaczenia nagrody

Oznaczenia:
- dek_licz_lew - deklarowana liczba lew przez gracza podczas licytacji (dla danego koloru atutowego)
- maks_dek_licz_lew - maksymalna liczba lew jaką gracz może wziąć z partnerem przy ustalonym mianie kontraktu
- mnożnik_kary - czyli kara za możliwość wzięcia mniej lew niż zadeklarowno (-50 za każdą)
- mnożnik_koloru - wartość punktowa za wzięcie lewy do wyznaczenia nagrody w zależności od miana (20 dla C/D; 30 dla H/S; 40 za pierwszą i 30 za kolejne dla NT)
- bonus - wartość dodatkowa za najbardziej punktowany kontrakt (50 pkt)

```
Jeśli kontrakt to pas:
  nagroda = 0
Jeśli kontrakt jest różny od pasu:
  Jeśli kontrakt jest nierealizowalny według solvera:
    nagroda = mnożnik_kary * (dek_licz_lew - maks_dek_licz_lew)
  Jeśli kontrakt jest realizowalny:
    Jeśli dek_licz_lew <= maks_dek_licz_lew:
      nagroda = mnożnik_koloru * (dek_licz_lew - maks_dek_licz_lew)
      Jeśli kontrakt jest równy najbardziej punktowanemu:
        nagroda = nagroda + bonus
```
Implementacja funkcji nagrody jest następująca:

```python
if action == 0:
    self.reward = 0
else:
    bind_trump = self.available_contracts[action].suit
    bind_number = self.available_contracts[action].number
    max_contract = self.players[player_index].makeable_contracts[bind_trump]
    max_number_of_tricks = self.players[player_index].number_of_trick[bind_trump]

    if max_contract == 0:
        self.reward = POINTS['FAIL'] * (bind_number + 6 - max_number_of_tricks)
    elif bind_number <= max_contract:
        if bind_trump == 'NT':
            self.reward = POINTS['NT'][0] + (bind_number - 1) * POINTS['NT'][1]
        else:
            self.reward = POINTS[bind_trump] * bind_number

        if (bind_trump in self.players[player_index].max_contract_trump) and bind_number == max_contract:
            self.reward += POINTS['BONUS']
```

