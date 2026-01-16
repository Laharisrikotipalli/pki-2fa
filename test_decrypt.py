import requests

# The long string you received from the instructor API
encrypted_seed = "cVgmBdIVGI9Z9kUJ6tK7wdX/1De5JMrtEpjVXyVEecJOMqwTEHg0DPFxhoneExqCosQE7yaLrZxXJ4HDwC3YNqFdtr3SxjC9Cq7LeA2TbLkecWX5xueQO4JKd6HVqNSbXV6IJ7RMKS70j9VzhwwDoFrF50Cm+Nvz1NK6v7n62gMZbfzpaOczTeQayGUmSpKHoO46mlrlJme8/hciHG7GoFfEeZF/V93uUqztTrxZezPs8IDws0w3mNGtjZhhEYNhDvw4QsOXiyT1QpNOQyggFXrceASDDDasNcfKCKypb4Mw/6xDwUjiYTYybta9WnTMm8blshzQUUuk3k/t3cYhdx3dRyuXFced8Hj8ACz99s5HwevsmRPWJ6aA3d3k2Fk+bBUP2oNEEXL2H+jwAJicmARNk6QVa9hMQiLwang5phPm+f5ib6G7p/AMxCczQz2NeKX9m4048vsuxQZFzCJyUuCot2HkfhWlKsZh6I+rN0a9oOKSy0f5YvTkSPd2yz8KJ981P+dza9D7shOlN+604QmP51LSX4d0Ybt6gQCS3q4kyy7hQX3+NRKWRfeI9GOjVlw99DjRWfPBC3CF4F4zuC9SPmTsr6+b4FpI3UlaL0lTFfNFc2NH6zo7LSM/p6UAZZ5vwQ4lPntue2YvC59x9JzuLFVYLbTUXsP3vYO1WwA="

url = "http://localhost:8080/decrypt-seed"
payload = {"encrypted_seed": encrypted_seed}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Success! Response:", response.json())
else:
    print(f"Error {response.status_code}: {response.text}")