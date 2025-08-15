import requests,time

# # start bot
# r=requests.post("http://127.0.0.1:5000/start_stop", json={"action": "start"})

# #stop bot
# r=requests.post("http://127.0.0.1:5000/start_stop", json={"action": "stop"})


# #check ballance host
# requests.post("http://127.0.0.1:5000/market", json={"action": "get_ballance"})


# ##buy host
# requests.post("http://127.0.0.1:5000/market", json={
#     "action": "buy",
#     "symbol": "beamx_usdt",
#     "amount": 1000
# })
# ##sell host
# requests.post("http://127.0.0.1:5000/market", json={
#     "action": "sell",
#     "symbol": "eth_usdt",
#     "amount": 500
# })

# get close open price

# r=requests.post("http://127.0.0.1:5000/market", json={
#     "action": "get_close_open",
#     "symbol": "eth_usdt",
# })



# print(r.status_code)  # 200
# print(r.json())  