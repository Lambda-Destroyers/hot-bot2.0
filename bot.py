import coinbasepro as cbpro

data = open('auth_key.txt', 'r').read().splitlines()
# print(data)

public = data[0]
passphrase = data[1]
secret = data[2]

auth_client = cbpro.AuthenticatedClient(public, secret, passphrase)

order = auth_client.place_limit_order(
    product_id='ETH-USD',
    side='buy', # specify 'buy' or 'sell'
    price='100.00',
    size='0.01',
    post_only=True, # ensures this is only posted and not immediately matched
)

print("Order placed: ", order)







# client = cbpro.PublicClient()

# result1 = client.get_products()
# result2 = client.get_currencies()

# result3 = client.get_product_order_book('BTC-USD', level=1)
# result4 = client.get_product_ticker('BTC-USD')
# result5 = client.get_product_24hr_stats('BTC-USD')


# for row in result1:
#     print(row['id'])

# for row in result2:
#     print(row['id'])

# print(result3)
# print(result4)
# print(result5)


