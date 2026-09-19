from database import connection

cursor=connection.cursor()

users=[["a1@gmail.com","$argon2id$v=19$m=65536,t=3,p=4$sxVzkEoPtCY3FBsb4DALVA$trnlmEBfWkDzB0xnw9XSkyA6R97qkzhGjpiILrTAcI8",3,"User",True],
       ["b1@gmail.com","$argon2id$v=19$m=65536,t=3,p=4$sxVzkEoPtCY3FBsb4DALVA$trnlmEBfWkDzB0xnw9XSkyA6R97qkzhGjpiILrTAcI8",4,"User",True]]

cursor.executemany("insert into users(Email,Password,User_id,Role,Email_verified) values(%s,%s,%s,%s,%s) on duplicate key update Email=Values(Email),Password=values(password),User_id=values(User_id),Role=values(Role),Email_Verified=values(email_verified)",users)

connection.commit()
cursor.close()



