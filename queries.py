from sqlite3 import Connection
from database import get_db
import json



def insert_data(table_name : str, data : tuple[str|int|float|bool], con : Connection = get_db()) :
    connexion = next(con) 
    try : 
        cursor = connexion.cursor()
        table_info = cursor.execute(f"PRAGMA table_info({table_name});").fetchall()
        columns = tuple([c[1] for c in table_info][1:])
        query = f"INSERT INTO {table_name}{columns} VALUES {data}"
        print(query)
        cursor.execute(query)
        connexion.commit()
        print("SUCCES")
                
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        con.close() 
    


def update_data(table_name : str, column_name : str, new_value : str|int|float|bool, id_to_modify : int, con : Connection = get_db()):
    connexion = next(con) 
    try : 
        cursor = connexion.cursor()
        query = f"UPDATE {table_name} SET {column_name} = {new_value} WHERE id = {id_to_modify}"
        cursor.execute(query)
        connexion.commit()
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally : 
        con.close()



def delete_data(table_name : str, id_to_delete, con : Connection = get_db()):
    connexion = next(con) 
    try : 
        cursor = connexion.cursor()
        query = f"DELETE FROM {table_name} WHERE id = {id_to_delete}"
        cursor.execute(query)
        connexion.commit()
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally : 
        con.close()





if __name__ == "__main__" : 
    
    values = ("4650", "180", "200", 360, 134, 286, 333, "sub_1")
    insert_data("performance", values)




