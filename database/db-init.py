import sqlite3

def create_tables(): #possibilidade de passar o nome como parâmetro
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            username TEXT PRIMARY KEY,
            senha TEXT,
            status TEXT,
            colecao_cartas TEXT,
            qtd_baralhos INTEGER,
            baralhos TEXT
        )
    ''')
        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carta (
            emocao TEXT PRIMARY KEY,
            tempo TEXT,
            impacto_social TEXT,
            efeito_cognitivo TEXT,
            qtd_emocoes_opostas INTEGER,
            qtd_emocoes_relacionadas INTEGER,
            intensidade INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def insert_data():
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cartas = [
        #emocao, tempo, impacto_social, efeito_cognitivo, qtd_emocoes_opostas, qtd_emocoes_relacionadas, intesidade
        ('autoestima', 'anos', 'positivo', 'certeza', 1, 1, 5),
        ('raiva', 'minutos', 'negativo', 'confusão', 2,6,5)
    ]
    cursor.executemany('INSERT INTO carta VALUES (?, ?, ?, ?, ?, ?, ?)', cartas)
    
    #usuario adm
    cursor.execute('INSERT INTO usuario VALUES (?, ?, ?, ?, ?, ?)', ['admin', 'admin123', 'offline', '["autoestima","raiva"]', 0, ''])

    conn.commit()
    conn.close()

create_tables()
insert_data()

# # testar se inseriu:
# conn = sqlite3.connect('database.db')
# cursor = conn.cursor()

# cursor.execute('SELECT * FROM usuario')
# result = cursor.fetchall()
# if result:
#     columns = [description[0] for description in cursor.description]
#     # metadata = "| " + " | ".join(columns) + " |"
#     # print(metadata)
#     # print("-" * (len(metadata)))
#     count=0
#     for row in result:
#         print('\nLinha', str(count),':')
#         i = 0
#         for item in row:
#             print(columns[i],'=',str(item))
#             i+=1
#         count+=1

# else:
#     print("Nenhum resultado encontrado =(")


# cursor.close()
# conn.close()
