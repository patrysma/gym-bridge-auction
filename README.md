# Środowisko do licytacji brydżowej

Środowisko wieloagentowe (czterech graczy) symulujące licytację brydżową wykorzystujące interfejs biblioteki Gym.

W tym środowisku agenci wykonują kolejno pojedyńcze akcje (licytują). Dlatego funkcja `step()` przyjmuje tylko jedno działanie agenta, który zgodnie z ustaloną kolejnością powinien licytować i zwraca jedną obserwację, nagrodę i informację czy należy zresetować środowisko (czy otrzymano 3 pasy po kolei, czyli zakończono licytację). 

Przestarzeń akcji zdefiniowano następująco: 
```python 
spaces.Discrete(36)
``` 
Poszczególne liczby oznaczają różne odzywki licytacyjne. Przestrzeń akcji zmniejsza się (gdy agenci nie pasują) w każdym kroku i zawiera odzywki wyższe od ostatniej wypowiedzianej. Oznaczenia przedstawiono poniżej.

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

Przestrzeń obserwacji zdefiniowano następująco:

```python
spaces.Dict({'whose turn': spaces.Discrete(self.n_players),
             'whose next turn': spaces.Discrete(self.n_players),
             'LAST_contract': spaces.Discrete(36),
             'NORTH_contract': spaces.Discrete(36),
             'EAST_contract': spaces.Discrete(36),
             'SOUTH_contract': spaces.Discrete(36),
             'WEST_contract': spaces.Discrete(36),
             'winning_pair': spaces.Discrete(self.n_players / 2)})
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


Działanie środowiska przetestowano w systemie Linux.

Aby użyć środowiska konieczne jest zainstalowanie następujących bibliotek: `pygame` , `cppyy` i `gym`.

Należy również przekopiować następujące pliki: `libdds.so` i `libddswrapper.so` do folderu `/usr/lib` w swoim systemie.

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

# Działanie opcji z interfejsem graficznym:

[![Watch the video](https://i.imgur.com/058RZlw.jpg)](https://youtu.be/DybSAue5bYY)  

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
    Jeśli dek_licz_lew > maks_dek_licz_lew:
      nagroda = mnożnik_kary * (dek_licz_lew - maks_dek_licz_lew)
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
    else:
        if bind_number > max_contract:
            self.reward = POINTS['FAIL'] * (bind_number + 6 - max_number_of_tricks)
        elif bind_number <= max_contract:
            if bind_trump == 'NT':
                self.reward = POINTS['NT'][0] + (bind_number - 1) * POINTS['NT'][1]
            else:
                self.reward = POINTS[bind_trump] * bind_number

            if (bind_trump in self.players[player_index].max_contract_trump) and bind_number == max_contract:
                self.reward += POINTS['BONUS']
```

