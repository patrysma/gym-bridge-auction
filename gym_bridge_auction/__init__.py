from gym.envs.registration import register

register(id='BridgeAuction-v0',
         entry_point='gym_bridge_auction.envs:AuctionEnv',
         )
