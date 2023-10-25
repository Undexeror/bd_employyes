import tkinter as tk
from tkinter import ttk
import sqlite3

#Класс главного окна
class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

##########################################################################################################
    #Создание и работа с главным окном
    def init_main(self):
        #Создаем панель инструментов
        toolbar = tk.Frame(bg = '#d7d7d7', bd =2)
        

        # упаковка
        toolbar.pack(side = tk.TOP, fill = tk.X)

##########################################################################################################

        #ДОБАВИТЬ
        self.imd_add = tk.PhotoImage(file = './img/add.png')
        # Создание кнопки с картинкой
        but_add = tk.Button(toolbar,text = 'Добавить', bg = '#d7d7d7',
                            bd = 0, image = self.imd_add, command = self.open_child)
        but_add.pack(side = tk.LEFT)

        # ИЗМЕНИТЬ
        self.update_img = tk.PhotoImage(file = './img/update.png')
        but_edit_dialog = tk.Button(toolbar,text = 'Изменить', bg = '#d7d7d7',
                            bd = 0, image = self.update_img, command = self.open_update_dialog)
        but_edit_dialog.pack(side = tk.LEFT)

        # УДАЛИТЬ
        self.delete_img = tk.PhotoImage(file = './img/delete.png')
        but_delete = tk.Button(toolbar,text = 'Удалить', bg = '#d7d7d7',
                            bd = 0, image = self.delete_img, command = self.delete_record)
        but_delete.pack(side = tk.LEFT)

        # ПОИСК
        self.search_img = tk.PhotoImage(file = './img/search.png')
        but_search = tk.Button(toolbar,text = 'Посик', bg = '#d7d7d7',
                            bd = 0, image = self.search_img, command = self.open_search)
        but_search.pack(side = tk.RIGHT)

        #ОБНОВИТЬ
        self.refresh_img = tk.PhotoImage(file = './img/refresh.png')
        but_refresh = tk.Button(toolbar,text = 'Удалить', bg = '#d7d7d7',
                            bd = 0, image = self.refresh_img, command = self.view_records)
        but_refresh.pack(side = tk.LEFT)




##########################################################################################################

        #Добавляем столбцы
        self.tree = ttk.Treeview(self,columns=('ID','name', 'phone','email','salary'),
                                height= 45, show = 'headings')
        
        #устанавливаем размеры столбцов
        self.tree.column('ID',width = 30, anchor = tk.CENTER)
        self.tree.column('name',width = 200, anchor = tk.CENTER)
        self.tree.column('phone',width = 150, anchor = tk.CENTER)
        self.tree.column('email',width = 150, anchor = tk.CENTER)
        self.tree.column('salary',width = 100, anchor = tk.CENTER)
        
        #Задаем имена
        self.tree.heading('ID', text = 'ID')
        self.tree.heading('name', text = 'ФИО')
        self.tree.heading('phone', text = 'Номер телефона')
        self.tree.heading('email', text = 'E-mail')
        self.tree.heading('salary', text = 'Зарплата')
        
        self.tree.pack(side = tk.LEFT)

        #Ползунок
        scroll = tk.Scrollbar(self, command = self.tree.yview)
        scroll.pack(side =tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

##########################################################################################################
    #Метод добавления данных
    def records(self, name, phone, email,salary):
        self.db.insert_data(name, phone, email,salary)
        self.view_records()
    # Метод обновления(изменения) данных
    def update_records(self, name, phone, email, salary):
        Id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cursor.execute('''UPDATE Users SET name=?, phone=?, email=?, salary=?
        WHERE ID=?''', (name, phone, email, salary, Id))
        self.db.connect.commit()
        self.view_records()



    # Вывод данных в таблицу на главном экране
    def view_records(self):
        self.db.cursor.execute('''SELECT * FROM Users''')

        # Удалить все из виджета
        [self.tree.delete(i) for i in self.tree.get_children()]


        #добавить все данные в таблице
        [self.tree.insert('','end',values = row)
         for row in self.db.cursor.fetchall()]


    #УДАЛЕНИЕ ЗАПИСЕЙ
    def delete_record(self):
        #Цикл по выделенным записям
        for selection_item in self.tree.selection():
            #удаляем из БД
            self.db.cursor.execute('''DELETE FROM Users WHERE ID=?''', (self.tree.set(selection_item, '#1'),))
        self.db.connect.commit()
        self.view_records()
    #ПОИСК ЗАПИСЕЙ
    def search_records(self,name):
        name = ('%'+name+'%')
        self.db.cursor.execute(
                '''SELECT * FROM Users WHERE name LIKE ?''',(name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values = row)
         for row in self.db.cursor.fetchall()]

##########################################################################################################
    #Метод вызывающий дочернее окно
    def open_child(self):
        Child()

    #Метод, вызывающий окно изменение данных
    def open_update_dialog(self):
        Update()

    def open_search(self):
        Search()
    

##########################################################################################################
#оздания окна добавления
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # инициалзицая виджетов дочернего окна
    def init_child(self):
        self.title('Добавление контакта')
        self.geometry('400x220')
        self.resizable(False,False)
        #перехват событий происходящих в приложении
        self.grab_set()
        #захватываем фокус
        self.focus()

        #Текст
        label_name = tk.Label(self,text = 'ФИО')
        label_name.place(x = 50, y = 50)
        
        
        label_phone = tk.Label(self,text = 'Номер телефона')
        label_phone.place(x = 50, y = 80)
        
        
        label_email = tk.Label(self,text = 'E-mail')
        label_email.place(x = 50, y = 110)
        
        
        label_salary = tk.Label(self,text = 'Зарплата')
        label_salary.place(x = 50, y = 140)


        # Виджет ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200,y=50)
        
        
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200,y=80)
        
        
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200,y=110)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200,y=140)


        # кнопка закрытия дочернего окна
        btn_cancel = tk.Button(self,text = 'Закрыть', command=self.destroy)
        btn_cancel.place(x = 200, y = 150)
        btn_cancel.pack()

        # кнопка добавления
        self.btn_add = tk.Button(self, text= "Добавить")
        self.btn_add.place(x=265, y=190)
        self.btn_add.bind('<Button-1>', lambda event:
                    self.view.records (self.entry_name.get(),
                                        self.entry_phone.get(),
                                        self.entry_email.get(),
                                        self.entry_salary.get()))


#Класс окна редактирования текущего контакта, наследуемый от калсса  Child
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.db = db
        self.view = app
        self.default_data()
    def init_edit(self):
        self.title("Редактировать позицию")
        self.btn_edit = ttk.Button(self, text= "Редактировать")
        self.btn_add.destroy()
        self.btn_edit.place(x = 265, y = 190)
        self.btn_edit.bind('<Button-1>',lambda event:
                    self.view.update_records (self.entry_name.get(),
                                        self.entry_phone.get(),
                                        self.entry_email.get(),
                                        self.entry_salary.get()))
        self.btn_edit.bind('<Button-1>', lambda event :self.destroy(), add = '+')
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cursor.execute('''SELECT * FROM Users WHERE ID =?''', (id,))
        #получаем достпу к первой записи из выборки
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


##########################################################################################################

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


    def init_child(self):
        self.title("Поиск контакта")
        self.geometry('300x150')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
##########################################################################################################
        label_name = tk.Label(self, text = "ФИО")
        label_name.place(x = 20, y = 40)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x = 70, y = 40)
##########################################################################################################   
        btn_cancel = tk.Button(self,text = 'Закрыть', command=self.destroy)
        btn_cancel.place(x = 200, y = 70)
        btn_cancel.pack()

        self.btn_search = tk.Button(self, text= "Найти")
        self.btn_search.place(x=200, y=100)
        self.btn_search.bind('<Button-1>',lambda event: self.view.search_records(self.entry_name.get()))

###########################################################################################################     
#Класс бд

class DB():
    def __init__(self):
        # создаем соединение с бд
        self.connect = sqlite3.connect('employees.db')
        self.cursor = self.connect.cursor()

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS Users(
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                phone TEXT,
                                email TEXT,
                                salary INTEGER)
                            ''')

        self.connect.commit()

    def insert_data(self,name,phone,email,salary):
        self.cursor.execute('''
                            INSERT INTO Users(name,phone,email,salary) 
                            VALUES (?,?,?,?)
                            ''',(name,phone,email,salary))
        self.connect.commit()


##########################################################################################################

#Запуск программы

if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('645x450')
    root.configure(bg = 'white')
    root.resizable(False,False)
    root.mainloop()
