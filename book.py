
class Book:
    def __init__(self,title,author,publisher,category,price,book_id=None,status="Available",borrower_name=""):
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__publisher = publisher
        self.__category = category
        self.__price = price
        self.__status = status
        self.__borrower_name = borrower_name

    def get_book_id(self):return self.__book_id
    def get_title(self):return self.__title
    def get_author(self):return self.__author
    def get_publisher(self): return self.__publisher
    def get_category(self): return self.__category
    def get_price(self):return self.__price
    def get_status(self):return self.__status
    def get_borrower_name(self):return self.__borrower_name


    def borrow_book(self, borrower_name):
        if self.__status == "Available":
            self.__status = "Borrowed"
            self.__borrower_name = borrower_name
            return True
        return False

    def return_book(self):
        if self.__status == "Borrowed":
            self.__status = "Available"
            self.__borrower_name = ""
            return True
        return False

    def purchase_book(self):
        if self.__status == "Available":
            self.__status = "Purchased"
            return True
        return False
    
    def get_details(self):
        return (
            f"ID: {self.__book_id}\nTitle: {self.__title}\nAuthor: {self.__author}\nPublisher: {self.__publisher}\nCategory: {self.__category}\nPrice: Rs.{self.__price:}\nStatus: {self.__status}\nBorrower: {self.__borrower_name if self.__borrower_name else 'None'}")

    def __str__(self):
        return f"{self.__title} by {self.__author} ({self.__status})"