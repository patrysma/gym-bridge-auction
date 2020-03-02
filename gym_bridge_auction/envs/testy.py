import gym
import gym_bridge_auction

env = gym.make('BridgeAuction-v0')
env.render()

a = [1, 2, 3, 4, 1, 2, 3]
b = [ [] for i in range(4)]

for i  in  range(0,len(a)):
    if a[i] == 1:
        b[0].append(a[i])
    elif a[i] == 2:
        b[1].append(a[i])
    elif a[i]==3:
        b[2].append(a[i])
    elif a[i]==4:
        b[3].append(a[i])

print(b)

a = '1'
b = int(a)

print(b.__class__)



