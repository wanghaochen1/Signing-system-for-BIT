from db import *
# from db.table_teacher import *




con=sql_connection()
create_table_teacher(con)
create_table_course(con)
insert_table_teacher(con,"teacher",1,"张三","123456")
insert_table_teacher(con,"teacher",2,"李四","123456")
teacher=select_table(con,"teacher",teacher_id=1)
print(teacher)