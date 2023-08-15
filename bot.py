import coinbasepro as cbpro

client = cbpro.PublicClient()

result = client.get_products()

for row in result:
    print(row['id'])

