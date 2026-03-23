#Libraries
import tkinter as tk 
import os
from tkinter import *
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
import datetime
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

meals_db = sqlite3.connect('Meals.db')
cursor = meals_db.cursor()


class ProductsC:

    def __init__(self, product_id, product_name, product_status, product_price, product_pic, product_recent):
        self.product_id     = product_id       
        self.product_name   = product_name       
        self.product_status = product_status       
        self.product_price  = product_price       
        self.product_pic    = product_pic 
        self.product_recent = product_recent 

    def get_id(self):
        return self.product_id

    def get_name(self):
        return self.product_name

    def get_picture(self):
        return self.product_pic    

    def get_status(self):
        return self.product_status 

    def get_recent(self):
        return int(self.product_recent)

    def become_recent(self):
        self.product_recent = 1
        cursor.execute('UPDATE Products SET ProductUsed = ? WHERE ProductID = ?', (self.product_recent, self.product_id))
        meals_db.commit()

    def update_recent(self, counter):
        self.product_recent = counter
        cursor.execute('UPDATE Products SET ProductUsed = ? WHERE ProductID = ?', (self.product_recent, self.product_id))
        meals_db.commit()

    def change_status(self):
        if self.product_status == 0:
            self.product_status = 1
        else:
            self.product_status = 0

        cursor.execute('UPDATE Products SET ProductStatus = ? WHERE ProductID = ?', (self.product_status, self.product_id))
        meals_db.commit()

    def __str__(self):
        return f"{self.product_id}  {self.product_name}  {self.product_status}   {self.product_price}   {self.product_pic}   {self.product_recent}"

class RecipesC():

    def __init__(self, recipe_id, recipe_pic, recipe_name, recipe_description, recipe_steps, recipe_status, recipe_user, recipe_ingredients):
        self.recipe_id             =  recipe_id       
        self.recipe_pic            =  recipe_pic       
        self.recipe_name           =  recipe_name       
        self.recipe_description    =  recipe_description       
        self.recipe_steps          =  recipe_steps 
        self.recipe_status         =  recipe_status 
        self.recipe_user           =  recipe_user 
        self.recipe_ingredients    =  recipe_ingredients 

    def get_recipe_id(self):
        return self.recipe_id

    def get_picture(self):
        return self.recipe_pic

    def get_name(self):
        return self.recipe_name

    def get_status(self):
        return int(self.recipe_status)

    def get_usermade(self):
        return int(self.recipe_user)

    def get_ingredients(self):
        return self.recipe_ingredients

    def get_description(self):
        return self.recipe_description

    def get_steps(self):
        return self.recipe_steps

    def change_status(self):
        if self.recipe_status == 0:
            self.recipe_status = 1
        else:
            self.recipe_status = 0

        cursor.execute('UPDATE Recipes SET RecipeStatus = ? WHERE RecipeID = ?', (self.recipe_status, self.recipe_id))
        meals_db.commit()

    def delete_recipe(self):
        cursor.execute('DELETE FROM Ingredients WHERE RecipeID = ?', (self.recipe_id,))
        meals_db.commit()

        cursor.execute('DELETE FROM Recipes WHERE RecipeID = ?', (self.recipe_id,))
        meals_db.commit()

    def plan_recipe(self, day_date, day_period):

        cursor.execute('INSERT INTO MealPlan VALUES (?,?,?)', (day_date, day_period, self.recipe_id))
        meals_db.commit()

    def delete_plan_recipe(self):
        cursor.execute('DELETE FROM MealPlan WHERE RecipeID = ?', (self.recipe_id,))
        meals_db.commit()
        


    def __str__(self):
        return (f"\n{self.recipe_id}\n{self.recipe_pic}\n{self.recipe_name}\n{self.recipe_description}\n{self.recipe_steps}\n{self.recipe_status}\n{self.recipe_user}\n{self.recipe_ingredients}\n" )

class EatPlan:
    def __init__(self, date, period, recipe_id):
        self.date           =  date 
        self.period         =  period 
        self.recipe_id      =  recipe_id   

    def get_day(self):
        return self.date

    def get_period(self):
        return self.period

    def get_recipe(self):
        return self.recipe_id


    def __str__(self):
        return (f"\n{self.date}   {self.period}   {self.recipe_id}")

        
class ShopList:
    def __init__(self, name, quantity, unit, approx_price):
        self.name               =  name 
        self.quantity           =  quantity
        self.unit               =  unit 
        self.approx_price       =  approx_price    
    
    def get_name(self):
        return self.name
    
    def get_quantity(self):
        return self.quantity
    
    def get_unit(self):
        return self.unit
    
    def get_approx_price(self):
        return self.approx_price
    
    def delete_item(self):
        cursor.execute('DELETE FROM ShoppingList WHERE ProductName = ?', (self.name,))
        meals_db.commit()

    def __str__(self):
        return (f"\n {self.name}   {self.quantity}   {self.unit}   {self.approx_price}")



#Subroutines
def delete_added_ingredient(event):
    for selected_item in user_ingredient_list.selection():
        user_ingredient_list.delete(selected_item)

def ingredient_chosen(event):

    for selected_item in search_tree_ingr_search.selection():
        item = search_tree_ingr_search.item(selected_item)
        record = item['text']

        ingr_list = []

        for parent in user_ingredient_list.get_children():
            ingr_list.append(user_ingredient_list.item(parent)["text"])

        if record not in ingr_list:          
            user_ingredient_list.insert('', tk.END, text=record, value =  ' X ')    
    
    close_ingredient_chooser()

def callback_text_ingr_search(var, index, mode):

    for item in search_tree_ingr_search.get_children():
        search_tree_ingr_search.delete(item)

    for each in products_cl:
        if str(search_text_ingr_search.get().lower().strip()) in str(each.get_name().lower()):
            search_tree_ingr_search.insert('', tk.END, text=each.get_name())

    search_tree_ingr_search.grid(row=0, column=0, sticky='nsew')

    scrollbar_ingr_search = ttk.Scrollbar(middle_ingr_search, orient=tk.VERTICAL, command=search_tree_ingr_search.yview)
    search_tree_ingr_search.configure(yscroll=scrollbar_ingr_search.set)
    scrollbar_ingr_search.grid(row=0, column=1, sticky='ns')


def search_user_library_recipes(var, index, mode):
    for each in user_recipes_frames_holder:
        each.destroy()

    new_list = []

    for each in recipes_cl:
        if str(search_user_recipes.get().lower().strip()) in str(each.get_name().lower()) or \
            str(search_user_recipes.get().lower().strip()) in str(each.get_description().lower()):
            new_list.append(each)

    upload_user_library(user_recipes_frames_holder, user_counter, new_list)

def search_favourite_recipes(var, index, mode):
    for each in fav_recipes_frames_holder:
        each.destroy()

    fav_data_showen = []

    for each in recipes_cl:
        if str(search_fav_recipes.get().lower().strip()) in str(each.get_name().lower()) or \
            str(search_fav_recipes.get().lower().strip()) in str(each.get_description().lower()):
            fav_data_showen.append(each)

    upload_favourite_menu(fav_recipes_frames_holder,fav_counter12, fav_data_showen)

def search_recipes(var, index, mode):

    for each in recipes_frames_holder:
        each.destroy()

    data_showen = []

    for each in recipes_cl:
        if str(search_text_recipes.get().lower().strip()) in str(each.get_name().lower()) or \
            str(search_text_recipes.get().lower().strip()) in str(each.get_description().lower()):
            data_showen.append(each)

    upload_main_recipe_menu(recipes_frames_holder, counter12, data_showen)

def ingedient_selected(event):
    global record

    product_info_frame.pack(fill='x', expand=True)
    recipe_frame.pack_forget()
    
    for selected_item in ingredient_list.selection():
        item = ingredient_list.item(selected_item)
        record = item['text']
        name_item.config(text=record)

        for each in products_cl:
            if str(record.lower()) == str(each.get_name().lower()):
                if each.get_status()==1:
                    star_button_pr.configure(image=button_photo7)
                    star_button_pr.photo = button_photo7
                else:
                    star_button_pr.configure(image=button_photo10)
                    star_button_pr.photo = button_photo10

                picture_product = PhotoImage(file= each.get_picture()) 
                canvas_c.itemconfig(image_container_pr, image=picture_product)
                canvas_c.image = picture_product

                update_recent(each)


def select_recipe(name_p, status_p, desc_p, pic_p, steps_p, ingr_p):
    global current_recipe

    current_recipe = name_p
    close_shopping_tab()
    close_recipe_tab()

    clean_searchbars()
    
    recipe_frame.pack(fill='x', expand=True)

    name.config(text = name_p)
    description.config(text = desc_p)
    steps.config(text = steps_p)

    for each in recipes_cl:
        if each.get_name() == name_p and each.get_usermade() == 1:
            top_recipe_label.config(width=34)
            delete_recipe.grid(column=1, row=0, padx=5)
            delete_recipe.pack_propagate(False)

    picture = Image.open(pic_p) 
    picture= picture.resize((250,230), Image.Resampling.LANCZOS)

    photo_image = ImageTk.PhotoImage(picture)

    canvas_recipe_info.itemconfig(image_container_recipe, image=photo_image)
    canvas_recipe_info.image = photo_image

    if status_p == 1:
        star_button_recipe.configure(image=button_photo7)
    else:
        star_button_recipe.configure(image=button_photo10)


    for item in ingredient_list.get_children():
        ingredient_list.delete(item)

    for each in ingr_p:
        for item in products_cl:
            if each == item.get_id():
                ingredient_list.insert('', tk.END, text=item.get_name())


    ingredient_list.grid(row=0, column=0, sticky='nsew')

def delete_recipe_sub():
    global recipes_cl
    temp_list = []
    for each in recipes_cl:
        if name["text"] == each.get_name() and \
            description["text"] == each.get_description() and \
            steps["text"] == each.get_steps():
            
            each.delete_recipe()
            del each
        else:
            temp_list.append(each)

    recipes_cl = temp_list

    for each in recipes_frames_holder:
        each.destroy()
    upload_main_recipe_menu(recipes_frames_holder, counter12, recipes_cl)

    for each in fav_recipes_frames_holder:
        each.destroy()
    upload_favourite_menu(fav_recipes_frames_holder,fav_counter12, recipes_cl)

    for each in user_recipes_frames_holder:
        each.destroy()
    upload_user_library(user_recipes_frames_holder, user_counter, recipes_cl)

    for each in recipes_frames_holder_plan:
        each.destroy()
    upload_main_recipe_menu_plan(recipes_frames_holder_plan, counter12_plan, recipes_cl)

    close_recipe_sub()

def upload_user_library(user_recipes_frames_holder, user_counter, passed_list):
    for each in passed_list:
        if each.get_usermade() == 1:
            temporary_user_frame = tk.Frame(main_user_recipes_frame, bg=theme[2],height=150, width=window_width-30, borderwidth=2, relief="groove")
            temporary_user_frame.pack(fill='x', expand=True, padx=1, pady=1)
            temporary_user_frame.pack_propagate(False)

            recipe_user_frame = tk.Frame(temporary_user_frame, bg=theme[5],height=150, width=120, borderwidth=2, relief="groove")
            recipe_user_frame.pack_propagate(False)
            recipe_user_frame.pack(fill='x', expand=True, padx=1, pady=1, side='right')
            
            recipe_picture_frame_user = tk.Frame(temporary_user_frame, bg=theme[1],height=120, width=8, borderwidth=2, relief="groove")
            recipe_picture_frame_user.pack_propagate(False)
            recipe_picture_frame_user.pack(fill='x', expand=True, padx=10, pady=1, side='left')

            extra_name_frame_user = tk.Frame(recipe_user_frame, bg=theme[5],height=40, width=120)
            extra_name_frame_user.pack_propagate(False)
            extra_name_frame_user.pack(fill='x', expand=True, padx=1, pady=1)

            name_recipe_small_user = Label(extra_name_frame_user,
                            bg=theme[5],
                            font=("CourierNew", 12),
                            text='',
                            anchor=W, 
                            wraplength=230)
            name_recipe_small_user.grid(padx=10, pady=5, sticky=W)

            extra_info_frame_user = tk.Frame(recipe_user_frame, bg=theme[5],height=90, width=120)
            extra_info_frame_user.pack_propagate(False)
            extra_info_frame_user.pack(fill='x', expand=True, padx=1, pady=1)

            descr_recipe_small_user = Label(extra_info_frame_user,
                            bg=theme[5],
                            font=("CourierNew", 10),
                            text='',
                            anchor=W,
                            wraplength=230, 
                            justify="left")
            descr_recipe_small_user.grid(padx=10, sticky=W)

            extra_pic_frame_user = tk.Frame(recipe_user_frame, bg=theme[5],height=30, width=120)
            extra_pic_frame_user.pack_propagate(False)
            extra_pic_frame_user.pack(fill='x', expand=True, padx=1, pady=1)

            canvas_user = Canvas(extra_pic_frame_user,height=20, width=20)
            canvas_user.pack(side='right', padx=10, pady=2,)
            
            recipe_user_frame.bind('<Visibility>',
            lambda e, decr_widget = descr_recipe_small_user, name_widget = name_recipe_small_user, canv_widget = canvas_user, number=fav_counter12, name = each.get_name(), status = each.get_status(), desc = each.get_description():
            upload_info(decr_widget, name_widget, canv_widget, number, name, status,desc))

            recipe_picture_frame_user.bind('<Visibility>',
            lambda e, frame_used=recipe_picture_frame_user, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                change_pic(frame_used, name, status, desc, pic, steps, ingr))

            temporary_user_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            recipe_user_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            recipe_picture_frame_user.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            extra_name_frame_user.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            extra_info_frame_user.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            extra_pic_frame_user.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            descr_recipe_small_user.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            name_recipe_small_user.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            canvas_user.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            user_recipes_frames_holder.append(temporary_user_frame)
            user_counter+=1

def upload_favourite_menu(fav_recipes_frames_holder,fav_counter12, fav_data_list):
    for each in fav_data_list:
        if each.get_status() == 1:
            temporary_frame = tk.Frame(main_fav_recipes_frame, bg=theme[2],height=150, width=window_width-30, borderwidth=2, relief="groove")
            temporary_frame.pack(fill='x', expand=True, padx=1, pady=1)
            temporary_frame.pack_propagate(False)

            recipe_info_frame = tk.Frame(temporary_frame, bg=theme[5],height=150, width=120, borderwidth=2, relief="groove")
            recipe_info_frame.pack_propagate(False)
            recipe_info_frame.pack(fill='x', expand=True, padx=1, pady=1, side='right')
            
            recipe_picture_frame = tk.Frame(temporary_frame, bg=theme[1],height=120, width=8, borderwidth=2, relief="groove")
            recipe_picture_frame.pack_propagate(False)
            recipe_picture_frame.pack(fill='x', expand=True, padx=10, pady=1, side='left')

            extra_name_frame = tk.Frame(recipe_info_frame, bg=theme[5],height=40, width=120)
            extra_name_frame.pack_propagate(False)
            extra_name_frame.pack(fill='x', expand=True, padx=1, pady=1)

            name_recipe_small = Label(extra_name_frame,
                            bg=theme[5],
                            font=("CourierNew", 12),
                            text='',
                            anchor=W, 
                            wraplength=230)
            name_recipe_small.grid(padx=10, pady=5, sticky=W)

            extra_info_frame = tk.Frame(recipe_info_frame, bg=theme[5],height=90, width=120)
            extra_info_frame.pack_propagate(False)
            extra_info_frame.pack(fill='x', expand=True, padx=1, pady=1)

            descr_recipe_small = Label(extra_info_frame,
                            bg=theme[5],
                            font=("CourierNew", 10),
                            text='',
                            anchor=W,
                            wraplength=230, 
                            justify="left")
            descr_recipe_small.grid(padx=10, sticky=W)

            extra_pic_frame = tk.Frame(recipe_info_frame, bg=theme[5],height=30, width=120)
            extra_pic_frame.pack_propagate(False)
            extra_pic_frame.pack(fill='x', expand=True, padx=1, pady=1)

            canvas111 = Canvas(extra_pic_frame,height=20, width=20, bg=theme[5])
            canvas111.pack(side='right', padx=10, pady=2,)
            
            recipe_info_frame.bind('<Visibility>',
            lambda e, decr_widget = descr_recipe_small, name_widget = name_recipe_small, canv_widget = canvas111, number=fav_counter12, name = each.get_name(), status = each.get_status(), desc = each.get_description():
            upload_info(decr_widget, name_widget, canv_widget, number, name, status,desc))

            recipe_picture_frame.bind('<Visibility>',
            lambda e, frame_used=recipe_picture_frame, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                change_pic(frame_used, name, status, desc, pic, steps, ingr))

            temporary_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            recipe_info_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            recipe_picture_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            extra_name_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            extra_info_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            extra_pic_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            descr_recipe_small.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            name_recipe_small.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            canvas111.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            select_recipe(name, status, desc, pic, steps, ingr))

            fav_recipes_frames_holder.append(temporary_frame)
            fav_counter12+=1

def upload_main_recipe_menu(recipes_frames_holder, counter12, data_list):
    for each in data_list:
        if each.get_usermade() != 1:
            temporary_frame1 = tk.Frame(main_recipes_frame, bg=theme[2],height=150, width=window_width-30, borderwidth=2, relief="groove")
            temporary_frame1.pack(fill='x', expand=True, padx=1, pady=1)
            temporary_frame1.pack_propagate(False)

            recipe_info_frame = tk.Frame(temporary_frame1, bg=theme[5],height=150, width=120, borderwidth=2, relief="groove")
            recipe_info_frame.pack_propagate(False)
            recipe_info_frame.pack(fill='x', expand=True, padx=1, pady=1, side='right')
            
            recipe_picture_frame = tk.Frame(temporary_frame1, bg=theme[1],height=120, width=8, borderwidth=2, relief="groove")
            recipe_picture_frame.pack_propagate(False)
            recipe_picture_frame.pack(fill='x', expand=True, padx=10, pady=1, side='left')

            extra_name_frame = tk.Frame(recipe_info_frame, bg=theme[5],height=40, width=120)
            extra_name_frame.pack_propagate(False)
            extra_name_frame.pack(fill='x', expand=True, padx=1, pady=1)

            name_recipe_small = Label(extra_name_frame,
                            bg=theme[5],
                            font=("CourierNew", 12),
                            text='',
                            anchor=W, 
                            wraplength=230)
            name_recipe_small.grid(padx=10, pady=5, sticky=W)

            extra_info_frame = tk.Frame(recipe_info_frame, bg=theme[5],height=90, width=120)
            extra_info_frame.pack_propagate(False)
            extra_info_frame.pack(fill='x', expand=True, padx=1, pady=1)

            descr_recipe_small = Label(extra_info_frame,
                            bg=theme[5],
                            font=("CourierNew", 10),
                            text='',
                            anchor=W,
                            wraplength=230, 
                            justify="left")
            descr_recipe_small.grid(padx=10, sticky=W)

            extra_pic_frame = tk.Frame(recipe_info_frame, bg=theme[5],height=30, width=120)
            extra_pic_frame.pack_propagate(False)
            extra_pic_frame.pack(fill='x', expand=True, padx=1, pady=1)

            canvas11 = Canvas(extra_pic_frame,height=20, width=20, bg=theme[5])
            canvas11.pack(side='right', padx=10, pady=2,)
            
            recipe_info_frame.bind('<Visibility>',
            lambda e, decr_widget = descr_recipe_small, name_widget = name_recipe_small, canv_widget = canvas11, number=counter12, name = each.get_name(), status = each.get_status(), desc = each.get_description():
            upload_info(decr_widget, name_widget, canv_widget, number, name, status,desc))

            recipe_picture_frame.bind('<Visibility>',
            lambda e, frame_used=recipe_picture_frame, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
            change_pic(frame_used, name, status, desc, pic, steps, ingr))

            temporary_frame1.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                select_recipe(name, status, desc, pic, steps, ingr))

            recipe_info_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                select_recipe(name, status, desc, pic, steps, ingr))

            recipe_picture_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                select_recipe(name, status, desc, pic, steps, ingr))

            extra_name_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                select_recipe(name, status, desc, pic, steps, ingr))

            extra_info_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                select_recipe(name, status, desc, pic, steps, ingr))

            extra_pic_frame.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                select_recipe(name, status, desc, pic, steps, ingr))

            descr_recipe_small.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                select_recipe(name, status, desc, pic, steps, ingr))

            name_recipe_small.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                select_recipe(name, status, desc, pic, steps, ingr))

            canvas11.bind("<Button-1>",
            lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
                select_recipe(name, status, desc, pic, steps, ingr))

            recipes_frames_holder.append(temporary_frame1)
            counter12+=1



def change_recipe_status():
    global current_recipe

    for each in recipes_cl:
        if current_recipe == each.get_name():

            each.change_status()

            if each.get_status()==1:
                star_button_recipe.configure(image=button_photo7)
                star_button_recipe.photo = button_photo7
            else:
                star_button_recipe.configure(image=button_photo10)
                star_button_recipe.photo = button_photo10

    for each in recipes_frames_holder:
        each.destroy()
    upload_main_recipe_menu(recipes_frames_holder, counter12, recipes_cl)

    for each in fav_recipes_frames_holder:
        each.destroy()
    upload_favourite_menu(fav_recipes_frames_holder,fav_counter12, recipes_cl)

    for each in user_recipes_frames_holder:
        each.destroy()
    upload_user_library(user_recipes_frames_holder, user_counter, recipes_cl)

    for each in recipes_frames_holder_plan:
        each.destroy()
    upload_main_recipe_menu_plan(recipes_frames_holder_plan, counter12_plan, recipes_cl)


def change_pic(frame_used, name, status, desc, pic, steps, ingr):
    canvas_c1 = Canvas(frame_used, height=250, width=250)
    canvas_c1.pack()

    picture_product1 = Image.open(pic)
    picture_product1= picture_product1.resize((150,130), Image.Resampling.LANCZOS)
    picture_product1 = ImageTk.PhotoImage(picture_product1)

    image_references.append(picture_product1)
    canvas_c1.create_image(0, 0, anchor=NW, image=picture_product1)

    canvas_c1.bind("<Button-1>",
     lambda e: 
     select_recipe(name, status, desc, pic, steps, ingr))

def  upload_info(decr_widget, name_widget, canv_widget, number, name, status,desc):

    name_widget.config(text = name)
    decr_widget.config(text = desc)

    if status == 1:
        image_container1 = canv_widget.create_image(2, 2, anchor=NW, image=button_photo13)
    else:
        image_container1 = canv_widget.create_image(2, 2, anchor=NW, image=button_photo14)

def upload_recipes_db(recipes):

    cursor.execute('SELECT * FROM Ingredients')
    lines = cursor.fetchall()

    ingredient=[]
    last_index = 0

    for each in lines:
        if each[0] > last_index:
            last_index = each[0]
    last_index += 1


    ingredient=[]

    for i in range(1, last_index):
        ingr = [] 
        for each in lines:
            if i == each[0]:
                ingr.append(each[1])
        ingredient.append([i, ingr])

    cursor.execute('SELECT * FROM Recipes')
    lines = cursor.fetchall()
    recipes=[]

    for i in range(1, last_index+1):
        for each in lines:
            temp = 0
            if i == each[0]:
                for j in range(0, len(ingredient)):
                    if i in ingredient[j]:
                        temp = ingredient[j][1]
                recipes.append(RecipesC(each[0], each[1], each[2], each[3], each[4], each[5], each[6], temp))

    return recipes

def upload_shoppings_db(list_sh):
    cursor.execute('SELECT * FROM ShoppingList')
    lines = cursor.fetchall()
    for each in lines:
        list_sh.append(ShopList(each[0], each[1], each[2], each[3]))

    return list_sh


def upload_planned_db(planned):
    cursor.execute('SELECT * FROM MealPlan')
    lines = cursor.fetchall()
    for each in lines:
        planned.append(EatPlan(each[0], each[1], each[2]))

    return planned



def upload_products_db(products):
    cursor.execute('SELECT * FROM Products')
    lines = cursor.fetchall()
    products=[]
    for each in lines:
        products.append(ProductsC(each[0], each[1], each[2], each[3], each[4], each[5]))
    return products

def change_status(record):
    global products_cl
    for each in products_cl:
        if str(record.lower()) == str(each.get_name().lower()):
            each.change_status()
            if each.get_status()==1:
                star_button_pr.configure(image=button_photo7)
                star_button_pr.photo = button_photo7
            else:
                star_button_pr.configure(image=button_photo10)
                star_button_pr.photo = button_photo10

    for item in favourite_list.get_children():
        favourite_list.delete(item)

    for each in products_cl:
        if each.get_status() == 1:
            favourite_list.insert('', tk.END, text=each.get_name())

    favourite_list.grid(row=0, column=0, sticky='nsew')

    scrollbar2 = ttk.Scrollbar(middle_favourite, orient=tk.VERTICAL, command=favourite_list.yview)
    favourite_list.configure(yscroll=scrollbar2.set)
    scrollbar2.grid(row=0, column=1, sticky='ns')

def upload_picture():
    global file_name

    file_name = askopenfilename(title="Open the picture", filetypes=(("Files", "*.png"), ("Files", "*.jpeg"), ("All Files", "*")))

    if file_name == '':
        file_name = 'empty_picture.png'
        return 0 

    picture = Image.open(file_name)

    picture= picture.resize((250,250), Image.Resampling.LANCZOS)

    picture = ImageTk.PhotoImage(picture)

    canvas_user_recipe_info.itemconfig(image_container_user_recipe,image=picture)
    canvas_user_recipe_info.image = picture

def ingredient_chooser():

    clean_searchbars()
    close_recipe_tab()

    ingr_search_frame.pack(fill='x', expand=True)


def clean_searchbars():
    price.set('')
    quantity.set('')
    total_price_pr.config(text='0.0')
    search_text.set('')
    search_text_fav.set('')
    search_text_recipes.set('')
    search_user_recipes.set('')
    search_text_ingr_search.set('')
    search_text_recipes_plan.set('')

def close_shopping_tab():
    groceries_frame.pack_forget()
    search_frame.pack_forget()
    favourite_frame.pack_forget()
    product_info_frame.pack_forget()
    recent_frame.pack_forget()

def close_recipe_tab():
    fav_recipes_frame.pack_forget()
    recipes_frame.pack_forget()
    recipe_frame.pack_forget()
    user_recipe_frame.pack_forget()
    ingr_search_frame.pack_forget()
    add_user_recipe_frame.pack_forget()

def close_mealplan():
    global x 

    x = datetime.datetime.now()

    date_of_label = str(x.day)+" "+str(x.strftime("%B"))+" "+str(x.year)
    date_label.config(text = date_of_label)

    meal_plan_frame.pack_forget()
    recipes_frame_plan.pack_forget()

    today = x.strftime("%x")
    update_meal_plan_days(today)





def close_fav_recipes_button_sub():
    global frame_page
    frame_page = 'main recipe'

    clean_searchbars()
    recipes_frame.pack(fill='x', expand=True)
    fav_recipes_frame.pack_forget()

def star_recipes_command():
    global frame_page
    frame_page = 'favourite recipe'

    clean_searchbars()
    recipes_frame.pack_forget()
    fav_recipes_frame.pack(fill='x', expand=True)

def close_button2_sub():
    global frame_page
    product_info_frame.pack_forget()
    clean_searchbars()

    match frame_page:
        case 'search':
           open_search_page()
        case 'favourite':
            open_favourite_list()
        case 'recent':
            open_recent_list()
        case 'main recipe':
            recipe_frame.pack(fill='x', expand=True)
        case 'favourite recipe':
            recipe_frame.pack(fill='x', expand=True)

def close_new_recipe_button():
    global frame_page

    match frame_page:
        case 'main recipe':
            close_user_recipes_button_sub()
        case 'user library':
            add_user_recipe_sub()

    frame_page = 'main recipe'

    clean_searchbars()
    close_recipe_tab()

    picture_recipe_user = PhotoImage(file='empty_picture.png')

    canvas_user_recipe_info.itemconfig(image_container_user_recipe,image=picture_recipe_user)
    canvas_user_recipe_info.image = picture_recipe_user

    for item in user_ingredient_list.get_children():
        user_ingredient_list.delete(item)

    entry_name_user_recipe['state'] = 'normal'
    description_user['state'] = 'normal'
    steps_user['state'] = 'normal'

    entry_name_user_recipe.delete('1.0',"end")
    description_user.delete('1.0',"end")
    steps_user.delete('1.0',"end")

    name_characters_counter.config(text='0/35')
    decr_characters_counter.config(text='0/75')
    steps_characters_counter.config(text='0/250')

    recipes_frame.pack(fill='x', expand=True)

def close_recipe_sub():
    global frame_page
    product_info_frame.pack_forget()
    recipe_frame.pack_forget()

    top_recipe_label.config(width=38)
    delete_recipe.grid_remove()

    match frame_page:
        case 'main recipe':
            open_recipe_list()
        case 'favourite recipe':
            open_fav_recipe_list()

def close_user_recipes_button_sub():
    global frame_page
    frame_page = 'main recipe'

    clean_searchbars()
    close_recipe_tab()

    recipes_frame.pack(fill='x', expand=True)

def close_ingredient_chooser():
    close_recipe_tab()
    clean_searchbars()

    add_user_recipe_frame.pack(fill='x', expand=True)


####################################################

def open_shop_list():
    clean_searchbars()
    close_shopping_tab()
    close_recipe_tab()
    close_mealplan()
    settings_frame.pack_forget()
    groceries_frame.pack(fill='x', expand=True)

def open_recipes():
    global frame_page
    frame_page = 'main recipe'
    clean_searchbars()
    close_shopping_tab()
    close_recipe_tab()
    close_mealplan()
    settings_frame.pack_forget()
    recipes_frame.pack(fill='x', expand=True)

def open_mealplan():
    clean_searchbars()
    close_shopping_tab()
    settings_frame.pack_forget()
    close_recipe_tab()
    meal_plan_frame.pack(fill='x', expand=True)
    

def open_settings():
    clean_searchbars()
    close_shopping_tab()
    close_recipe_tab()
    close_mealplan()
    settings_frame.pack(fill='x', expand=True)

####################################################

def add_user_recipe_sub():
    global frame_page
    close_recipe_tab()
    frame_page = 'user library'

    add_user_recipe_frame.pack(fill='x', expand=True)

def open_user_recipe_library():
    close_recipe_tab()
    user_recipe_frame.pack(fill='x', expand=True)

def open_recipe_list():
    recipe_frame.pack_forget()
    product_info_frame.pack_forget()
    recipes_frame.pack(fill='x', expand=True)

def open_fav_recipe_list():
    recipe_frame.pack_forget()
    product_info_frame.pack_forget()
    fav_recipes_frame.pack(fill='x', expand=True)

def open_favourite_list():
    groceries_frame.pack_forget()
    favourite_frame.pack(fill='x', expand=True)

def open_search_page():
    groceries_frame.pack_forget()
    search_frame.pack(fill='x', expand=True)

def open_recent_list():
    groceries_frame.pack_forget()
    recent_frame.pack(fill='x', expand=True)

def recent_close_button_sub():
    recent_frame.pack_forget()
    groceries_frame.pack(fill='x', expand=True)

def callback_text(var, index, mode):

    for item in search_tree.get_children():
        search_tree.delete(item)

    for each in products_cl:
        if str(search_text.get().lower().strip()) in str(each.get_name().lower()):
            search_tree.insert('', tk.END, text=each.get_name())

    search_tree.grid(row=0, column=0, sticky='nsew')

    scrollbar = ttk.Scrollbar(middle, orient=tk.VERTICAL, command=search_tree.yview)
    search_tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

def close_button_sub():
    clean_searchbars()
    search_frame.pack_forget()
    groceries_frame.pack(fill='x', expand=True)

def item_selected(event):
    global record, frame_page
    frame_page = 'search'
    product_info_frame.pack(fill='x', expand=True)
    search_frame.pack_forget()
    
    for selected_item in search_tree.selection():
        item = search_tree.item(selected_item)
        record = item['text']
        name_item.config(text=record)

        for each in products_cl:
            if str(record.lower()) == str(each.get_name().lower()):
                if each.get_status()==1:
                    star_button_pr.configure(image=button_photo7)
                    star_button_pr.photo = button_photo7
                else:
                    star_button_pr.configure(image=button_photo10)
                    star_button_pr.photo = button_photo10

                picture_product = PhotoImage(file= each.get_picture()) 
                canvas_c.itemconfig(image_container_pr, image=picture_product)
                canvas_c.image = picture_product

                update_recent(each)

        search_text.set('')

def callback_text_fav(var, index, mode):
    for item in favourite_list.get_children():
        favourite_list.delete(item)

    for each in products_cl:
        if str(search_text_fav.get().lower().strip()) in str(each.get_name().lower()) and each.get_status() == 1:
            favourite_list.insert('', tk.END, text=each.get_name())

    favourite_list.grid(row=0, column=0, sticky='nsew')

    scrollbar2 = ttk.Scrollbar(middle_favourite, orient=tk.VERTICAL, command=favourite_list.yview)
    favourite_list.configure(yscroll=scrollbar2.set)
    scrollbar2.grid(row=0, column=1, sticky='ns')

def fav_close_button_sub ():
    search_text_fav.set('')
    groceries_frame.pack(fill='x', expand=True)
    favourite_frame.pack_forget()

def fav_item_selected(event):
    global record, frame_page
    frame_page = 'favourite'
    product_info_frame.pack(fill='x', expand=True)
    favourite_frame.pack_forget()
    
    for selected_item in favourite_list.selection():
        item = favourite_list.item(selected_item)
        record = item['text']
        name_item.config(text=record)

        for each in products_cl:
            if str(record.lower()) == str(each.get_name().lower()):
                if each.get_status()==1:
                    star_button_pr.configure(image=button_photo7)
                    star_button_pr.photo = button_photo7
                else:
                    star_button_pr.configure(image=button_photo10)
                    star_button_pr.photo = button_photo10

                picture_product = PhotoImage(file= each.get_picture()) 
                canvas_c.itemconfig(image_container_pr, image=picture_product)
                canvas_c.image = picture_product

                update_recent(each)

        search_text_fav.set('')

def update_recent(item):

    counter = 0
    for each in products_cl:
        if each.get_recent() > counter:
            counter = each.get_recent()

    flag = counter
    num = 0

    for each in products_cl:
            if each == item and each.get_recent() != 0:
                num = each.get_recent()

    for i in range(flag):
        for each in products_cl:
            if each.get_recent() == counter and counter != 0:
                each.update_recent(counter+1)
                counter-=1

    for each in products_cl:
        if int(each.get_recent()) > num and num != 0:
            each.update_recent(int(each.get_recent())-1)

        if int(each.get_recent()) == 30:
            each.update_recent(0)

    for each in products_cl:
            if each == item:
                each.become_recent()
            

    counter = flag

    for item in recent_list.get_children():
            recent_list.delete(item)

    for i in range(1, counter):
        for each in products_cl:
            if each.get_recent() == i:
                recent_list.insert("", tk.END, text=str(each.get_name()))

    recent_list.grid(row=0, column=0, sticky='nsew')


def recent_item_selected(event):
    global record, frame_page
    frame_page = 'recent'
    product_info_frame.pack(fill='x', expand=True)
    recent_frame.pack_forget()
    
    for selected_item in recent_list.selection():
        item = recent_list.item(selected_item)
        record = item['text']
        name_item.config(text=record)

        for each in products_cl:
            if str(record.lower()) == str(each.get_name().lower()):
                if each.get_status()==1:
                    star_button_pr.configure(image=button_photo7)
                    star_button_pr.photo = button_photo7
                else:
                    star_button_pr.configure(image=button_photo10)
                    star_button_pr.photo = button_photo10

                picture_product = PhotoImage(file= each.get_picture()) 
                canvas_c.itemconfig(image_container_pr, image=picture_product)
                canvas_c.image = picture_product

                update_recent(each)

def name_text_changes(event):

    number1= len(entry_name_user_recipe.get('1.0',"end"))-1
    
    if number1 >= 35:
        entry_name_user_recipe.delete('1.35', 'end')
        number1 = 35
        entry_name_user_recipe['state'] = 'disable'
        entry_name_user_recipe.bind('<BackSpace>',
        lambda e, limit = 35, widget = entry_name_user_recipe, counter = name_characters_counter:
        unable_text(limit, widget, counter))

    name_characters_counter.config(text=f'{number1}/35')

def descr_text_changes(event):
    number2= len(description_user.get('1.0',"end"))-1
    
    if number2 >= 75:
        description_user.delete('1.75', 'end')
        number2 = 75

        description_user['state'] = 'disable'
        description_user.bind('<BackSpace>',
        lambda e, limit = 75, widget = description_user, counter = decr_characters_counter: 
        unable_text(limit, widget, counter))

    decr_characters_counter.config(text=f'{number2}/75')

def steps_text_changes(event):
    number3= len(steps_user.get('1.0',"end"))-1
    
    if number3 >= 250:
        steps_user.delete('1.250', 'end')
        number3 = 250

        steps_user['state'] = 'disable'
        steps_user.bind('<BackSpace>', 
        lambda e, limit = 250, widget = steps_user, counter = steps_characters_counter: 
        unable_text(limit, widget, counter))

    steps_characters_counter.config(text=f'{number3}/250')

def unable_text(limit, widget, counter):
    widget['state'] = 'normal'

    number= len(widget.get('1.0',"end"))-1
    counter.config(text=f'{number}/{limit}')


def save_user_recipe():
    global file_name

    recipe_index = 0

    for each in recipes_cl:
        if each.get_recipe_id() > recipe_index:
            recipe_index = each.get_recipe_id()
    recipe_index += 1

    recipe_name = entry_name_user_recipe.get('1.0',"end").strip()
    recipe_descript = description_user.get('1.0',"end").strip()
    recipe_stepss = steps_user.get('1.0',"end").strip()

    if recipe_name == '' or recipe_descript == '' or recipe_stepss == '':
        messagebox.showerror('Data Error', 'Enter all required fields!')
        return 0

    ing_list = []

    for parent in user_ingredient_list.get_children():
            ing_list.append(user_ingredient_list.item(parent)["text"])

    if ing_list == []:
        messagebox.showerror('Data Error', 'Enter all required fields!')
        return 0

    class_ingr = []

    for each in products_cl:
        for ing in ing_list:
            if each.get_name() == ing:
                class_ingr.append(each)

    ing_list = []

    if file_name == '':
        file_name = 'empty_picture.png'

    cursor.execute('INSERT INTO Recipes(RecipeID, RecipePicture, RecipeName, RecipeDescription, RecipeSteps, RecipeStatus, RecipeUserCreated) VALUES(?,?,?,?,?,?,?)', 
    (recipe_index, file_name, recipe_name, recipe_descript, recipe_stepss, 0, 1))

    meals_db.commit()

    for each in class_ingr:
        cursor.execute('INSERT INTO Ingredients(RecipeID, ProductID) VALUES(?,?)',
        (recipe_index, each.get_id()))
        meals_db.commit()

        ing_list.append(each.get_id())

    recipes_cl.append(RecipesC(recipe_index, file_name, recipe_name, recipe_descript, recipe_stepss, 0, 1, ing_list))

    for each in recipes_frames_holder:
        each.destroy()
    upload_main_recipe_menu(recipes_frames_holder, counter12, recipes_cl)

    for each in fav_recipes_frames_holder:
        each.destroy()
    upload_favourite_menu(fav_recipes_frames_holder,fav_counter12, recipes_cl)

    for each in user_recipes_frames_holder:
        each.destroy()
    upload_user_library(user_recipes_frames_holder, user_counter, recipes_cl)

    for each in recipes_frames_holder_plan:
        each.destroy()
    upload_main_recipe_menu_plan(recipes_frames_holder_plan, counter12_plan, recipes_cl)

    picture_recipe_user = PhotoImage(file='empty_picture.png')

    canvas_user_recipe_info.itemconfig(image_container_user_recipe,image=picture_recipe_user)
    canvas_user_recipe_info.image = picture_recipe_user

    for item in user_ingredient_list.get_children():
        user_ingredient_list.delete(item)

    entry_name_user_recipe['state'] = 'normal'
    description_user['state'] = 'normal'
    steps_user['state'] = 'normal'

    entry_name_user_recipe.delete('1.0',"end")
    description_user.delete('1.0',"end")
    steps_user.delete('1.0',"end")
    
    name_characters_counter.config(text='0/35')
    decr_characters_counter.config(text='0/75')
    steps_characters_counter.config(text='0/250')
    
    file_name = 'empty_picture.png'

    close_new_recipe_button()

def next_day():
    global x, breakfast_recipe_frame, lunch_recipe_frame, dinner_recipe_frame
  
    x = (x + datetime.timedelta(1))

    date_of_label = str(x.day)+" "+str(x.strftime("%B"))+" "+str(x.year)
    date_label.config(text = date_of_label)

    today = x.strftime("%x")
    update_meal_plan_days(today)

    

def previous_day():
    global x, breakfast_recipe_frame, lunch_recipe_frame, dinner_recipe_frame

    x = x - datetime.timedelta(1)

    date_of_label = str(x.day)+" "+str(x.strftime("%B"))+" "+str(x.year)
    date_label.config(text = date_of_label)

    today = x.strftime("%x")
    update_meal_plan_days(today)



def update_meal_plan_days(today):
    flag = False
    br_recipe = 0

    for each in planned_cl:
        if each.get_day() == today and each.get_period() == "brf":
            flag = True
            br_recipe = each.get_recipe()

    if flag == True:
        for each in recipes_cl:
            if each.get_recipe_id() == br_recipe:

                breakfast_recipe_empty_fr.pack_forget()
                breakfast_recipe_fr_r.pack(fill='x', expand=True)


                name_recipe_small_planned.config(text=each.get_name())
                descr_recipe_small_planned.config(text=each.get_description())

                new_pic = PhotoImage(file=each.get_picture())

                canvas_recipe_planned1.itemconfig(image_container_recipe_planned1,image=new_pic)
                canvas_recipe_planned1.image = new_pic
    else:

        breakfast_recipe_fr_r.pack_forget()
        breakfast_recipe_empty_fr.pack(fill='x', expand=True)

    flag = False
    br_recipe = 0

    for each in planned_cl:
        if each.get_day() == today and each.get_period() == "lnc":
            flag = True
            br_recipe = each.get_recipe()

    if flag == True:
        for each in recipes_cl:
            if each.get_recipe_id() == br_recipe:

                lunch_recipe_empty_fr.pack_forget()
                lunch_recipe_frame_r.pack(fill='x', expand=True)


                name_recipe_small_planned2.config(text=each.get_name())
                descr_recipe_small_planned2.config(text=each.get_description())

                new_pic = PhotoImage(file=each.get_picture())

                canvas_recipe_planned2.itemconfig(image_container_recipe_planned2,image=new_pic)
                canvas_recipe_planned2.image = new_pic
    else:

        lunch_recipe_frame_r.pack_forget()
        lunch_recipe_empty_fr.pack(fill='x', expand=True)

    flag = False
    br_recipe = 0

    for each in planned_cl:
        if each.get_day() == today and each.get_period() == "dnr":
            flag = True
            br_recipe = each.get_recipe()

    if flag == True:
        for each in recipes_cl:
            if each.get_recipe_id() == br_recipe:

                dinner_recipe_empty_fr.pack_forget()
                dinner_recipe_frame_rr.pack(fill='x', expand=True)


                name_recipe_small_planned3.config(text=each.get_name())
                descr_recipe_small_planned3.config(text=each.get_description())

                new_pic = PhotoImage(file=each.get_picture())

                canvas_recipe_planned3.itemconfig(image_container_recipe_planned3,image=new_pic)
                canvas_recipe_planned3.image = new_pic
    else:

        dinner_recipe_frame_rr.pack_forget()
        dinner_recipe_empty_fr.pack(fill='x', expand=True)

def close_recipes_plan_menu():
    meal_plan_frame.pack(fill='x', expand=True)
    recipes_frame_plan.pack_forget()

def search_recipes_plan(var, index, mode):

    for each in recipes_frames_holder_plan:
        each.destroy()

    data_showen = []

    for each in recipes_cl:
        if str(search_text_recipes_plan.get().lower().strip()) in str(each.get_name().lower()) or \
            str(search_text_recipes_plan.get().lower().strip()) in str(each.get_description().lower()):
            data_showen.append(each)

    upload_main_recipe_menu_plan(recipes_frames_holder_plan, counter12_plan, data_showen)


def upload_main_recipe_menu_plan(recipes_frames_holder_plan, counter12_plan, data_list):
    for each in data_list:
        temporary_frame_plan = tk.Frame(main_recipes_frame_plan, bg=theme[2],height=150, width=window_width-30, borderwidth=2, relief="groove")
        temporary_frame_plan.pack(fill='x', expand=True, padx=1, pady=1)
        temporary_frame_plan.pack_propagate(False)

        recipe_info_frame_plan = tk.Frame(temporary_frame_plan, bg=theme[5],height=150, width=120, borderwidth=2, relief="groove")
        recipe_info_frame_plan.pack_propagate(False)
        recipe_info_frame_plan.pack(fill='x', expand=True, padx=1, pady=1, side='right')
        
        recipe_picture_frame_plan = tk.Frame(temporary_frame_plan, bg=theme[1],height=120, width=8, borderwidth=2, relief="groove")
        recipe_picture_frame_plan.pack_propagate(False)
        recipe_picture_frame_plan.pack(fill='x', expand=True, padx=10, pady=1, side='left')

        extra_name_frame_plan = tk.Frame(recipe_info_frame_plan, bg=theme[5],height=40, width=120)
        extra_name_frame_plan.pack_propagate(False)
        extra_name_frame_plan.pack(fill='x', expand=True, padx=1, pady=1)

        name_recipe_small_plan = Label(extra_name_frame_plan,
                        bg=theme[5],
                        font=("CourierNew", 12),
                        text='',
                        anchor=W, 
                        wraplength=230)
        name_recipe_small_plan.grid(padx=10, pady=5, sticky=W)

        extra_info_frame_plan = tk.Frame(recipe_info_frame_plan, bg=theme[5],height=90, width=120)
        extra_info_frame_plan.pack_propagate(False)
        extra_info_frame_plan.pack(fill='x', expand=True, padx=1, pady=1)

        descr_recipe_small_plan = Label(extra_info_frame_plan,
                        bg=theme[5],
                        font=("CourierNew", 10),
                        text='',
                        anchor=W,
                        wraplength=230, 
                        justify="left")
        descr_recipe_small_plan.grid(padx=10, sticky=W)

        extra_pic_frame_plan = tk.Frame(recipe_info_frame_plan, bg=theme[5],height=30, width=120)
        extra_pic_frame_plan.pack_propagate(False)
        extra_pic_frame_plan.pack(fill='x', expand=True, padx=1, pady=1)

        canvas11_plan = Canvas(extra_pic_frame_plan,height=20, width=20, bg=theme[5])
        canvas11_plan.pack(side='right', padx=10, pady=2,)
        
        recipe_info_frame_plan.bind('<Visibility>',
        lambda e, decr_widget = descr_recipe_small_plan, name_widget = name_recipe_small_plan, canv_widget = canvas11_plan, number=counter12, name = each.get_name(), status = each.get_status(), desc = each.get_description():
        upload_info(decr_widget, name_widget, canv_widget, number, name, status,desc))

        recipe_picture_frame_plan.bind('<Visibility>',
        lambda e, frame_used=recipe_picture_frame_plan, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps(), ingr = each.get_ingredients():
        change_pic_plan(frame_used, name, status, desc, pic, steps, ingr))

        temporary_frame_plan.bind("<Button-1>",
        lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps():
            select_recipe_plan(name, status, desc, pic, steps))

        recipe_info_frame_plan.bind("<Button-1>",
        lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps():
            select_recipe_plan(name, status, desc, pic, steps))

        recipe_picture_frame_plan.bind("<Button-1>",
        lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps():
            select_recipe_plan(name, status, desc, pic, steps))

        extra_name_frame_plan.bind("<Button-1>",
        lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps():
            select_recipe_plan(name, status, desc, pic, steps))

        extra_info_frame_plan.bind("<Button-1>",
        lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps():
            select_recipe_plan(name, status, desc, pic, steps))

        extra_pic_frame_plan.bind("<Button-1>",
        lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps():
            select_recipe_plan(name, status, desc, pic, steps))

        descr_recipe_small_plan.bind("<Button-1>",
        lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps():
            select_recipe_plan(name, status, desc, pic, steps))

        name_recipe_small_plan.bind("<Button-1>",
        lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps():
            select_recipe_plan(name, status, desc, pic, steps))

        canvas11_plan.bind("<Button-1>",
        lambda e, name = each.get_name(), status = each.get_status(), desc = each.get_description(), pic = each.get_picture(), steps = each.get_steps():
            select_recipe_plan(name, status, desc, pic, steps))

        

        recipes_frames_holder_plan.append(temporary_frame_plan)
        counter12_plan+=1

def change_pic_plan(frame_used, name, status, desc, pic, steps, ingr):
    canvas11_plan = Canvas(frame_used, height=250, width=250)
    canvas11_plan.pack()

    picture_product1_plan = Image.open(pic)
    picture_product1_plan= picture_product1_plan.resize((150,130), Image.Resampling.LANCZOS)
    picture_product1_plan = ImageTk.PhotoImage(picture_product1_plan)

    image_references.append(picture_product1_plan)
    canvas11_plan.create_image(0, 0, anchor=NW, image=picture_product1_plan)

    canvas11_plan.bind("<Button-1>",
        lambda e:
            select_recipe_plan(name, status, desc, pic, steps))

def plan_recipe(periood):
    global time_period
    time_period = periood

    meal_plan_frame.pack_forget()
    recipes_frame_plan.pack(fill='x', expand=True)


def select_recipe_plan(name_p, status_p, desc_p, pic_p, steps_p):
    global x, time_period

    today = x.strftime("%x")
    print(today)
    clean_searchbars()
    meal_plan_frame.pack(fill='x', expand=True)
    recipes_frame_plan.pack_forget()

    for each_recipe in recipes_cl:
        if each_recipe.get_name() == name_p and \
            each_recipe.get_status() == status_p and \
            each_recipe.get_description() == desc_p and \
            each_recipe.get_picture() == pic_p and \
            each_recipe.get_steps() == steps_p:

            flag = False
            object_delete = None

            for each in planned_cl:
                if each.get_day() == today and each.get_period() == str(time_period):
                    flag = True

                if each.get_recipe() == each_recipe.get_recipe_id():
                    object_delete = each
                    
            if flag == True:
                each_recipe.delete_plan_recipe()
                planned_cl.remove(object_delete)

                

            each_recipe.plan_recipe(str(today), str(time_period))
            planned_cl.append(EatPlan(today, time_period, each_recipe.get_recipe_id()))

            update_meal_plan_days(today)


def change_application_theme(colour_chosen):
    global theme

    match colour_chosen:
        case 'yellow':
            theme = ["#000000","#92977E","#E6E18F","#FEFCAD","#EADDA6","#FFFAE2"]
        case 'blue':
            theme = ["#000000","#9CB5D6","#A0BBDC","#D1DDEC","#DEE7F2","#E8EEF6"]
        case 'green':
            theme = ["#000000","#6C876E","#91A38E","#828D8B","#B1BB80","#E1E9DB"]
        case 'red':
            theme = ["#000000","#8F7E7E","#B96E70","#D2BEBE","#E2CDCE","#E9E0DF"]
        case 'grey':
            theme = ["#000000","#A0A0A6","#B5B5BA","#D5D5D8","#DFDFE2","#EFEFF0"]

    widgets_colours(theme)
    with open("colour.txt", "w") as f:
        f.write('\n'.join(theme))

def widgets_colours(theme):

    main_frames.config(bg=theme[3])
    button_panel.config(bg=theme[2])
    list_button.config(activebackground=theme[5], activeforeground=theme[1], bg=theme[3], fg=theme[0])
    recipe_button.config(activebackground=theme[5], activeforeground=theme[1], bg=theme[3], fg=theme[0])
    plan_button.config(activebackground=theme[5], activeforeground=theme[1], bg=theme[3], fg=theme[0])
    setting_button.config(activebackground=theme[5], activeforeground=theme[1], bg=theme[3], fg=theme[0])

    #SHOPPING LIST PAGE 
    groceries_frame.config(bg=theme[3])
    top_panel.config(bg=theme[5])
    middle_panel.config(bg=theme[5])
    total_panel.config(bg=theme[5])
    total_label1.config(bg=theme[5])
    total_price.config(bg=theme[5])
    space1.config(bg=theme[5])
    space2.config(bg=theme[5])
    space3.config(bg=theme[5])
    space4.config(bg=theme[5])
    space5.config(bg=theme[5])
    bin_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    recent_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    add_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[4], fg=theme[0])
    star_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])

    #SEARCH ITEM PAGE 
    search_frame.config(bg=theme[3])
    top.config(bg=theme[5])
    middle.config(bg=theme[5])
    close_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    canvas_search1.config(bg=theme[5])

    #PRODUCT INFORMATION PAGE
    product_info_frame.config(bg=theme[3])
    top_frame.config(bg=theme[5])
    middle_frame.config(bg=theme[5])
    top_label.config(bg=theme[5])
    close_button2.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    name_item.config(bg=theme[5])
    info_frame.config(bg=theme[5])
    quantity_label.config(bg=theme[5])
    price_label.config(bg=theme[5])
    symbol_label1.config(bg=theme[5])
    total_label.config(bg=theme[5])
    symbol_label2.config(bg=theme[5])
    total_price_pr.config(bg=theme[5])
    button_frame.config(bg=theme[5])
    select_button.config(activebackground=theme[5],activeforeground=theme[3],bg=theme[3],fg=theme[0])
    star_button_pr.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])

    # FAVOURITE LIST OF PRODUCTS
    favourite_frame.config(bg=theme[3])
    top_favourite.config(bg=theme[5])
    middle_favourite.config(bg=theme[5])
    canvas2.config(bg=theme[5])
    fav_close_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])

    # RECENT LIST OF PRODUCTS
    recent_frame.config(bg=theme[3])
    top_recent.config(bg=theme[5])
    middle_recent.config(bg=theme[5])
    top_panel_label.config(bg=theme[5])
    recent_close_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])

    #RECIPES PAGE
    recipes_frame.config(bg=theme[3])
    top_recipes.config(bg=theme[5])
    canvas_search.config(bg=theme[5])
    star_recipes_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    library_recipes_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    add_recipes_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    middle_recipes.config(bg=theme[5])
    canvas_recipe.config(bg=theme[1])
    main_recipes_frame.config(bg=theme[1])
    for each in recipes_frames_holder:
        each.destroy()
    upload_main_recipe_menu(recipes_frames_holder, counter12, recipes_cl)

    # FAVOURITE RECIPES PAGE
    fav_recipes_frame.config(bg=theme[3])
    top_fav_recipes.config(bg=theme[5])
    canvas_fa.config(bg=theme[5])
    close_fav_recipes_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    middle_fav_recipes.config(bg=theme[5])
    canvas_fav_recipe.config(bg=theme[1])
    main_fav_recipes_frame.config(bg=theme[1])
    for each in fav_recipes_frames_holder:
        each.destroy()
    upload_favourite_menu(fav_recipes_frames_holder,fav_counter12, recipes_cl)

    #RECIPE INFORMATION PAGE
    recipe_frame.config(bg=theme[3])
    top_recipe.config(bg=theme[5])
    middle_recipe.config(bg=theme[5])
    star_button_recipe.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    delete_recipe.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    top_recipe_label.config(bg=theme[5])
    close_button_recipe.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    left_frame.config(bg=theme[2])
    ingredients_frame.config(bg=theme[4]) 
    ingr_label.config(bg=theme[4]) 
    ingred_inside_frame.config(bg=theme[5]) 
    right_frame.config(bg=theme[2]) 
    right_info_frame.config(bg=theme[4]) 
    name_recipe_frame.config(bg=theme[4]) 
    name.config(bg=theme[4]) 
    desc_label.config(bg=theme[4]) 
    description_frame.config(bg=theme[5]) 
    description.config(bg=theme[5]) 
    steps_label.config(bg=theme[4]) 
    steps_frame.config(bg=theme[5]) 
    steps.config(bg=theme[5]) 

    # USER LIBRARY RECIPES 
    user_recipe_frame.config(bg=theme[3])
    top_user_recipe.config(bg=theme[5]) 
    canvas_user.config(bg=theme[5]) 
    add_recipes_user_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    close_user_recipes_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    middle_user_recipe.config(bg=theme[5]) 
    canvas_user_recipe.config(bg=theme[1]) 
    main_user_recipes_frame.config(bg=theme[1]) 
    for each in user_recipes_frames_holder:
        each.destroy()
    upload_user_library(user_recipes_frames_holder, user_counter, recipes_cl)

    # ADD RECIPE TO USER LIBRARY
    add_user_recipe_frame.config(bg=theme[3])
    top_add_user_recipe.config(bg=theme[5])
    save_user_recipe_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[1], fg=theme[5])
    top_add_label.config(bg=theme[5])
    add_user_close_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    middle_add_user_recipe.config(bg=theme[5])
    left_user_frame.config(bg=theme[2])
    ingredients_user_frame.config(bg=theme[4])
    user_ingr_label.config(bg=theme[4])
    user_ingred_inside_frame.config(bg=theme[5])
    add_ingredient.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    right_user_frame.config(bg=theme[2])
    right_user_info_frame.config(bg=theme[4])
    name_user.config(bg=theme[4])    
    name_characters_counter.config(bg=theme[4])
    desc_user_label.config(bg=theme[4])
    decr_characters_counter.config(bg=theme[4])
    steps_user_label.config(bg=theme[4])
    steps_characters_counter.config(bg=theme[4])

    #INGREDIENT CHOOSER PAGE 
    ingr_search_frame.config(bg=theme[3])
    top_ingr_search.config(bg=theme[5])
    middle_ingr_search.config(bg=theme[5])
    canvas_ingr_search.config(bg=theme[5])
    close_button_ingr_search.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])

    # MEAL PLAN
    meal_plan_frame.config(bg=theme[3])
    top_meal_plan.config(bg=theme[5])
    left_arrow_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    date_label.config(bg=theme[5])
    right_arrow_button.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    middle_meal_plan.config(bg=theme[2])
    breakfast_frame.config(bg=theme[5])
    breakfast_label.config(bg=theme[5])
    breakfast_recipe_frame.config(bg=theme[3])
    breakfast_recipe_fr_r.config(bg=theme[3])
    recipe_planned_frame1.config(bg=theme[5])
    recipe_picture_frame_planned1.config(bg=theme[1])
    extra_name_frame_planned.config(bg=theme[5])
    name_recipe_small_planned.config(bg=theme[5])
    extra_info_frame_planned.config(bg=theme[5])
    descr_recipe_small_planned.config(bg=theme[5])
    breakfast_recipe_empty_fr.config(bg=theme[3])
    canvas_recipe_planned11.config(bg=theme[5])
    lunch_frame.config(bg=theme[5])
    lunch_label.config(bg=theme[5])
    lunch_recipe_frame.config(bg=theme[3])
    lunch_recipe_frame_r.config(bg=theme[3])
    recipe_planned_frame2.config(bg=theme[5])
    recipe_picture_frame_planned2.config(bg=theme[1])
    extra_name_frame_planned2.config(bg=theme[5])
    name_recipe_small_planned2.config(bg=theme[5])
    extra_info_frame_planned2.config(bg=theme[5])
    descr_recipe_small_planned2.config(bg=theme[5])
    lunch_recipe_empty_fr.config(bg=theme[3])
    canvas_recipe_planned22.config(bg=theme[5])
    dinner_frame.config(bg=theme[5])
    dinner_label.config(bg=theme[5])
    dinner_recipe_frame.config(bg=theme[3])
    dinner_recipe_frame_rr.config(bg=theme[3])
    recipe_planned_frame3.config(bg=theme[5])
    recipe_picture_frame_planned3.config(bg=theme[1])
    extra_name_frame_planned3.config(bg=theme[5])
    name_recipe_small_planned3.config(bg=theme[5])
    extra_info_frame_planned3.config(bg=theme[5])
    descr_recipe_small_planned3.config(bg=theme[5])
    dinner_recipe_empty_fr.config(bg=theme[3])
    canvas_recipe_planned33.config(bg=theme[5])

    #MENU OF RECIPES - MEAL PLAN
    recipes_frame_plan.config(bg=theme[3])
    top_recipes_plan.config(bg=theme[5])
    canvas_search_plan.config(bg=theme[5])
    close_plan_meal.config(activebackground=theme[4], activeforeground=theme[1], bg=theme[5], fg=theme[0])
    middle_recipes_plan.config(bg=theme[5])
    canvas_recipe_plan.config(bg=theme[1])
    main_recipes_frame_plan.config(bg=theme[1])
    for each in recipes_frames_holder_plan:
        each.destroy()
    upload_main_recipe_menu_plan(recipes_frames_holder_plan, counter12_plan, recipes_cl)

    # SETTINGS PAGE 
    settings_frame.config(bg=theme[3])
    top_settings.config(bg=theme[5])
    settings_label.config(bg=theme[5])
    middle_settings.config(bg=theme[2])
    colour_changing.config(bg=theme[5])
    colour_change_label.config(bg=theme[5])
    theme1_button.config(activebackground=theme[1], activeforeground=theme[1], bg=theme[2], fg=theme[0])
    theme2_button.config(activebackground=theme[1], activeforeground=theme[1], bg=theme[2], fg=theme[0])
    theme3_button.config(activebackground=theme[1], activeforeground=theme[1], bg=theme[2], fg=theme[0])
    theme4_button.config(activebackground=theme[1], activeforeground=theme[1], bg=theme[2], fg=theme[0])
    theme5_button.config(activebackground=theme[1], activeforeground=theme[1], bg=theme[2], fg=theme[0])
    file_download.config(bg=theme[5])
    file_download_label.config(bg=theme[5])
    download_button.config(activebackground=theme[1], activeforeground=theme[1], bg=theme[2], fg=theme[0])

def multiple_total_p(event):
    number2= len(price.get())-1
    if price.get()[number2].lower() >= 'a':
        price_entry.delete(f'{number2}', 'end')
    else:
        count_total()

def multiple_total_q(event):
    number1= len(quantity.get())-1
    if quantity.get()[number1].lower() >= 'a':
        quantity_entry.delete(f'{number1}', 'end')
    else:
        count_total()

def count_total():
    total = 0
    qu = 0
    pr = 0

    if quantity.get() != '':
        qu = float(quantity.get())

    if price.get() != '':
        pr = float(price.get())

    if quantity_var.get() == "g":
        total = (qu / 1000 * pr)
        total = round(total, 2)
    else:
        total = (qu * pr)
        total = round(total, 2)

    total_price_pr.config(text=total)

def clear_shopping_list():
    global last_product
    last_product = 1
    for each in shopping_cl:
        cursor.execute('DELETE FROM ShoppingList WHERE ProductName = ?', (each.get_name(),))
        meals_db.commit()

    for item in tree.get_children():
        tree.delete(item)

    total_price.config(text='£0.0')

def item_shooping_delete(event):
    name_chosen = ''
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        name_chosen = item['values']
        name_chosen = name_chosen[1]

    for item in tree.get_children():
        tree.delete(item)

    for each in shopping_cl:
        if each.get_name() == name_chosen:
            each.delete_item()
            shopping_cl.remove(each)

    last_product = 1

    for each in shopping_cl:
        tree.insert('', tk.END, values=(last_product, each.get_name(), each.get_quantity(), each.get_unit(), each.get_approx_price()))
        last_product+=1

    total_items = 0.0
    for each in shopping_cl:
        total_items += float(each.get_approx_price())
    total_price.config(text=f'£{round(total_items, 2)}')


def add_list_item(record):
    global last_product
    tree.insert('', tk.END, values=(last_product, record, quantity.get(),quantity_var.get(), total_price_pr['text']))
    cursor.execute('INSERT INTO ShoppingList VALUES (?,?,?,?)', (record, quantity.get(),quantity_var.get(), total_price_pr['text']))
    meals_db.commit()
    shopping_cl.append(ShopList(record, quantity.get(),quantity_var.get(), total_price_pr['text']))
    total_pricee = float(total_price['text'][1::])
    total_pricee += float(total_price_pr['text'])
    total_price.config(text=f'£{round(total_pricee, 2)}')
    last_product += 1
    open_shop_list()



def save_to_txt_file():
    value = ''
    with open("shopping_list.txt", "w") as shoppings:
        for items in tree.get_children():
            value = tree.item(items)['values']
            shoppings.write(str(value[0]))
            shoppings.write(" ")
            shoppings.write(str(value[1]))
            shoppings.write(" ")
            shoppings.write(str(value[2]))
            shoppings.write(" ")
            shoppings.write(str(value[3]))
            shoppings.write(" ")
            shoppings.write(str(value[4]))
            shoppings.write("\n")

    os.startfile("shopping_list.txt")
            


#Main program

last_product = 1

frame_page = ''
products_cl = []
products_cl = upload_products_db(products_cl)

recipes_cl = []
recipes_cl = upload_recipes_db(recipes_cl)

planned_cl = []
planned_cl = upload_planned_db(planned_cl)

shopping_cl = []
shopping_cl = upload_shoppings_db(shopping_cl)



with open("colour.txt", "r") as f:
    lines = f.readlines()
theme = []
for line in lines:
    theme.append(line.strip())


window = tk.Tk()   #creation of window
window.title("MealMate") #name of program
window.iconbitmap('app_icon.ico') #icon of app

window_width = 460
window_height = 700
##finding the center of computer screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
center_x = int(screen_width /2 - window_width /2)
center_y = int(screen_height /2 - window_height /2)
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}') #establishing size and center position to window

window.resizable(False, False) #prevent all changes of window size

main_frame_height = 640 #variable responsible for the size of the main window without the switching panel
panel_height = 60 #variable responsible for the size of the switching panel

main_frames = tk.Frame(window, bg=theme[3],height=main_frame_height) #creating a frame where all frames will be showen
main_frames.pack(fill='x', expand=True) #establishing width the same as window width and given height 
main_frames.pack_propagate(False) #frame should have a fixed size that I specified

button_panel = tk.Frame(window, bg=theme[2],height=panel_height)#creating a frame of the switching panel
button_panel.pack(fill='x', expand=True)
button_panel.pack_propagate(False)
button_panel.grid_columnconfigure(0, weight=3) #created a grid to distribute four buttons sequentially in a frame

button_photo1 = PhotoImage(file = "listing.png") 
button_photo2 = PhotoImage(file = "cooking.png")
button_photo3 = PhotoImage(file = "calendar.png") 
button_photo4 = PhotoImage(file = "settings.png") 
button_photo5 = PhotoImage(file = "bin.png")
button_photo6 = PhotoImage(file = "history.png")
button_photo7 = PhotoImage(file = "star.png")
button_photo8 = PhotoImage(file = "cancel.png")
button_photo9 = PhotoImage(file = "search.png")
button_photo10 = PhotoImage(file = "empty_star.png")
button_photo11 = PhotoImage(file = "book.png")
button_photo12 = PhotoImage(file = "plus.png")
button_photo13 = PhotoImage(file = "smaller_star.png")
button_photo14 = PhotoImage(file = "smaller_empty_star.png")
button_photo15 = PhotoImage(file = "download.png")
button_photo16 = PhotoImage(file = "right.png")
button_photo17 = PhotoImage(file = "left.png")

#create first button with specified pic and name responsible for shopping list frames
list_button = Button(button_panel,
                          text="List",
                          command=open_shop_list,
                          font=("CourierNew", 10),
                          activebackground=theme[5],
                          activeforeground=theme[1],
                          bg=theme[3],
                          fg=theme[0],
                          image = button_photo1, 
                          compound = TOP,
                          height=panel_height,
                          width = window_width/4-5)
list_button.grid(column=0, row=0)
list_button.pack_propagate(False) #button should have a fixed size that I specified

#create recipe button responsible for recipes frames
recipe_button = Button(button_panel,
                          text="Recipes",
                          command=open_recipes,
                          font=("CourierNew", 10),
                          activebackground=theme[5],
                          activeforeground=theme[1],
                          bg=theme[3],
                          fg=theme[0],
                          image = button_photo2, 
                          compound = TOP,
                          height=panel_height,
                          width = window_width/4-5)
recipe_button.grid(column=1, row=0)
recipe_button.pack_propagate(False) #button should have a fixed size that I specified

#create plan button responsible for meal plan frames
plan_button = Button(button_panel,
                          text="Meal Plan",
                          command=open_mealplan,
                          font=("CourierNew", 10),
                          activebackground=theme[5],
                          activeforeground=theme[1],
                          bg=theme[3],
                          fg=theme[0],
                          image = button_photo3, 
                          compound = TOP,
                          height=panel_height,
                          width = window_width/4-5)

plan_button.grid(column=2, row=0)
plan_button.pack_propagate(False) #button should have a fixed size that I specified

#create settings button responsible for setting frame
setting_button = Button(button_panel,
                          text="Settings",
                          command=open_settings,
                          font=("CourierNew", 10),
                          activebackground=theme[5],
                          activeforeground=theme[1],
                          bg=theme[3],
                          fg=theme[0],
                          image = button_photo4, 
                          compound = TOP,
                          height=panel_height,
                          width = window_width/4-15)
setting_button.grid(column=3, row=0)
setting_button.pack_propagate(False) #button should have a fixed size that I specified

#SHOPPING LIST PAGE 

groceries_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height) #creating a frame where all groceries from shopping list are shown
groceries_frame.pack(fill='x', expand=True) #establishing width the same as window width and given height 
groceries_frame.pack_propagate(False) #frame should have a fixed size that I specified


top_panel = tk.Frame(groceries_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")#top panel with add buttons and etc. 
top_panel.pack(fill='x', expand=True)
top_panel.grid_columnconfigure(0, weight=8) #created a grid to distribute some buttons sequentially in a frame
top_panel.pack_propagate(False) #frame should have a fixed size that I specified

middle_panel = tk.Frame(groceries_frame, bg=theme[5],height=main_frame_height-panel_height-10, borderwidth=2, relief="groove")#initial frame with shopping list
middle_panel.pack(fill='x', expand=True)
middle_panel.pack_propagate(False)

total_panel = tk.Frame(groceries_frame, bg=theme[5],height=50, borderwidth=2, relief="groove")
total_panel.pack(fill='x', expand=True)
total_panel.pack_propagate(False)
total_panel.grid_columnconfigure(0, weight=1) #created a grid to distribute some buttons sequentially in a frame

total_label1 = Label(total_panel,
                      font=("CourierNew", 12),
                      bg = theme[5],
                      text="Total price:")
total_label1.grid(sticky=tk.W, column=0, row=0, pady= 10, padx= 5)

total_items = 0.0
for each in shopping_cl:
    total_items += float(each.get_approx_price())

total_price = Label(total_panel,
                      font=("CourierNew", 12),
                      bg = theme[5],
                      text=f'£{total_items}')
total_price.grid(sticky=tk.E,column=1, row=0, pady= 10, padx= 5)

space1 = tk.Frame(top_panel, bg=theme[5],height=panel_height, width=10) 
space1.grid(column=0, row=0) 

#every button is created at the same way as others but with different parameters 
#creating button that will delete every item in the shopping list 

bin_button = Button(top_panel,
                          command=clear_shopping_list,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo5, 
                          height=30,
                          width = 30,
                          borderwidth=0)
bin_button.grid(column=1, row=0)
bin_button.pack_propagate(False) #button should have a fixed size that I specified

space2= tk.Frame(top_panel, bg=theme[5],height=panel_height, width=20) 
space2.grid(column=2, row=0) 

#creating button that activates page with recent groceries 
recent_button = Button(top_panel,
                          command=open_recent_list,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo6, 
                          height=30,
                          width = 30,
                          borderwidth=0)
recent_button.grid(column=3, row=0)
recent_button.pack_propagate(False) #button should have a fixed size that I specified

space3 = tk.Frame(top_panel, bg=theme[5],height=panel_height, width=45) 
space3.grid(column=4, row=0)

#creating button that show add-page with other groceries 
add_button = Button(top_panel,
                          text="ADD",
                          command=open_search_page,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[4],
                          fg=theme[0],
                          height=1,
                          width = 20)
add_button.grid(column=5, row=0)
add_button.pack_propagate(False) #button should have a fixed size that I specified

space4 = tk.Frame(top_panel, bg=theme[5],height=panel_height, width=80) 
space4.grid(column=6, row=0) 

#creating button that activates page with favourite groceries 
star_button = Button(top_panel,
                          command=open_favourite_list,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo7, 
                          height=30,
                          width = 30,
                          borderwidth=0)
star_button.grid(column=7, row=0)
star_button.pack_propagate(False)

space5 = tk.Frame(top_panel, bg=theme[5],height=panel_height, width=20)
space5.grid(column=8, row=0)

columns = ('n','product_name', 'quantity', 'units','approx_price' )

tree = ttk.Treeview(middle_panel, height = 25, columns=columns, show='headings')

tree.heading('n', text='N')
tree.heading('product_name', text='Product Name')
tree.heading('quantity', text='Quantity')
tree.heading('units', text='Units')
tree.heading('approx_price', text='Approx. Price')

tree.column('n', width=50, anchor=tk.CENTER)
tree.column('product_name', width=125, anchor=tk.CENTER)
tree.column('quantity', width=80, anchor=tk.CENTER)
tree.column('units', width=80, anchor=tk.CENTER)
tree.column('approx_price', width=100, anchor=tk.CENTER)


tree.grid(row=0, column=0, sticky='nsew')

for each in shopping_cl:
    tree.insert('', tk.END, values=(last_product, each.get_name(), each.get_quantity(), each.get_unit(), each.get_approx_price()))
    last_product+=1

tree.bind('<<TreeviewSelect>>', item_shooping_delete)

scrollbar = ttk.Scrollbar(middle_panel, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

#SEARCH ITEM PAGE 

search_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height) 
search_frame.pack(fill='x', expand=True) 
search_frame.pack_propagate(False) #frame should have a fixed size that I specified
search_frame.pack_forget()

top = tk.Frame(search_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")#top panel with add buttons and etc. 
top.pack(fill='x', expand=True)
top.grid_columnconfigure(0, weight=2) #created a grid to distribute some buttons sequentially in a frame
top.pack_propagate(False) #frame should have a fixed size that I specified

middle = tk.Frame(search_frame, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle.pack(fill='x', expand=True)
middle.pack_propagate(False)

canvas_search1 = Canvas(top, height=40, width=40, bg=theme[5], borderwidth=0)
canvas_search1.grid(column=0, row=0, padx=5)
image_container1 = canvas_search1.create_image(5, 5, anchor=NW, image=button_photo9)

search_text = StringVar()          
search_text.trace_add('write', callback_text)
entry_search = Entry(top, width=49,  font=("CourierNew", 10), textvariable = search_text)
entry_search.grid(column=1, row=0, sticky=tk.EW, padx=5)

close_button = Button(top,
                          command=close_button_sub,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo8, 
                          compound = LEFT,
                          borderwidth=0,
                          width = 40,
                          height= panel_height)
close_button.grid(column=2, row=0, sticky=tk.W, padx=5)
close_button.pack_propagate(False) 

search_tree = ttk.Treeview(middle, height = 28, column='prod')
search_tree['show'] = 'tree'
search_tree.column('prod', width=235, anchor=tk.CENTER)

for each in products_cl:
    search_tree.insert('', 'end', text=str(each.get_name()))

search_tree.grid(row=0, column=0, sticky='nsew')

scrollbar = ttk.Scrollbar(middle, orient=tk.VERTICAL, command=search_tree.yview)
search_tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

record = ''
search_tree.bind('<<TreeviewSelect>>', item_selected)

#PRODUCT INFORMATION PAGE

product_info_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height)
product_info_frame.pack(fill='x', expand=True)
product_info_frame.pack_propagate(False)
product_info_frame.pack_forget()

top_frame = tk.Frame(product_info_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_frame.pack(fill='x', expand=True)
top_frame.grid_columnconfigure(0, weight=2) 
top_frame.pack_propagate(False) 

middle_frame = tk.Frame(product_info_frame, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_frame.pack(fill='x', expand=True)
middle_frame.pack_propagate(False)

top_label = Label(top_frame,
                      font=("CourierNew", 12),
                      bg=theme[5],
                      text="Selected Item")
top_label.grid(column=0, row=0, sticky=tk.NS)

close_button2 = Button(top_frame,
                          command=close_button2_sub,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo8, 
                          compound = LEFT,
                          borderwidth=0,
                          width = 40,
                          height= panel_height)
close_button2.grid(column=2, row=0, sticky=tk.W, padx=5)
close_button2.pack_propagate(False) 

pic_pr = tk.Frame(middle_frame,height=250, width=250, relief="groove", borderwidth=1)
pic_pr.pack(padx=10, pady=20, side='top')
pic_pr.pack_propagate(False)

canvas_c = Canvas(pic_pr, height=250, width=250)
canvas_c.pack()

picture_product = PhotoImage(file='apples.png')
image_container_pr = canvas_c.create_image(0, 0, anchor=NW, image=picture_product)

name_item = Label(middle_frame,
                bg=theme[5],
                font=("CourierNew", 15),
                text='00')
name_item.pack()

info_frame = tk.Frame(middle_frame, bg=theme[5],height=180)
info_frame.pack(fill='x', expand=True, padx=50)
info_frame.pack_propagate(False)


quantity_label = Label(info_frame,
                bg=theme[5],
                font=("CourierNew", 12),
                text='Quantity:',
                justify='left')
quantity_label.grid(row = 0, column = 0, padx=5, pady=5, sticky=tk.W)

quantity = StringVar()          
quantity_entry = Entry(info_frame, width=8,  font=("CourierNew", 12), textvariable = quantity)
quantity_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

quantity_var = StringVar() 
list_q = ('kg', 'g', 'p')
quantity_list = OptionMenu(info_frame, quantity_var, *list_q, command=lambda option:count_total()) 
quantity_list.config(width=3)
quantity_list.grid(row = 0, column = 2, padx=5, pady=5, sticky=tk.E)
quantity_var.set('kg')

price_label = Label(info_frame,
                bg=theme[5],
                font=("CourierNew", 12),
                text='Approximate price:',
                justify='left')
price_label.grid(row = 1, column = 0, padx=5, pady=5, sticky=tk.W)

symbol_label1 = Label(info_frame,
                bg=theme[5],
                font=("CourierNew", 12),
                text='£')
symbol_label1.grid(row = 1, column = 1, padx=0, pady=5, sticky=tk.E)

price = StringVar()          
price_entry = Entry(info_frame, width=8,  font=("CourierNew", 12), textvariable = price)
price_entry.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)

quantity_entry.bind('<KeyRelease>', multiple_total_q)
price_entry.bind('<KeyRelease>', multiple_total_p)
quantity_entry.bind('<BackSpace>',multiple_total_q)
price_entry.bind('<BackSpace>',multiple_total_p)

total_label = Label(info_frame,
                bg=theme[5],
                font=("CourierNew", 12),
                text='Total price:',
                justify='left')
total_label.grid(row = 2, column = 0, padx=5, pady=5, sticky=tk.W)

symbol_label2 = Label(info_frame,
                bg=theme[5],
                font=("CourierNew", 12),
                text='£')
symbol_label2.grid(row = 2, column = 1, padx=0, pady=5, sticky=tk.E)

total_price_pr = Label(info_frame,
                bg=theme[5],
                font=("CourierNew", 12),
                text='0.0')
total_price_pr.grid(row = 2, column = 2, padx=0, pady=5, sticky=tk.E)

button_frame = tk.Frame(middle_frame, bg=theme[5],height=80)
button_frame.pack(pady=20)
button_frame.pack_propagate(False)

select_button = Button(     button_frame,
                            command=lambda:add_list_item(record),
                            font=("CourierNew", 20),
                            activebackground=theme[5],
                            activeforeground=theme[3],
                            bg=theme[3],
                            fg=theme[0],
                            text = 'ADD', 
                            relief="groove",
                            width= 10)
select_button.grid(column=0, row=0, sticky=tk.N, padx=30)

star_button_pr = Button(button_frame,
                          command=lambda:change_status(record),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo10, 
                          height=30,
                          width = 30,
                          borderwidth=0)
star_button_pr.grid(column=1, row=0, padx=0, pady=10, sticky=tk.N)
star_button_pr.pack_propagate(False)

# FAVOURITE LIST OF PRODUCTS

favourite_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height) 
favourite_frame.pack(fill='x', expand=True) 
favourite_frame.pack_propagate(False)
favourite_frame.pack_forget()

top_favourite = tk.Frame(favourite_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_favourite.pack(fill='x', expand=True)
top_favourite.grid_columnconfigure(0, weight=2) 
top_favourite.pack_propagate(False) 

middle_favourite = tk.Frame(favourite_frame, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_favourite.pack(fill='x', expand=True)
middle_favourite.pack_propagate(False)

canvas2 = Canvas(top_favourite,height=40, width=40, bg=theme[5])
canvas2.grid(column=0, row=0, sticky=tk.W, padx=5)
image_container2 = canvas2.create_image(5, 5, anchor=NW, image=button_photo9)

search_text_fav = StringVar()          
search_text_fav.trace_add('write', callback_text_fav)
Entry(top_favourite, width=49,  font=("CourierNew", 10), textvariable = search_text_fav).grid(column=1, row=0, sticky=tk.EW, padx=5)

fav_close_button = Button(top_favourite,
                          command=fav_close_button_sub,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo8, 
                          compound = LEFT,
                          borderwidth=0,
                          width = 40,
                          height= panel_height)
fav_close_button.grid(column=2, row=0, sticky=tk.W, padx=5)
fav_close_button.pack_propagate(False) 

favourite_list = ttk.Treeview(middle_favourite, height = 28, column='prod')
favourite_list['show'] = 'tree'
favourite_list.column('prod', width=235, anchor=tk.CENTER)

for each in products_cl:
    if each.get_status() == 1:
        favourite_list.insert('', 'end', text=str(each.get_name()))

favourite_list.grid(row=0, column=0, sticky='nsew')

scrollbar2 = ttk.Scrollbar(middle_favourite, orient=tk.VERTICAL, command=favourite_list.yview)
favourite_list.configure(yscroll=scrollbar2.set)
scrollbar2.grid(row=0, column=1, sticky='ns')

record = ''
favourite_list.bind('<<TreeviewSelect>>', fav_item_selected)

# RECENT LIST OF PRODUCTS

recent_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height) 
recent_frame.pack(fill='x', expand=True) 
recent_frame.pack_propagate(False)
recent_frame.pack_forget()

top_recent = tk.Frame(recent_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_recent.pack(fill='x', expand=True)
top_recent.grid_columnconfigure(0, weight=2) 
top_recent.pack_propagate(False) 

middle_recent = tk.Frame(recent_frame, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_recent.pack(fill='x', expand=True)
middle_recent.pack_propagate(False)

top_panel_label = Label(top_recent,
                      font=("CourierNew", 12),
                      bg=theme[5],
                      text="Recently Used")
top_panel_label.grid(column=0, row=0, sticky=tk.NS)

recent_close_button = Button(top_recent,
                          command=recent_close_button_sub,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo8, 
                          compound = LEFT,
                          borderwidth=0,
                          width = 40,
                          height= panel_height)
recent_close_button.grid(column=0, row=0, sticky=tk.E, padx=5)
recent_close_button.pack_propagate(False) 

recent_list = ttk.Treeview(middle_recent, height = 28, column='prod')
recent_list['show'] = 'tree'
recent_list.column('prod', width=255, anchor=tk.CENTER)

counter = 0
for each in products_cl:
    if each.get_recent() > counter:
        counter = each.get_recent()

for i in range(1, counter):
    for each in products_cl:
        if each.get_recent() == i:
            recent_list.insert("", tk.END, text=str(each.get_name()))

recent_list.grid(row=0, column=0, sticky='nsew')

recent_list.bind('<<TreeviewSelect>>', recent_item_selected)

#RECIPES PAGE

recipes_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height)
recipes_frame.pack(fill='x', expand=True)
recipes_frame.pack_propagate(False) 
recipes_frame.pack_forget()

top_recipes = tk.Frame(recipes_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_recipes.pack(fill='x', expand=True)
top_recipes.grid_columnconfigure(0, weight=8) 
top_recipes.pack_propagate(False)

canvas_search = Canvas(top_recipes, bg=theme[5], height=40, width=40)
canvas_search.grid(column=0, row=0, sticky=tk.W, padx=5, pady=10)
image_container_fav = canvas_search.create_image(5, 5, anchor=NW, image=button_photo9)

search_text_recipes = StringVar()          
search_text_recipes.trace_add('write', search_recipes)
entry_search_recipes = Entry(top_recipes, width=35,  font=("CourierNew", 10), textvariable = search_text_recipes)
entry_search_recipes.grid(column=1, row=0, sticky=tk.W, padx=5)

star_recipes_button = Button(top_recipes,
                          command=star_recipes_command,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo7, 
                          height=30,
                          width = 30,
                          borderwidth=0)
star_recipes_button.grid(column=2, row=0, padx=10)
star_recipes_button.pack_propagate(False)

library_recipes_button = Button(top_recipes,
                          command=open_user_recipe_library,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo11, 
                          height=30,
                          width = 30,
                          borderwidth=0)
library_recipes_button.grid(column=3, row=0, padx=5)
library_recipes_button.pack_propagate(False)

add_recipes_button = Button(top_recipes,
                          command=add_user_recipe_sub,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo12, 
                          height=30,
                          width = 30,
                          borderwidth=0)
add_recipes_button.grid(column=5, row=0, padx=10)
add_recipes_button.pack_propagate(False)

middle_recipes = tk.Frame(recipes_frame, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_recipes.pack(fill='x', expand=True)
middle_recipes.pack_propagate(False)

canvas_recipe = Canvas(middle_recipes, bg=theme[1])
scrollbar_recipe = ttk.Scrollbar(middle_recipes, orient="vertical", command=canvas_recipe.yview)
main_recipes_frame = tk.Frame(canvas_recipe, bg=theme[1])
main_recipes_frame.pack(fill='x', expand=True)

main_recipes_frame.bind("<Configure>", lambda e: canvas_recipe.configure(scrollregion=canvas_recipe.bbox("all")))

canvas_recipe.create_window((0, 0), window=main_recipes_frame, anchor="nw")
canvas_recipe.configure(yscrollcommand=scrollbar_recipe.set)

canvas_recipe.pack(side="left", fill="both", expand=True)
scrollbar_recipe.pack(side="right", fill="y")

image_references = []
recipes_frames_holder = []
counter12 = 0

upload_main_recipe_menu(recipes_frames_holder, counter12, recipes_cl)


# FAVOURITE RECIPES PAGE

fav_recipes_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height)
fav_recipes_frame.pack(fill='x', expand=True)
fav_recipes_frame.pack_propagate(False) 
fav_recipes_frame.pack_forget()

top_fav_recipes = tk.Frame(fav_recipes_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_fav_recipes.pack(fill='x', expand=True)
top_fav_recipes.grid_columnconfigure(0, weight=3) 
top_fav_recipes.pack_propagate(False)

canvas_fa = Canvas(top_fav_recipes,height=40, width=40, bg=theme[5])
canvas_fa.grid(column=0, row=0, sticky=tk.W, padx=5, pady=10)
image_container_fav = canvas_fa.create_image(5, 5, anchor=NW, image=button_photo9)

search_fav_recipes = StringVar()          
search_fav_recipes.trace_add('write', search_favourite_recipes)

entry_fav_recipes = Entry(top_fav_recipes, width=49,  font=("CourierNew", 10), textvariable = search_fav_recipes)
entry_fav_recipes.grid(column=1, row=0, sticky=tk.W, padx=5)

close_fav_recipes_button = Button(top_fav_recipes,
                          command=close_fav_recipes_button_sub,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo8, 
                          compound = LEFT,
                          borderwidth=0,
                          width = 40,
                          height= 40)
close_fav_recipes_button.grid(column=2, row=0, sticky=tk.W, padx=5)
close_fav_recipes_button.pack_propagate(False) 

middle_fav_recipes = tk.Frame(fav_recipes_frame, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_fav_recipes.pack(fill='x', expand=True)
middle_fav_recipes.pack_propagate(False)

canvas_fav_recipe = Canvas(middle_fav_recipes, bg=theme[1])
scrollbar_recipe = ttk.Scrollbar(middle_fav_recipes, orient="vertical", command=canvas_fav_recipe.yview)
main_fav_recipes_frame = tk.Frame(canvas_fav_recipe, bg=theme[1])
main_fav_recipes_frame.pack(fill='x', expand=True)

main_fav_recipes_frame.bind("<Configure>", lambda e: canvas_fav_recipe.configure(scrollregion=canvas_fav_recipe.bbox("all")))

canvas_fav_recipe.create_window((0, 0), window=main_fav_recipes_frame, anchor="nw")
canvas_fav_recipe.configure(yscrollcommand=scrollbar_recipe.set)

canvas_fav_recipe.pack(side="left", fill="both", expand=True)
scrollbar_recipe.pack(side="right", fill="y")

fav_recipes_frames_holder = []
fav_counter12 = 0

upload_favourite_menu(fav_recipes_frames_holder,fav_counter12, recipes_cl)


#RECIPE INFORMATION PAGE

current_recipe = ''

recipe_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height)
recipe_frame.pack(fill='x', expand=True)
recipe_frame.pack_propagate(False) 
recipe_frame.pack_forget()

top_recipe = tk.Frame(recipe_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_recipe.pack(fill='x', expand=True)
top_recipe.grid_columnconfigure(0, weight=8) 
top_recipe.pack_propagate(False)

middle_recipe = tk.Frame(recipe_frame, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_recipe.pack(fill='x', expand=True)
middle_recipe.pack_propagate(False)

star_button_recipe = Button(top_recipe,
                          command=change_recipe_status,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo10, 
                          height=30,
                          width = 30,
                          borderwidth=0)
star_button_recipe.grid(column=0, row=0, padx=0, pady=10, sticky=tk.NS)
star_button_recipe.pack_propagate(False)

delete_recipe = Button(top_recipe,
                                command=delete_recipe_sub,
                                activebackground=theme[4],
                                activeforeground=theme[1],
                                bg=theme[5],
                                fg=theme[0],
                                image = button_photo5, 
                                height=30,
                                width = 30,
                                borderwidth=0)

top_recipe_label = Label(top_recipe,
                      font=("CourierNew", 12),
                      bg=theme[5],
                      compound = CENTER,
                      width=38,
                      height=3,
                      text="Chosen dish")
top_recipe_label.grid(column=2, row=0, sticky=tk.NS)

close_button_recipe = Button(top_recipe,
                          command=close_recipe_sub,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo8, 
                          compound = LEFT,
                          borderwidth=0,
                          width = 40,
                          height= 30)
close_button_recipe.grid(column=3, row=0, sticky=tk.NS, padx=5)
close_button_recipe.pack_propagate(False) 

left_frame = tk.Frame(middle_recipe, bg=theme[2],height=main_frame_height-panel_height, width= 240)
left_frame.pack(side=LEFT)
left_frame.pack_propagate(False)

canvas_recipe_info = Canvas(left_frame, height=220, width=220)
canvas_recipe_info.pack(padx=5, pady=5)

picture_recipe = PhotoImage(file='apples.png')
image_container_recipe = canvas_recipe_info.create_image(0, 0, anchor=NW, image=picture_recipe)

ingredients_frame = tk.Frame(left_frame, bg=theme[4],height=340, borderwidth=2, width= 225, relief="groove")
ingredients_frame.pack(padx=5, pady=5)
ingredients_frame.pack_propagate(False)

ingr_label = Label(ingredients_frame,
                      font=("CourierNew", 12),
                      bg=theme[4],
                      compound = CENTER,
                      width=38,
                      height=2,
                      text="Ingredients:")
ingr_label.pack()

ingred_inside_frame = tk.Frame(ingredients_frame, bg=theme[5],height=300, borderwidth=2, width= 210, relief="groove")
ingred_inside_frame.pack(pady=5)
ingred_inside_frame.pack_propagate(False)

ingredient_list = ttk.Treeview(ingred_inside_frame, height = 14, column='prod', show = 'tree')
ingredient_list.column('prod', width=1)
ingredient_list.pack()

record = ''
ingredient_list.bind('<<TreeviewSelect>>', ingedient_selected)

right_frame = tk.Frame(middle_recipe, bg=theme[2],height=main_frame_height-panel_height, width= 220)
right_frame.pack(side=RIGHT)
right_frame.pack_propagate(False)

right_info_frame = tk.Frame(right_frame, bg=theme[4],height=main_frame_height-panel_height, width= 220, borderwidth=2, relief="groove")
right_info_frame.pack(padx=5, pady=5)
right_info_frame.pack_propagate(False)

name_recipe_frame = tk.Frame(right_info_frame, bg=theme[4],height=70, width= 210)
name_recipe_frame.pack(padx=5, pady=5)
name_recipe_frame.pack_propagate(False)

name = Label(name_recipe_frame,
                      font=("CourierNew", 14),
                      bg=theme[4],
                      compound = LEFT,
                      width=38,
                      anchor=W, 
                      justify=LEFT,
                      wraplength=170,
                      text="")
name.pack(padx=5, pady=5)

desc_label = Label(right_info_frame,
                      font=("CourierNew", 11),
                      bg=theme[4],
                      compound = LEFT,
                      width=38,
                      anchor=W, 
                      justify=LEFT,
                      text="Description:")
desc_label.pack(padx=5)
 
description_frame = tk.Frame(right_info_frame, bg=theme[5],height=150, borderwidth=2, width= 210, relief="groove")
description_frame.pack(padx=5, pady=5)
description_frame.pack_propagate(False)

description = Label(description_frame,
                      font=("CourierNew", 10),
                      bg=theme[5],
                      compound = LEFT,
                      width=38,
                      anchor=W, 
                      justify=LEFT,
                      wraplength=170,
                      text="")
description.pack(padx=5, pady=5)

steps_label = Label(right_info_frame,
                      font=("CourierNew", 11),
                      bg=theme[4],
                      compound = LEFT,
                      width=38,
                      anchor=W, 
                      justify=LEFT,
                      text="Steps:")
steps_label.pack(padx=5)

steps_frame = tk.Frame(right_info_frame, bg=theme[5],height=400, borderwidth=2, width= 210, relief="groove")
steps_frame.pack(padx=5, pady=5)
steps_frame.pack_propagate(False)

steps = Label(steps_frame,
                      font=("CourierNew", 10),
                      bg=theme[5],
                      compound = LEFT,
                      wraplength=170,
                      width=38,
                      anchor=W, 
                      justify=LEFT,
                      text="")
steps.pack(padx=5, pady=5)

# USER LIBRARY RECIPES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

user_recipe_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height)
user_recipe_frame.pack(fill='x', expand=True)
user_recipe_frame.pack_propagate(False) 
user_recipe_frame.pack_forget()

top_user_recipe = tk.Frame(user_recipe_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_user_recipe.pack(fill='x', expand=True)
top_user_recipe.grid_columnconfigure(0, weight=8) 
top_user_recipe.pack_propagate(False)

canvas_user = Canvas(top_user_recipe,height=40, width=40, bg=theme[5])
canvas_user.grid(column=0, row=0, sticky=tk.W, padx=5, pady=10)
image_container_user = canvas_user.create_image(5, 5, anchor=NW, image=button_photo9)

search_user_recipes = StringVar()          
search_user_recipes.trace_add('write', search_user_library_recipes)

entry_user_recipes = Entry(top_user_recipe, width=43,  font=("CourierNew", 10), textvariable = search_user_recipes)
entry_user_recipes.grid(column=1, row=0, sticky=tk.W, padx=10)

add_recipes_user_button = Button(top_user_recipe,
                          command=add_user_recipe_sub,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo12, 
                          height=30,
                          width = 30,
                          borderwidth=0)
add_recipes_user_button.grid(column=2, row=0, sticky=tk.W)
add_recipes_user_button.pack_propagate(False)

close_user_recipes_button = Button(top_user_recipe,
                          command=close_user_recipes_button_sub,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo8, 
                          compound = LEFT,
                          borderwidth=0,
                          width = 40,
                          height= 40)
close_user_recipes_button.grid(column=3, row=0, sticky=tk.W, padx=5)
close_user_recipes_button.pack_propagate(False) 

middle_user_recipe = tk.Frame(user_recipe_frame, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_user_recipe.pack(fill='x', expand=True)
middle_user_recipe.pack_propagate(False)

canvas_user_recipe = Canvas(middle_user_recipe, bg=theme[1])
scrollbar_user = ttk.Scrollbar(middle_user_recipe, orient="vertical", command=canvas_user_recipe.yview)

main_user_recipes_frame = tk.Frame(canvas_user_recipe, bg=theme[1])
main_user_recipes_frame.pack(fill='x', expand=True)

main_user_recipes_frame.bind("<Configure>", lambda e: canvas_user_recipe.configure(scrollregion=canvas_user_recipe.bbox("all")))

canvas_user_recipe.create_window((0, 0), window=main_user_recipes_frame, anchor="nw")
canvas_user_recipe.configure(yscrollcommand=scrollbar_user.set)

canvas_user_recipe.pack(side="left", fill="both", expand=True)
scrollbar_user.pack(side="right", fill="y")

user_recipes_frames_holder = []
user_counter = 0

upload_user_library(user_recipes_frames_holder, user_counter, recipes_cl)

# ADD RECIPE TO USER LIBRARY~~~~~~~~~~~~~~~~~~~~~~~~~~~

add_user_recipe_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height)
add_user_recipe_frame.pack(fill='x', expand=True)
add_user_recipe_frame.pack_propagate(False) 
add_user_recipe_frame.pack_forget()

top_add_user_recipe = tk.Frame(add_user_recipe_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_add_user_recipe.pack(fill='x', expand=True)
top_add_user_recipe.grid_columnconfigure(0, weight=8) 
top_add_user_recipe.pack_propagate(False)

save_user_recipe_button = Button(top_add_user_recipe,
                          command=save_user_recipe,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[1],
                          fg=theme[5],
                          text = 'SAVE',
                          compound = RIGHT,
                          borderwidth=1,
                          width = 10,
                          height= 2)
save_user_recipe_button.grid(column=0, row=0, sticky=tk.W, padx=5)
save_user_recipe_button.pack_propagate(False) 

top_add_label = Label(top_add_user_recipe,
                      font=("CourierNew", 12),
                      bg=theme[5],
                      text="Add New Recipe")
top_add_label.grid(column=1, row=0, sticky=tk.NS, pady=5, padx=100)

add_user_close_button = Button(top_add_user_recipe,
                          command=close_new_recipe_button,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo8, 
                          compound = LEFT,
                          borderwidth=0,
                          width = 40,
                          height= panel_height)
add_user_close_button.grid(column=2, row=0, sticky=tk.E, padx=5)
add_user_close_button.pack_propagate(False) 

middle_add_user_recipe = tk.Frame(add_user_recipe_frame, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_add_user_recipe.pack(fill='x', expand=True)
middle_add_user_recipe.pack_propagate(False)

left_user_frame = tk.Frame(middle_add_user_recipe, bg=theme[2],height=main_frame_height-panel_height, width= 240)
left_user_frame.pack(side=LEFT)
left_user_frame.pack_propagate(False)

canvas_user_recipe_info = Canvas(left_user_frame, height=220, width=220)
canvas_user_recipe_info.pack(padx=5, pady=5)

picture_recipe_user = PhotoImage(file='empty_picture.png')
image_container_user_recipe = canvas_user_recipe_info.create_image(0, 0, anchor=NW, image=picture_recipe_user)

file_name = 'empty_picture.png'

canvas_user_recipe_info.bind("<Button-1>",
            lambda e: upload_picture())

ingredients_user_frame = tk.Frame(left_user_frame, bg=theme[4],height=340, borderwidth=2, width= 225, relief="groove")
ingredients_user_frame.pack(padx=5, pady=5)
ingredients_user_frame.pack_propagate(False)

user_ingr_label = Label(ingredients_user_frame,
                      font=("CourierNew", 12),
                      bg=theme[4],
                      compound = CENTER,
                      width=38,
                      height=2,
                      text="Ingredients:")
user_ingr_label.pack()

user_ingred_inside_frame = tk.Frame(ingredients_user_frame, bg=theme[5],height=220, borderwidth=2, width= 210, relief="groove")
user_ingred_inside_frame.pack(pady=5)
user_ingred_inside_frame.pack_propagate(False)

user_ingredient_list = ttk.Treeview(user_ingred_inside_frame, height = 12, column=('prod','tickbox'), show = 'tree')
user_ingredient_list.column('prod', width=1)
user_ingredient_list.column('tickbox', width=1)
user_ingredient_list.pack()

record = ''
user_ingredient_list.bind('<<TreeviewSelect>>', delete_added_ingredient)

add_ingredient = Button(ingredients_user_frame,
                          command=ingredient_chooser,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          text = 'ADD', 
                          compound = LEFT,
                          borderwidth=1,
                          width = 25,
                          height= 2)
add_ingredient.pack()
add_ingredient.pack_propagate(False) 

right_user_frame = tk.Frame(middle_add_user_recipe, bg=theme[2],height=main_frame_height-panel_height, width= 220)
right_user_frame.pack(side=RIGHT)
right_user_frame.pack_propagate(False)

right_user_info_frame = tk.Frame(right_user_frame, bg=theme[4],height=main_frame_height-panel_height, width= 220, borderwidth=2, relief="groove")
right_user_info_frame.pack(padx=5, pady=5)
right_user_info_frame.pack_propagate(False)

name_user = Label(right_user_info_frame,
                      font=("CourierNew", 11),
                      bg=theme[4],
                      compound = LEFT,
                      width=38,
                      anchor=W, 
                      justify=LEFT,
                      wraplength=170,
                      text="Enter recipe name:")
name_user.pack(padx=5, pady=5)        

entry_name_user_recipe = Text(right_user_info_frame, height=2, width=26,  font=("CourierNew", 10))
entry_name_user_recipe.pack(padx=5, pady=5)

entry_name_user_recipe.bind('<KeyRelease>', name_text_changes)

name_characters_counter = Label(right_user_info_frame,
                      font=("CourierNew", 10),
                      bg=theme[4],
                      compound = LEFT,
                      width=30,
                      anchor=W, 
                      justify=LEFT,
                      height=1,
                      text="0/35")
name_characters_counter.pack(padx=5, pady=5)

desc_user_label = Label(right_user_info_frame,
                      font=("CourierNew", 11),
                      bg=theme[4],
                      compound = LEFT,
                      width=38,
                      anchor=W, 
                      justify=LEFT,
                      text="Description:")
desc_user_label.pack(padx=5)
 
description_user = Text(right_user_info_frame, height=5, width=26,  font=("CourierNew", 10))
description_user.pack(padx=5, pady=5)

description_user.bind('<KeyRelease>', descr_text_changes)

decr_characters_counter = Label(right_user_info_frame,
                      font=("CourierNew", 10),
                      bg=theme[4],
                      compound = LEFT,
                      width=30,
                      anchor=W, 
                      justify=LEFT,
                      height=1,
                      text="0/75")
decr_characters_counter.pack(padx=5, pady=5)

steps_user_label = Label(right_user_info_frame,
                      font=("CourierNew", 11),
                      bg=theme[4],
                      compound = LEFT,
                      width=38,
                      anchor=W, 
                      justify=LEFT,
                      text="Steps:")
steps_user_label.pack(padx=5)

steps_user = Text(right_user_info_frame, height=14, width=26,  font=("CourierNew", 10))
steps_user.pack(padx=5, pady=5)

steps_user.bind('<KeyRelease>', steps_text_changes)

steps_characters_counter = Label(right_user_info_frame,
                      font=("CourierNew", 10),
                      bg=theme[4],
                      compound = LEFT,
                      width=30,
                      anchor=W, 
                      justify=LEFT,
                      height=1,
                      text="0/250")
steps_characters_counter.pack(padx=5, pady=5)

#INGREDIENT CHOOSER PAGE 

ingr_search_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height) 
ingr_search_frame.pack(fill='x', expand=True) 
ingr_search_frame.pack_propagate(False) 
ingr_search_frame.pack_forget()

top_ingr_search = tk.Frame(ingr_search_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_ingr_search.pack(fill='x', expand=True)
top_ingr_search.grid_columnconfigure(0, weight=2) 
top_ingr_search.pack_propagate(False)

middle_ingr_search = tk.Frame(ingr_search_frame, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_ingr_search.pack(fill='x', expand=True)
middle_ingr_search.pack_propagate(False)

canvas_ingr_search = Canvas(top_ingr_search,height=40, width=40, bg=theme[5])
canvas_ingr_search.grid(column=0, row=0, sticky=tk.W, padx=5)
image_container_ingr_search = canvas_ingr_search.create_image(5, 5, anchor=NW, image=button_photo9)

search_text_ingr_search = StringVar()          
search_text_ingr_search.trace_add('write', callback_text_ingr_search)

entry_search_ingr_search = Entry(top_ingr_search, width=49,  font=("CourierNew", 10), textvariable = search_text_ingr_search)
entry_search_ingr_search.grid(column=1, row=0, sticky=tk.EW, padx=5)

close_button_ingr_search = Button(top_ingr_search,
                          command=close_ingredient_chooser,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo8, 
                          compound = LEFT,
                          borderwidth=0,
                          width = 40,
                          height= panel_height)
close_button_ingr_search.grid(column=2, row=0, sticky=tk.W, padx=5)
close_button_ingr_search.pack_propagate(False) 

search_tree_ingr_search = ttk.Treeview(middle_ingr_search, height = 28, column=('prod', 'tick'))
search_tree_ingr_search['show'] = 'tree'
search_tree_ingr_search.column('prod', width=200, anchor=tk.CENTER)
search_tree_ingr_search.column('tick', width=35, anchor=tk.CENTER)


for each in products_cl:
    search_tree_ingr_search.insert('', 'end', text=str(each.get_name()))

search_tree_ingr_search.grid(row=0, column=0, sticky='nsew')

scrollbar_ingr_search = ttk.Scrollbar(middle_ingr_search, orient=tk.VERTICAL, command=search_tree_ingr_search.yview)
search_tree_ingr_search.configure(yscroll=scrollbar_ingr_search.set)
scrollbar_ingr_search.grid(row=0, column=1, sticky='ns')

record = ''
search_tree_ingr_search.bind('<<TreeviewSelect>>', ingredient_chosen)

# MEAL PLAN

meal_plan_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height)
meal_plan_frame.pack(fill='x', expand=True)
meal_plan_frame.pack_propagate(False) 
meal_plan_frame.pack_forget()

top_meal_plan = tk.Frame(meal_plan_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_meal_plan.pack(fill='x', expand=True)
top_meal_plan.grid_columnconfigure(0, weight=8) 
top_meal_plan.pack_propagate(False)

left_arrow_button = Button(top_meal_plan,
                          command= previous_day,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo17, 
                          height=30,
                          width = 30,
                          borderwidth=0)
left_arrow_button.grid(column=0, row=0, padx=10, pady=10)
left_arrow_button.pack_propagate(False)

x = datetime.datetime.now()
empty_recipe_planned = PhotoImage(file='add-image.png')

date_of_label = str(x.day)+" "+str(x.strftime("%B"))+" "+str(x.year)

date_label = Label(top_meal_plan,
                      font=("CourierNew", 13),
                      bg=theme[5],
                      width=38,
                      text=date_of_label
                      )
date_label.grid(column=1, row=0, padx=5, pady=15)

right_arrow_button = Button(top_meal_plan,
                          command= next_day,
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo16, 
                          height=30,
                          width = 30,
                          borderwidth=0)
right_arrow_button.grid(column=2, row=0, padx=7, pady=10)
right_arrow_button.pack_propagate(False)

middle_meal_plan = tk.Frame(meal_plan_frame, bg=theme[2],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_meal_plan.pack(fill='x', expand=True)
middle_meal_plan.pack_propagate(False)

breakfast_frame = tk.Frame(middle_meal_plan, bg=theme[5],height=170, borderwidth=2, relief="groove")
breakfast_frame.pack(fill='x', expand=True, padx = 10, pady=10)
breakfast_frame.pack_propagate(False)

breakfast_label = Label(breakfast_frame,
                      font=("CourierNew", 12),
                      bg=theme[5],
                      width=38,
                      text="Breakfast")
breakfast_label.pack(padx=5, pady=10)

today = x.strftime("%x")
time_period = ''

breakfast_recipe_frame = tk.Frame(breakfast_frame, bg=theme[3],height=150, borderwidth=2, relief="groove")
breakfast_recipe_frame.pack(fill='x', expand=True, padx = 10, pady=5)
breakfast_recipe_frame.pack_propagate(False)

breakfast_recipe_fr_r = tk.Frame(breakfast_recipe_frame, bg=theme[3],height=150, borderwidth=2, relief="groove")
breakfast_recipe_fr_r.pack(fill='x', expand=True)
breakfast_recipe_fr_r.pack_propagate(False)

recipe_planned_frame1 = tk.Frame(breakfast_recipe_fr_r, bg=theme[5],height=150, width=120, borderwidth=2, relief="groove")
recipe_planned_frame1.pack_propagate(False)
recipe_planned_frame1.pack(fill='x', expand=True, padx=1, pady=1, side='right')

recipe_picture_frame_planned1 = tk.Frame(breakfast_recipe_fr_r, bg=theme[1],height=120, width=8, borderwidth=2, relief="groove")
recipe_picture_frame_planned1.pack_propagate(False)
recipe_picture_frame_planned1.pack(fill='x', expand=True, padx=10, pady=1, side='left')

canvas_recipe_planned1 = Canvas(recipe_picture_frame_planned1, height=120, width=120)
canvas_recipe_planned1.pack(padx=5, pady=5)

image_container_recipe_planned1 = canvas_recipe_planned1.create_image(0, 0, anchor=NW, image=empty_recipe_planned)

extra_name_frame_planned = tk.Frame(recipe_planned_frame1, bg=theme[5],height=40, width=120)
extra_name_frame_planned.pack_propagate(False)
extra_name_frame_planned.pack(fill='x', expand=True, padx=1, pady=1)

name_recipe_small_planned = Label(extra_name_frame_planned,
                bg=theme[5],
                font=("CourierNew", 12),
                text="",
                anchor=W, 
                wraplength=230)
name_recipe_small_planned.grid(padx=10, pady=5, sticky=W)

extra_info_frame_planned = tk.Frame(recipe_planned_frame1, bg=theme[5],height=90, width=120)
extra_info_frame_planned.pack_propagate(False)
extra_info_frame_planned.pack(fill='x', expand=True, padx=1, pady=1)

descr_recipe_small_planned = Label(extra_info_frame_planned,
                bg=theme[5],
                font=("CourierNew", 10),
                text="",
                anchor=W,
                wraplength=230, 
                justify="left")
descr_recipe_small_planned.grid(padx=10, pady=10, sticky=W)

breakfast_recipe_empty_fr = tk.Frame(breakfast_recipe_frame, bg=theme[3],height=150, borderwidth=2, relief="groove")
breakfast_recipe_empty_fr.pack(fill='x', expand=True, padx = 10, pady=5)
breakfast_recipe_empty_fr.pack_propagate(False)

canvas_recipe_planned11 = Canvas(breakfast_recipe_empty_fr, height=100, width=400, bg = theme[5])
canvas_recipe_planned11.pack(padx=5)

image_container_recipe_planned11 = canvas_recipe_planned11.create_image(0, 0, anchor=NW, image=empty_recipe_planned)

flag = False
br_recipe = 0

for each in planned_cl:
    if each.get_day() == today and each.get_period() == "brf":
        flag = True
        br_recipe = each.get_recipe()

if flag == True:
    for each in recipes_cl:
        if each.get_recipe_id() == br_recipe:

            breakfast_recipe_empty_fr.pack_forget()
            breakfast_recipe_fr_r.pack(fill='x', expand=True)


            name_recipe_small_planned.config(text=each.get_name())
            descr_recipe_small_planned.config(text=each.get_description())

            new_pic = PhotoImage(file=each.get_picture())

            canvas_recipe_planned1.itemconfig(image_container_recipe_planned1,image=new_pic)
            canvas_recipe_planned1.image = new_pic
else:

    breakfast_recipe_fr_r.pack_forget()
    breakfast_recipe_empty_fr.pack(fill='x', expand=True)


breakfast_recipe_empty_fr.bind("<Button-1>",
            lambda e:
            plan_recipe('brf'))

canvas_recipe_planned11.bind("<Button-1>",
            lambda e:
            plan_recipe('brf'))

breakfast_recipe_fr_r.bind("<Button-1>",
            lambda e:
            plan_recipe('brf'))

recipe_planned_frame1.bind("<Button-1>",
            lambda e:
            plan_recipe('brf'))

recipe_picture_frame_planned1.bind("<Button-1>",
            lambda e:
            plan_recipe('brf'))

canvas_recipe_planned1.bind("<Button-1>",
            lambda e:
            plan_recipe('brf'))

extra_name_frame_planned.bind("<Button-1>",
            lambda e:
            plan_recipe('brf'))

name_recipe_small_planned.bind("<Button-1>",
            lambda e:
            plan_recipe('brf'))

extra_info_frame_planned.bind("<Button-1>",
            lambda e:
            plan_recipe('brf'))

descr_recipe_small_planned.bind("<Button-1>",
            lambda e:
            plan_recipe('brf'))


lunch_frame = tk.Frame(middle_meal_plan, bg=theme[5],height=170, borderwidth=2, relief="groove")
lunch_frame.pack(fill='x', expand=True, padx = 10, pady=5)
lunch_frame.pack_propagate(False)

lunch_label = Label(lunch_frame,
                      font=("CourierNew", 12),
                      bg=theme[5],
                      width=38,
                      text="Lunch")
lunch_label.pack(padx=5, pady=15)

lunch_recipe_frame = tk.Frame(lunch_frame, bg=theme[3],height=150, borderwidth=2, relief="groove")
lunch_recipe_frame.pack(fill='x', expand=True, padx = 10, pady=5)
lunch_recipe_frame.pack_propagate(False)

lunch_recipe_frame_r = tk.Frame(lunch_recipe_frame, bg=theme[3],height=150, borderwidth=2, relief="groove")
lunch_recipe_frame_r.pack(fill='x', expand=True)
lunch_recipe_frame_r.pack_propagate(False)

recipe_planned_frame2 = tk.Frame(lunch_recipe_frame_r, bg=theme[5],height=150, width=120, borderwidth=2, relief="groove")
recipe_planned_frame2.pack_propagate(False)
recipe_planned_frame2.pack(fill='x', expand=True, padx=1, pady=1, side='right')

recipe_picture_frame_planned2 = tk.Frame(lunch_recipe_frame_r, bg=theme[1],height=120, width=8, borderwidth=2, relief="groove")
recipe_picture_frame_planned2.pack_propagate(False)
recipe_picture_frame_planned2.pack(fill='x', expand=True, padx=10, pady=1, side='left')

canvas_recipe_planned2 = Canvas(recipe_picture_frame_planned2, height=120, width=120)
canvas_recipe_planned2.pack(padx=5, pady=5)

image_container_recipe_planned2 = canvas_recipe_planned2.create_image(0, 0, anchor=NW, image=empty_recipe_planned)

extra_name_frame_planned2 = tk.Frame(recipe_planned_frame2, bg=theme[5],height=40, width=120)
extra_name_frame_planned2.pack_propagate(False)
extra_name_frame_planned2.pack(fill='x', expand=True, padx=1, pady=1)

name_recipe_small_planned2 = Label(extra_name_frame_planned2,
                bg=theme[5],
                font=("CourierNew", 12),
                text="",
                anchor=W, 
                wraplength=230)
name_recipe_small_planned2.grid(padx=10, pady=5, sticky=W)

extra_info_frame_planned2 = tk.Frame(recipe_planned_frame2, bg=theme[5],height=90, width=120)
extra_info_frame_planned2.pack_propagate(False)
extra_info_frame_planned2.pack(fill='x', expand=True, padx=1, pady=1)

descr_recipe_small_planned2 = Label(extra_info_frame_planned2,
                bg=theme[5],
                font=("CourierNew", 10),
                text="",
                anchor=W,
                wraplength=230, 
                justify="left")
descr_recipe_small_planned2.grid(padx=10, pady=10, sticky=W)

lunch_recipe_empty_fr = tk.Frame(lunch_recipe_frame, bg=theme[3],height=150, borderwidth=2, relief="groove")
lunch_recipe_empty_fr.pack(fill='x', expand=True, padx = 10, pady=5)
lunch_recipe_empty_fr.pack_propagate(False)

canvas_recipe_planned22 = Canvas(lunch_recipe_empty_fr, height=100, width=400, bg = theme[5])
canvas_recipe_planned22.pack(padx=5)

image_container_recipe_planned22 = canvas_recipe_planned22.create_image(0, 0, anchor=NW, image=empty_recipe_planned)

flag = False
br_recipe = 0

for each in planned_cl:
    if each.get_day() == today and each.get_period() == "lnc":
        flag = True
        br_recipe = each.get_recipe()

if flag == True:
    for each in recipes_cl:
        if each.get_recipe_id() == br_recipe:

            lunch_recipe_empty_fr.pack_forget()
            lunch_recipe_frame_r.pack(fill='x', expand=True)


            name_recipe_small_planned2.config(text=each.get_name())
            descr_recipe_small_planned2.config(text=each.get_description())

            new_pic = PhotoImage(file=each.get_picture())

            canvas_recipe_planned2.itemconfig(image_container_recipe_planned2,image=new_pic)
            canvas_recipe_planned2.image = new_pic
else:

    lunch_recipe_frame_r.pack_forget()
    lunch_recipe_empty_fr.pack(fill='x', expand=True)

lunch_recipe_empty_fr.bind("<Button-1>",
            lambda e:
            plan_recipe('lnc'))

canvas_recipe_planned22.bind("<Button-1>",
            lambda e:
            plan_recipe('lnc'))

lunch_recipe_frame_r.bind("<Button-1>",
            lambda e:
            plan_recipe('lnc'))

recipe_planned_frame2.bind("<Button-1>",
            lambda e:
            plan_recipe('lnc'))

recipe_picture_frame_planned2.bind("<Button-1>",
            lambda e:
            plan_recipe('lnc'))

canvas_recipe_planned2.bind("<Button-1>",
            lambda e:
            plan_recipe('lnc'))

extra_name_frame_planned2.bind("<Button-1>",
            lambda e:
            plan_recipe('lnc'))

name_recipe_small_planned2.bind("<Button-1>",
            lambda e:
            plan_recipe('lnc'))

extra_info_frame_planned2.bind("<Button-1>",
            lambda e:
            plan_recipe('lnc'))

descr_recipe_small_planned2.bind("<Button-1>",
            lambda e:
            plan_recipe('lnc'))


dinner_frame = tk.Frame(middle_meal_plan, bg=theme[5],height=170, borderwidth=2, relief="groove")
dinner_frame.pack(fill='x', expand=True, padx = 10, pady=10)
dinner_frame.pack_propagate(False)

dinner_label = Label(dinner_frame,
                      font=("CourierNew", 12),
                      bg=theme[5],
                      width=38, 
                      text="Dinner")
dinner_label.pack(padx=5, pady=15)

dinner_recipe_frame = tk.Frame(dinner_frame, bg=theme[3],height=150, borderwidth=2, relief="groove")
dinner_recipe_frame.pack(fill='x', expand=True, padx = 10, pady=5)
dinner_recipe_frame.pack_propagate(False)

dinner_recipe_frame_rr = tk.Frame(dinner_recipe_frame, bg=theme[3],height=150, borderwidth=2, relief="groove")
dinner_recipe_frame_rr.pack(fill='x', expand=True)
dinner_recipe_frame_rr.pack_propagate(False)

recipe_planned_frame3 = tk.Frame(dinner_recipe_frame_rr, bg=theme[5],height=150, width=120, borderwidth=2, relief="groove")
recipe_planned_frame3.pack_propagate(False)
recipe_planned_frame3.pack(fill='x', expand=True, padx=1, pady=1, side='right')

recipe_picture_frame_planned3 = tk.Frame(dinner_recipe_frame_rr, bg=theme[1],height=120, width=8, borderwidth=2, relief="groove")
recipe_picture_frame_planned3.pack_propagate(False)
recipe_picture_frame_planned3.pack(fill='x', expand=True, padx=10, pady=1, side='left')

canvas_recipe_planned3 = Canvas(recipe_picture_frame_planned3, height=120, width=120)
canvas_recipe_planned3.pack(padx=5, pady=5)

image_container_recipe_planned3 = canvas_recipe_planned3.create_image(0, 0, anchor=NW, image=empty_recipe_planned)

extra_name_frame_planned3 = tk.Frame(recipe_planned_frame3, bg=theme[5],height=40, width=120)
extra_name_frame_planned3.pack_propagate(False)
extra_name_frame_planned3.pack(fill='x', expand=True, padx=1, pady=1)

name_recipe_small_planned3 = Label(extra_name_frame_planned3,
                bg=theme[5],
                font=("CourierNew", 12),
                text='',
                anchor=W, 
                wraplength=230)
name_recipe_small_planned3.grid(padx=10, pady=5, sticky=W)

extra_info_frame_planned3 = tk.Frame(recipe_planned_frame3, bg=theme[5],height=90, width=120)
extra_info_frame_planned3.pack_propagate(False)
extra_info_frame_planned3.pack(fill='x', expand=True, padx=1, pady=1)

descr_recipe_small_planned3 = Label(extra_info_frame_planned3,
                bg=theme[5],
                font=("CourierNew", 10),
                text='',
                anchor=W,
                wraplength=230, 
                justify="left")
descr_recipe_small_planned3.grid(padx=10, pady=10, sticky=W)


dinner_recipe_empty_fr = tk.Frame(dinner_recipe_frame, bg=theme[3],height=150, borderwidth=2, relief="groove")
dinner_recipe_empty_fr.pack(fill='x', expand=True, padx = 10, pady=5)
dinner_recipe_empty_fr.pack_propagate(False)

canvas_recipe_planned33 = Canvas(dinner_recipe_empty_fr, height=100, width=400, bg = theme[5])
canvas_recipe_planned33.pack(padx=5)

image_container_recipe_planned33 = canvas_recipe_planned33.create_image(0, 0, anchor=NW, image=empty_recipe_planned)


flag = False
br_recipe = 0

for each in planned_cl:
    if each.get_day() == today and each.get_period() == "dnr":
        flag = True
        br_recipe = each.get_recipe()

if flag == True:
    for each in recipes_cl:
        if each.get_recipe_id() == br_recipe:

            dinner_recipe_empty_fr.pack_forget()
            dinner_recipe_frame_rr.pack(fill='x', expand=True)


            name_recipe_small_planned3.config(text=each.get_name())
            descr_recipe_small_planned3.config(text=each.get_description())

            new_pic = PhotoImage(file=each.get_picture())

            canvas_recipe_planned3.itemconfig(image_container_recipe_planned3,image=new_pic)
            canvas_recipe_planned3.image = new_pic
else:

    dinner_recipe_frame_rr.pack_forget()
    dinner_recipe_empty_fr.pack(fill='x', expand=True)


dinner_recipe_empty_fr.bind("<Button-1>",
            lambda e:
            plan_recipe('dnr'))

canvas_recipe_planned33.bind("<Button-1>",
            lambda e:
            plan_recipe('dnr'))

dinner_recipe_frame_rr.bind("<Button-1>",
            lambda e:
            plan_recipe('dnr'))

recipe_planned_frame3.bind("<Button-1>",
            lambda e:
            plan_recipe('dnr'))

recipe_picture_frame_planned3.bind("<Button-1>",
            lambda e:
            plan_recipe('dnr'))

canvas_recipe_planned3.bind("<Button-1>",
            lambda e:
            plan_recipe('dnr'))

extra_name_frame_planned3.bind("<Button-1>",
            lambda e:
            plan_recipe('dnr'))

name_recipe_small_planned3.bind("<Button-1>",
            lambda e:
            plan_recipe('dnr'))

extra_info_frame_planned3.bind("<Button-1>",
            lambda e:
            plan_recipe('dnr'))

descr_recipe_small_planned3.bind("<Button-1>",
            lambda e:
            plan_recipe('dnr'))


#MENU OF RECIPES - MEAL PLAN

recipes_frame_plan = tk.Frame(main_frames, bg=theme[3],height=main_frame_height)
recipes_frame_plan.pack(fill='x', expand=True)
recipes_frame_plan.pack_propagate(False) 
recipes_frame_plan.pack_forget()

top_recipes_plan = tk.Frame(recipes_frame_plan, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_recipes_plan.pack(fill='x', expand=True)
top_recipes_plan.grid_columnconfigure(0, weight=8) 
top_recipes_plan.pack_propagate(False)

canvas_search_plan = Canvas(top_recipes_plan,height=40, width=40, bg=theme[5])
canvas_search_plan.grid(column=0, row=0, sticky=tk.W, padx=5, pady=10)
image_container_fav_plan = canvas_search_plan.create_image(5, 5, anchor=NW, image=button_photo9)

search_text_recipes_plan = StringVar()          
search_text_recipes_plan.trace_add('write', search_recipes_plan)
entry_search_recipes_plan = Entry(top_recipes_plan, width=49,  font=("CourierNew", 10), textvariable = search_text_recipes_plan)
entry_search_recipes_plan.grid(column=1, row=0, sticky=tk.W, padx=5)


close_plan_meal = Button(top_recipes_plan,
                          command=close_recipes_plan_menu,
                          font=("CourierNew", 10),
                          activebackground=theme[4],
                          activeforeground=theme[1],
                          bg=theme[5],
                          fg=theme[0],
                          image = button_photo8, 
                          compound = LEFT,
                          borderwidth=0,
                          width = 40,
                          height= 40)
close_plan_meal.grid(column=2, row=0, sticky=tk.W, padx=5)
close_plan_meal.pack_propagate(False) 

middle_recipes_plan = tk.Frame(recipes_frame_plan, bg=theme[5],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_recipes_plan.pack(fill='x', expand=True)
middle_recipes_plan.pack_propagate(False)

canvas_recipe_plan = Canvas(middle_recipes_plan,  bg=theme[1])
scrollbar_recipe_plan = ttk.Scrollbar(middle_recipes_plan, orient="vertical", command=canvas_recipe_plan.yview)
main_recipes_frame_plan = tk.Frame(canvas_recipe_plan, bg=theme[1])
main_recipes_frame_plan.pack(fill='x', expand=True)

main_recipes_frame_plan.bind("<Configure>", lambda e: canvas_recipe_plan.configure(scrollregion=canvas_recipe_plan.bbox("all")))

canvas_recipe_plan.create_window((0, 0), window=main_recipes_frame_plan, anchor="nw")
canvas_recipe_plan.configure(yscrollcommand=scrollbar_recipe_plan.set)

canvas_recipe_plan.pack(side="left", fill="both", expand=True)
scrollbar_recipe_plan.pack(side="right", fill="y")

image_references_plan = []
recipes_frames_holder_plan = []
counter12_plan = 0

upload_main_recipe_menu_plan(recipes_frames_holder_plan, counter12_plan, recipes_cl)

# SETTINGS PAGE 

settings_frame = tk.Frame(main_frames, bg=theme[3],height=main_frame_height)
settings_frame.pack(fill='x', expand=True)
settings_frame.pack_propagate(False) 
settings_frame.pack_forget()

top_settings = tk.Frame(settings_frame, bg=theme[5],height=panel_height, borderwidth=2, relief="groove")
top_settings.pack(fill='x', expand=True)
top_settings.grid_columnconfigure(0, weight=8) 
top_settings.pack_propagate(False)

settings_label = Label(top_settings,
                      font=("CourierNew", 12),
                      bg=theme[5],
                      width=38,
                      text="Settings")
settings_label.pack(padx=5, pady=15)

middle_settings = tk.Frame(settings_frame, bg=theme[2],height=main_frame_height-panel_height, borderwidth=2, relief="groove")
middle_settings.pack(fill='x', expand=True)
middle_settings.pack_propagate(False)

colour_changing = tk.Frame(middle_settings, bg=theme[5],height=400, borderwidth=2, relief="groove")
colour_changing.pack(fill='x', expand=True, padx=10, pady=10)
colour_changing.pack_propagate(False)

colour_change_label = Label(colour_changing,
                      font=("CourierNew", 12),
                      bg=theme[5],
                      width=38,
                      text="Change the application's colour theme:")
colour_change_label.pack(padx=5, pady=20)

theme1_button = Button(colour_changing,
                          command=lambda: change_application_theme('yellow'),
                          activebackground=theme[1],
                          activeforeground=theme[1],
                          bg=theme[2],
                          fg=theme[0],
                          text = "Theme 1", 
                          height= 2,
                          width = 50,
                          borderwidth=1)
theme1_button.pack(padx=5, pady=10)
theme1_button.pack_propagate(False)

theme2_button = Button(colour_changing,
                          command=lambda: change_application_theme('blue'),
                          activebackground=theme[1],
                          activeforeground=theme[1],
                          bg=theme[2],
                          fg=theme[0],
                          text = "Theme 2", 
                          height= 2,
                          width = 50,
                          borderwidth=1)
theme2_button.pack(padx=5, pady=10)
theme2_button.pack_propagate(False)

theme3_button = Button(colour_changing,
                          command=lambda: change_application_theme('green'),
                          activebackground=theme[1],
                          activeforeground=theme[1],
                          bg=theme[2],
                          fg=theme[0],
                          text = "Theme 3", 
                          height= 2,
                          width = 50,
                          borderwidth=1)
theme3_button.pack(padx=5, pady=10)
theme3_button.pack_propagate(False)

theme4_button = Button(colour_changing,
                          command=lambda: change_application_theme('red'),
                          activebackground=theme[1],
                          activeforeground=theme[1],
                          bg=theme[2],
                          fg=theme[0],
                          text = "Theme 4", 
                          height= 2,
                          width = 50,
                          borderwidth=1)
theme4_button.pack(padx=5, pady=10)
theme4_button.pack_propagate(False)

theme5_button = Button(colour_changing,
                          command=lambda: change_application_theme('grey'),
                          activebackground=theme[1],
                          activeforeground=theme[1],
                          bg=theme[2],
                          fg=theme[0],
                          text = "Theme 5", 
                          height= 2,
                          width = 50,
                          borderwidth=1)
theme5_button.pack(padx=5, pady=10)
theme5_button.pack_propagate(False)

file_download = tk.Frame(middle_settings, bg=theme[5],height=300, borderwidth=2, relief="groove")
file_download.pack(fill='x', expand=True, padx = 10, pady=10)
file_download.pack_propagate(False)

file_download_label = Label(file_download,
                      font=("CourierNew", 12),
                      bg=theme[5],
                      width=38,
                      text="Press to download shopping list as text file:")
file_download_label.pack(padx=5, pady=15)

download_button = Button(file_download,
                          command=save_to_txt_file,
                          activebackground=theme[1],
                          activeforeground=theme[1],
                          bg=theme[2],
                          fg=theme[0],
                          image = button_photo15, 
                          height=40,
                          width = 200,
                          borderwidth=1)
download_button.pack(padx=5, pady=10)
download_button.pack_propagate(False)


window.mainloop()