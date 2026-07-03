import tkinter as tk
from tkinter import ttk
from manager import LibraryManager
from book import Book

class LibraryGUI:

   def __init__(self, root):
      self.root = root
      self.manager = LibraryManager()
      self.root.title("Library Management System")
      self.root.configure(bg="#BCCCDF")
      self.root.geometry("1200x700")
      self.create_widgets()
      self.load_books()
      self.refresh_dashboard()
   def create_widgets(self):
      #heading
      heading = tk.Label(self.root,text="Library Management System",font=("cambria",20,"bold"),bg="#BCCCDF")
      heading.pack(pady=10)
      #Form frame
      form_frame = tk.Frame(self.root,bg="#94ADCD",border=10)
      form_frame.pack(pady=10)
      #Labels
      tk.Label(form_frame,text="Title",width=12,).grid(row=0,column=0,padx=5,pady=5)
      tk.Label(form_frame,text="Author",width=12).grid(row=1,column=0,padx=5,pady=5)
      tk.Label(form_frame,text="Publisher",width=12).grid(row=2,column=0,padx=5,pady=5)
      tk.Label(form_frame,text="Category",width=12).grid(row=3,column=0,padx=5,pady=5)
      tk.Label(form_frame,text="Price",width=12).grid(row=4,column=0,padx=5,pady=5)
      tk.Label(form_frame,text="Search",width=12).grid(row=5,column=0,padx=5,pady=5)
#dashboard frame
      dashboard_frame = tk.Frame(self.root, bg="#BCCCDF")
      dashboard_frame.pack(fill="x", padx=390 ,pady=15)
      #card values
      self.total_label = self.create_card(dashboard_frame, "Total Books", 0)
      self.available_label = self.create_card(dashboard_frame, "Available", 1)
      self.borrowed_label = self.create_card(dashboard_frame, "Borrowed", 2)
      self.purchased_label = self.create_card(dashboard_frame, "Purchased", 3)
      #Entry widgets
      self.title_entry = tk.Entry(form_frame,width=30)
      self.author_entry = tk.Entry(form_frame,width=30)
      self.publisher_entry = tk.Entry(form_frame,width=30)
      self.category_entry = tk.Entry(form_frame,width=30)
      self.price_entry = tk.Entry(form_frame,width=30)
      self.search_entry = tk.Entry(form_frame,width=30)
      self.borrower_entry = tk.Entry(form_frame,width=30)
      #Place Entries
      self.title_entry.grid(row=0,column=1,padx=5,pady=5)
      self.author_entry.grid(row=1,column=1,padx=5,pady=5)
      self.publisher_entry.grid(row=2,column=1,padx=5,pady=5)
      self.category_entry.grid(row=3,column=1,padx=5,pady=5)
      self.price_entry.grid(row=4,column=1,padx=5,pady=5)
      self.search_entry.grid(row=5,column=1,padx=5,pady=5)
      # button frame
      button_frame = tk.Frame(self.root, bg="#BCCCDF")
      button_frame.pack(pady=10)
      #buttons
      self.add_btn = tk.Button(button_frame,text="Add Book",font=("cambria",10,),width=12,command=self.add_book,bg="#D4A9F4")
      self.add_btn.grid(row=0, column=0, padx=5)

      self.update_btn = tk.Button(button_frame,text="Update",font=("cambria",10,),width=12,command=self.update_book,bg="#A9F4B8")
      self.update_btn.grid(row=0, column=1, padx=5)

      self.delete_btn = tk.Button(button_frame,text="Delete",font=("cambria",10,),width=12,command=self.delete_book,bg="#F4F4A9")
      self.delete_btn.grid(row=0, column=2, padx=5)

      self.search_btn = tk.Button(button_frame,text="Search",font=("cambria",10,),width=12,command=self.search_book,bg="#F4AFA9")
      self.search_btn.grid(row=0, column=3, padx=5)

      self.borrow_btn = tk.Button(button_frame,text="Borrow",font=("cambria",10,),width=12,command=self.borrow_book,bg="#B4F0C0")
      self.borrow_btn.grid(row=0, column=4, padx=5)

      self.return_btn = tk.Button(button_frame,text="Return",font=("cambria",10,),width=12,command=self.return_book,bg="#A9EBF4")
      self.return_btn.grid(row=0, column=5, padx=5)

      self.purchase_btn = tk.Button(button_frame,text="Purchase",width=12,command=self.purchase_book,bg="#F4E8A9")
      self.purchase_btn.grid(row=0, column=6, padx=5)

      self.borrow_btn = tk.Button(button_frame,text="Show All",font=("cambria",10,),width=12,command=self.load_books,bg="#E39CF7")
      self.borrow_btn.grid(row=0, column=7, padx=5)

      #tree view
      columns = ("ID","Title","Author","Publisher","Category","Price","Status")
      self.tree = ttk.Treeview(self.root,columns=columns,show="headings",height=30)
      #Create Column Headings
      for col in columns:
         self.tree.heading(col, text=col)
         self.tree.column(col, width=130)
      #stacking treeview
      self.tree.pack(fill="both", expand=True, padx=10, pady=10)
         
      self.tree.bind("<<TreeviewSelect>>", self.select_book)

   def create_card(self, parent, title, column):
         card = tk.Frame(parent, bg="#FFFFFF", bd=2, width=180, height=80)
         card.grid(row=0, column=column, padx=10)
         tk.Label(card,text=title,font=("Cambria", 12, "bold"),bg="white").pack(pady=(10, 0))
         value = tk.Label(card,text="0",font=("Cambria", 18, "bold"),bg="white",fg="#212637")
         value.pack()
         return value

   def refresh_dashboard(self):
      self.total_label.config(text=self.manager.get_total_books())
      self.available_label.config(text=self.manager.get_available_books())
      self.borrowed_label.config(text=self.manager.get_borrowed_books())
      self.purchased_label.config(text=self.manager.get_purchased_books())

   def load_books(self):
      # Remove old rows
      for row in self.tree.get_children():
        self.tree.delete(row)
      # Read books from database
      books = self.manager.display_books()
      # Insert each book
      for book in books:
         self.tree.insert("","end",values=(book.get_book_id(),book.get_title(),book.get_author(),book.get_publisher(),book.get_category(),book.get_price(),book.get_status()))
   def clear_entries(self):

      self.title_entry.delete(0, tk.END)
      self.author_entry.delete(0, tk.END)
      self.publisher_entry.delete(0, tk.END)
      self.category_entry.delete(0, tk.END)
      self.price_entry.delete(0, tk.END)

   def add_book(self):
      try:
        book = Book(self.title_entry.get(),self.author_entry.get(),self.publisher_entry.get(),self.category_entry.get(),float(self.price_entry.get()))
        self.manager.add_book(book)
        self.load_books()
        self.clear_entries()
        print("Book Added Successfully!")
      except ValueError:
        print("Price must be a number.")
      self.refresh_dashboard()

   def update_book(self):
      book = Book(self.title_entry.get(),self.author_entry.get(),self.publisher_entry.get(),self.category_entry.get(),float(self.price_entry.get()),book_id=self.selected_book_id)
      self.manager.update_book(book)
      self.load_books()
      self.clear_entries()
      self.refresh_dashboard()

   def delete_book(self):
      book = Book("","","","",0,book_id=self.selected_book_id)
      self.manager.delete_book(book)
      self.load_books()
      self.clear_entries()
      self.refresh_dashboard()

   def borrow_book(self):
    book = Book(self.title_entry.get(),self.author_entry.get(),self.publisher_entry.get(),self.category_entry.get(),float(self.price_entry.get()),book_id=self.selected_book_id,status=self.selected_status)
    self.manager.borrow_book(book,self.borrower_entry.get())
    self.load_books()
    self.refresh_dashboard()

   def return_book(self):
    book = Book(self.title_entry.get(),self.author_entry.get(),self.publisher_entry.get(),self.category_entry.get(),float(self.price_entry.get()),book_id=self.selected_book_id,status=self.selected_status)
    self.manager.return_book(book)
    self.load_books()

   def purchase_book(self):
    book = Book(self.title_entry.get(),self.author_entry.get(),self.publisher_entry.get(),self.category_entry.get(),float(self.price_entry.get()),book_id=self.selected_book_id,status=self.selected_status)
    self.manager.purchase_book(book)
    self.load_books()
    self.refresh_dashboard()

   def search_book(self):
    keyword = self.search_entry.get()
    books = self.manager.search_book(keyword)
    self.tree.delete(*self.tree.get_children())
    for book in books:
        self.tree.insert( "", "end",
            values=(
                book.get_book_id(),book.get_title(),book.get_author(),book.get_publisher(),book.get_category(),book.get_price(),book.get_status())
        )

   def select_book(self, event):
    selected = self.tree.focus()
    if not selected:
        return
    values = self.tree.item(selected, "values")
    self.selected_status=values[6]
    self.selected_book_id = values[0]
    self.title_entry.delete(0, tk.END)
    self.title_entry.insert(0, values[1])
    self.author_entry.delete(0, tk.END)
    self.author_entry.insert(0, values[2])
    self.publisher_entry.delete(0, tk.END)
    self.publisher_entry.insert(0, values[3])
    self.category_entry.delete(0, tk.END)
    self.category_entry.insert(0, values[4])
    self.price_entry.delete(0, tk.END)
    self.price_entry.insert(0, values[5])
