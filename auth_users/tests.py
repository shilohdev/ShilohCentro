
class Connection:
    def __init__(self, db, table, condition, inner, params):
        self.db = db
        self.table = table
        self.conn = connections[self.db].cursor()
        self.condition = condition
        self.inner = inner
        self.params = params

    def connect(self):
        return self.conn

    def execute(self, query):
        self.conn.execute(query)
        return self.conn.fetchall()

    def insert(self, query, params=None):
        self.conn.execute(query, params) if params else self.conn.execute(query)
        return self.conn

    def fetch(self, column, params):
        if params:
            self.conn.execute("SELECT {} FROM {} {} {}".format(dealStrignify(column), self.table, self.inner, self.condition), self.params)
        else:
            self.conn.execute("SELECT {} FROM {} {} {}".format(dealStrignify(column), self.table, self.inner, self.condition))

        return self.conn.fetchall()

    def update(self, params):
        if params:
            self.conn.execute("UPDATE {} SET {}".format(self.table, self.condition), params)
        else:
            self.conn.execute("UPDATE {} SET {}".format(self.table, self.condition))

        return self.conn.rowcount

    def close(self):
        return self.conn.close()

    def connection(self):
        return connections[self.db].cursor()
        
    def execUpdate(self, table, column, condition, params):
        self.conn.execute("UPDATE {} SET {} = %s WHERE {} = %s".format(table, column, condition), params)
        return self.conn.rowcount

    def execRow(self, dictFetch, dictUpdate):
        table = dictFetch["table"]
        d_column = dictFetch["column"]
        d_condition = dictFetch["condition"]
        params = dictFetch["params"]

        column = ""
        for k in d_column.split(","):
            column += "{}, ".format(k.strip())
        column = column[:-2]

        condition = ""
        for k in d_condition.split(","):
            condition += "{} = %s AND ".format(k.strip())
        
        condition = condition[:-5]
        
        self.conn.execute("SELECT {} FROM {} WHERE {}".format(column, table, condition), params)
        dados = self.conn.fetchall()
        if dados:
            table = dictUpdate["table"]
            d_column = dictUpdate["column_update"]
            d_condition = dictUpdate["condition"]
            params = dictUpdate["params_update"]

            column = ""
            for k in d_column.split(","):
                column += "{} = %s, ".format(k.strip())
            column = column[:-2]

            condition = ""
            for k in d_condition.split(","):
                condition += "{} = %s AND ".format(k.strip())
            
            condition = condition[:-5]
            
            self.conn.execute("UPDATE {} SET {} WHERE {}".format(table, column, condition), params)
        else:
            table = dictUpdate["table"]
            d_column = dictUpdate["column"]
            params = dictUpdate["params_insert"]

            column = ""
            for k in d_column.split(","):
                column += "`{}`, ".format(k.strip())
            column = column[:-2]

            condition = ""
            for k in d_column.split(","):
                condition += "%s, ".format(k.strip())

            condition = condition[:-2]

            self.conn.execute("INSERT {} ({}) VALUES ({})".format(table, column, condition), params)

        return self.conn.rowcount


db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO

db.table = "auth_users.users p" #VAR COM CONEEXAO TAVLE
db.condition = "WHERE p.id = %s AND JFKSJAFNAOJSDFHASHUJ" #VAR COM A CONDDIÇÃO UTILIZADA NO BANCO
db.params = (id_user,) #VAR COM O PARAM
