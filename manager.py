import sqlite3
from book import Book
from abc import ABC, abstractmethod

class LibraryOperations(ABC):
    @abstractmethod
    def add_book(self,book):
        pass
    @abstractmethod
    def update_book(self,book):
        pass
    @abstractmethod
    def delete_book(self,book):
        pass
    @abstractmethod
    def borrow_book(self,book):
        pass
    @abstractmethod
    def return_book(self,book):
        pass
    @abstractmethod
    def purchase_book(self,book):
       pass
    @abstractmethod
    def search_book(self,keyword):
        pass
    @abstractmethod
    def display_books(self):
        pass
    @abstractmethod
    def close(self):
        pass
class LibraryManager(LibraryOperations):
    def __init__(self):
        self.conn=sqlite3.connect("library.db")
        self.cursor=self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT,publisher TEXT, category TEXT, price REAL,status TEXT, borrower_name TEXT )""")
        self.conn.commit()

    def add_book(self,book:Book):
        self.cursor.execute("""INSERT INTO books(title,author,publisher,category,price,status,borrower_name) VALUES(?,?,?,?,?,?,?) """,(book.get_title(),book.get_author(),book.get_publisher(),book.get_category(),book.get_price(),book.get_status(),book.get_borrower_name()))
        self.conn.commit()

    def display_books(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        books = []
        for i in rows:
            book = Book(i[1], i[2], i[3],  i[4], i[5], i[0],  i[6],  i[7])
            books.append(book)
        return books    
    def update_book(self,book:Book):
        self.cursor.execute("""UPDATE books SET title=?,author=?,publisher=?,category=?,price=? WHERE id=?""",(book.get_title(),book.get_author(),book.get_publisher(),book.get_category(),book.get_price(),book.get_book_id()))
        self.conn.commit()
    
    def delete_book(self,book:Book):
        self.cursor.execute("""DELETE FROM books WHERE id=?""",(book.get_book_id(),))
        self.conn.commit()
    
    def borrow_book(self,book:Book,borrower_name):
        if book.borrow_book(borrower_name):
            self.cursor.execute("""UPDATE books SET status=? ,borrower_name=? WHERE id=?""",(book.get_status(),book.get_borrower_name(),book.get_book_id()))
            self.conn.commit()
        
    def return_book(self,book:Book):
        if book.return_book():
            self.cursor.execute("""UPDATE books SET status=? ,borrower_name=? WHERE id=?""",(book.get_status(),book.get_borrower_name(),book.get_book_id()))
            self.conn.commit()
       
    def purchase_book(self,book:Book):
        if book.purchase_book():
                self.cursor.execute("""UPDATE books SET status=? WHERE id=?""",(book.get_status(),book.get_book_id()))
                self.conn.commit() 

    def search_book(self,keyword):
        self.cursor.execute("""SELECT * FROM books WHERE id LIKE ? OR title LIKE ? OR author LIKE ? OR category LIKE ? """,(f"%{keyword}%",f"%{keyword}%",f"%{keyword}%",f"%{keyword}%"))
        rows = self.cursor.fetchall()
        books = []
        for i in rows:
            book = Book(i[1], i[2], i[3],  i[4], i[5], i[0],  i[6],  i[7])
            books.append(book)
        return books   
    def get_total_books(self):
        self.cursor.execute("SELECT COUNT(*) FROM books")
        total=self.cursor.fetchone()[0]
        return total
    def get_available_books(self):
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE status=?",("Available",))
        available=self.cursor.fetchone()[0]
        return available
    def get_borrowed_books(self):
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE status=?",("Borrowed",))
        borrowed=self.cursor.fetchone()[0]
        return borrowed
    def get_purchased_books(self):
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE status=?",("Purchased",))
        purchased=self.cursor.fetchone()[0]
        return purchased
    def close(self):
        self.conn.close()
