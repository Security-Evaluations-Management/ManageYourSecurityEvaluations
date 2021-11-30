import psycopg2


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(dbname="Security Platform", user="postgres", password="si4848748", port="8888")
        self.cur = self.conn.cursor()

    # search whether user is inside the
    def search_user(self, email):
        self.cur.execute("select * from employee where email=(%s)", (email,))
        rows = self.cur.fetchall()
        return rows

    # check whether the employee exist in the database through email
    # return True: if the employee email exist in the DB
    def check_if_user_exist(self, email):
        rows = self.search_user(email)
        return bool(rows)

    # get user's saved password via email
    # need check user exist or not before call this method
    def get_user_hashed_password(self, email):
        return self.search_user(email)[3]

    # add a new employ into the database
    # need check user exist or not before call this method
    def add_new_user(self, name, email, hash_value):
        self.cur.execute("insert into employee(name, email, hash_value) VALUES(%s,%s,%s)", (name, email, hash_value))
        self.conn.commit()

        # remove below things if function works
        print('------------------------------------------------------------------')
        self.cur.execute("select * from employee")
        rows = self.cur.fetchall()
        for row in rows:
            print(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]))

# self.conn.commit()

# conn.close()