from database import connection

cursor=connection.cursor()

books=[[1,123,"chem","Daffodil"]]
cursor.executemany("""insert into books(book_id,book_isbn,book_name,author_name)values(%s,%s,%s,%s) 
        
        on duplicate key update 

        book_id=values(book_id),
        book_isbn=values(book_isbn),
        book_name=values(book_name),
        author_name=values(author_name)
                      """
                   ,books)


connection.commit()
cursor.close()

