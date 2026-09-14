from flask import Flask,render_template,request,redirect,url_for
import  mysql.connector
from mysql.connector.aio import cursor

app = Flask(__name__)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user='root',
        password='123#@!krishn',
        database='book_db'
    )
# HOME PAGE - SHOW ALL BOOKS
@app.route("/")
def index():
    connection=None
    cursor=None
    try:
        connection=get_db_connection()
        cursor=connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        books=cursor.fetchall()
        return render_template("index.html",books=books)
    except mysql.connector.Error as error:
        return f"Database Error: {error}"
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
# add Book
@app.route("/add",methods=["GET","POST"])
def add_book():
    if request.method=="POST":
        title=request.form.get("title")
        author=request.form.get("author")
        price=request.form.get("price")
        status=request.form.get("status")
        connection=None
        cursor=None
        try:
            connection=get_db_connection()
            cursor=connection.cursor()
            query="""INSERT INTO books (title,author,price,status) VALUES (%s,%s,%s,%s)"""
            values=(title,author,price,status)
            cursor.execute(query,values)
            connection.commit()
            return  redirect(url_for("index"))
        except mysql.connector.Error as error:
            return f"Database Error: {error}"
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    return render_template("add_book.html")
# EDIT BOOK
@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit_book(id):
    connection=None
    cursor=None
    try:
        connection=get_db_connection()
        cursor=connection.cursor(dictionary=True)
        if request.method=="POST":
            title=request.form["title"]
            author=request.form["author"]
            price=request.form["price"]
            status=request.form["status"]
            query="""UPDATE books SET title=%s,author=%s,price=%s,status=%s WHERW id=%s"""
            values=(title,author,price,status,id)
            cursor.execute(query,values)
            connection.commit()
            return redirect(url_for("index"))
#         GET=show existing books data
        cursor.execute("""SELECT * FROM books WHERE id=%s""", (id,))
        book=cursor.fetchone()
        if book is None:
            return "Book not found"
        return render_template("edit_book.html",book=book)
    except mysql.connector.Error as error:
        return f"Database Error: {error}"
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
# Delete books
@app.route("/delete/<int:id>")
def delete_book(id):
    connection=None
    cursor=None
    try:
        connection=get_db_connection()
        cursor=connection.cursor()
        query="""
        DELETE FROM books WHERE id=%s"""
        cursor.execute(query,(id,))
        connection.commit()
        return redirect(url_for("index"))
    except mysql.connector.Error as error:
        return f"Database Error: {error}"
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
#             SEARCH BOOK
@app.route("/search")
def search_book():
    search=request.args.get("q","")
    connection=None
    cursor=None
    try:
        connection=get_db_connection()
        cursor=connection.cursor(dictionary=True)
#         Search title or author
        query="""SELECT * FROM books WHERE title LIKE %s OR author LIKE %s"""
        search_values="%"+search+"%"
        cursor.execute(query,(search_values,search_values))
        books=cursor.fetchall()
        return render_template("index.html",books=books,search=search)
    except mysql.connector.Error as error:
        return f"Database Error: {error}"
    finally:
        if cursor:
           cursor.close()
        if connection and connection.is_connected():
            connection.close()
            

if __name__ == '__main__':
    app.run(debug=True)