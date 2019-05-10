from tkinter import *
from tkinter import ttk
import ihome_FP as FP

class ihome_GUI:
    def __init__(self, master):
        master.title('موتور جستجوی هوشمند خانه')
        master.geometry('600x850')
        master.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#e1d8b9')
        self.style.configure('TButton', background='#e1d8b9')
        self.style.configure('TLabel', background='#e1d8b9',font = ('B koodak', 12))
        self.style.configure('Header.TLabel', background='#e1d8b9', font=('B Titr', 14), foreground = 'blue')

        self.panedwin = ttk.Panedwindow(master,orient = VERTICAL)
        self.panedwin.pack(fill = BOTH , expand = True)

        self.search_frame = ttk.Frame(self.panedwin, width = 400 , height = 400, relief = RAISED)
        self.search_frame.pack(side = RIGHT)

        self.logo = PhotoImage(file = 'ihome.gif')
        self.label = ttk.Label(self.search_frame,image = self.logo)
        self.label.pack(pady = 20)
        self.label_home_search = ttk.Label(self.search_frame, text = 'جستجوی خانه در تهران بر اساس منطقه', style = 'Header.TLabel')
        # self.label1.config(font=('B koodak', 14))
        self.label_home_search.pack()
        self.label_zone_name = ttk.Label(self.search_frame, text = 'نام منطقه (مثال: سعادت آباد)')
        self.label_zone_name.pack()
        self.entry_search = ttk.Entry(self.search_frame, width = 30)
        self.entry_search.pack()
        self.label_pages = ttk.Label(self.search_frame, text = 'تعداد صفحات برای جستجو')
        self.label_pages.pack()
        self.entry_pages = ttk.Entry(self.search_frame, width = 30)
        self.entry_pages.pack()
        self.button_search = ttk.Button(self.search_frame, text = 'شروع جستجو', command = lambda: FP.home_search(self.entry_search.get(),int(self.entry_pages.get())))
        self.button_search.pack(pady = 10)
        self.progressbar = ttk.Progressbar(self.search_frame, orient = HORIZONTAL, length = 200)
        self.progressbar.pack(pady = 10)
        self.progressbar.config(mode = 'determinate')
        self.button_search.bind('<1>', lambda e: bar() )

        def bar():
            import time
            self.progressbar['value'] = 20
            self.search_frame.update_idletasks()
            time.sleep(3)
            self.progressbar['value'] = 50
            self.search_frame.update_idletasks()
            time.sleep(3)
            self.progressbar['value'] = 80
            self.search_frame.update_idletasks()
            time.sleep(3)
            self.progressbar['value'] = 100

        self.estimation_frame = ttk.Frame(self.panedwin, width = 400 , height = 400, relief = RAISED)
        self.estimation_frame.pack()

        self.label_smart_estimate = ttk.Label(self.estimation_frame, text = 'محاسبه هوشمند قیمت خانه', style = 'Header.TLabel')
        self.label_smart_estimate.pack(pady = 10)

        self.label_name = ttk.Label(self.estimation_frame, text='نام منطقه در تهران (مثال: پونک)')
        self.label_name.pack()
        self.entry_name = ttk.Entry(self.estimation_frame, width=30)
        self.entry_name.pack()
        self.label_area = ttk.Label(self.estimation_frame, text='مساحت خانه')
        self.label_area.pack()
        self.entry_area = ttk.Entry(self.estimation_frame, width=30)
        self.entry_area.pack()
        self.label_room = ttk.Label(self.estimation_frame, text='تعداد اتاق')
        self.label_room.pack()
        self.entry_room = ttk.Entry(self.estimation_frame, width=30)
        self.entry_room.pack()
        self.button_price = ttk.Button(self.estimation_frame, text = 'تخمین قیمت', command = lambda: FP.Smart_Price_estimation(self.entry_name.get(),self.entry_area.get(),self.entry_room.get()))
        self.button_price.pack(pady = 10)
        self.entry_result = ttk.Entry(self.estimation_frame, text = 'قیمت تخمینی')
        # Es_price = FP.Smart_Price_estimation(self.entry_name.get(), self.entry_area.get(), self.entry_room.get())
        # self.entry_result.insert(0, Es_price)
        self.entry_result.pack(pady = 10)

        self.DB_frame = ttk.Frame(self.panedwin , width = 400 , height = 400, relief = RAISED)
        self.DB_frame.pack()

        self.label_Create_DB = ttk.Label(self.DB_frame, text='ایجاد پایگاه داده', style = 'Header.TLabel')
        self.label_Create_DB.pack(pady = 10)
        self.page_num = ttk.Label(self.DB_frame,text = "تعداد صفحه مورد نظر برای ایجاد پایگاه داده")
        self.page_num.pack()
        self.entry_page_num = ttk.Entry(self.DB_frame, width=30)
        self.entry_page_num.pack()
        self.DB_button = ttk.Button(self.DB_frame, text = 'ایجاد پایگاه داده جدید', command = lambda: FP.CreateDB_ihome(int(self.entry_page_num.get())))
        self.DB_button.pack(pady = 10)
        self.DB_show_button = ttk.Button(self.DB_frame, text='نمایش پایگاه داده', command = lambda: FP.show_DB())
        self.DB_show_button.pack(pady=10)


        self.panedwin.add(self.search_frame)
        self.panedwin.add(self.estimation_frame)
        self.panedwin.add(self.DB_frame)

def main():
    root = Tk()
    ihome = ihome_GUI(root)
    root.mainloop()


if __name__ == "__main__": main()
