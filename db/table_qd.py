def create_table_qd(con,table_name="qd"):
    """
    签到表：                                    注：group为关键字，需要输入[group]
    学生学号： student_id
    签到时间： sign_time
    
    return:
    True : 创建成功    False : 创建失败
    """

    cursor=con.cursor()
    try:
        cursor.execute("CREATE TABLE "+ table_name+" ("
                    "student_id INT PRIMARY KEY,"
                    "sign_time FLOAT)")
        con.commit()
        print("table "+table_name+" is created")
        return True
    except Exception as e:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        if result:
            print("table "+table_name+" is already exists")
        else:
            print("Create Table Failed")
            print(e)
        return False
    
def insert_table_qd(con,table_name,student_id,sign_time):
    cursor=con.cursor()
    try:
        sql="INSERT INTO "+table_name+" (student_id,sign_time) VALUES(?,?)"
        cursor.execute(sql,(student_id,sign_time))
        con.commit()
        print("Successfully Insert")
        return True
    except:
        print("Insert Failed")
        con.rollback()
        return False