import psycopg2

conn = psycopg2.connect(dbname="Security Platform", user="postgres", password="si4848748", port="8888")

cur = conn.cursor()

cur.execute("select * from role natural join role_right")
rows = cur.fetchall()
print('------------------------------------------------------------------')
for row in rows:
    print(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]))
print('------------------------------------------------------------------')

conn.commit()

conn.close()