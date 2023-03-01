import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from sympy import *
import timeit
import math
from sympy.combinatorics.graycode import gray_to_bin
from sympy.combinatorics.graycode import bin_to_gray
import random


win = tk.Tk()
win.title('Реализация и исследование генетического алгоритма')
win.geometry("600x500")
win.resizable(False,False)  


def openFile1():
    tf = filedialog.askopenfilename(
        initialdir="", 
        title="Open Text file", 
        filetypes=(("Text Files", "*.txt"),)
        )
    tf = open(tf)  # or tf = open(tf, 'r')
    data = tf.read()
    func.delete(0,tk.END)
    func.insert(END, data)
    tf.close()
    

x1,x2 = symbols("x1 x2")

def algorithm_1(generation,population_count,selection_prob,crossing_prob,mutation_prob,сrossing_v,stop_v,expression,x1_min,x2_min,x1_max,x2_max,accuracy,interval):
    begin = timeit.default_timer() 
    
    interval_2 = int(math.log2(interval))
    
    pop_elms = []
    for i in range(population_count):
        x1_rand = random.randint(0, interval)
        x2_rand = random.randint(0, interval)
        x1_res = x1_min + (x1_max - x1_min)*x1_rand/interval
        x2_res = x2_min + (x2_max - x2_min)*x2_rand/interval
        x1_bin = bin(x1_rand)[2:].zfill(interval_2)
        x2_bin = bin(x2_rand)[2:].zfill(interval_2)
        x1_gray = bin_to_gray(x1_bin).zfill(interval_2)
        x2_gray = bin_to_gray(x2_bin).zfill(interval_2)
        f_xi = expression.subs([(x1, x1_res), (x2, x2_res)])
        pop_elms.append([x1_res,x2_res,x1_bin,x2_bin,x1_gray,x2_gray,x1_rand,x2_rand,f_xi])
    pop_elms = sorted(pop_elms, key=lambda pop_elms: pop_elms[8])
    #Критерий останова

    if stop_v =='Достигнута популяция заданного предела качества':
    
        while(pop_elms[len(pop_elms)-1][8]/pop_elms[0][8] > 1.2):
            size = len(pop_elms)
            if size * selection_prob % 2 == 0:
                pop_size = int(len(pop_elms) * selection_prob)
            else:
                pop_size = int(len(pop_elms) * selection_prob + 1)
            del pop_elms[pop_size:size]
            random.shuffle(pop_elms)
            size = int(len(pop_elms)*crossing_prob)
            for i in range (0,size,2):
                #скрещивание
                crossing = cross(сrossing_v,pop_elms,i,interval_2)
                child_1_x1_gray = crossing[0]
                child_1_x2_gray = crossing[1]
                child_1_x1_bin = gray_to_bin(child_1_x1_gray).zfill(interval_2)
                child_1_x2_bin = gray_to_bin(child_1_x2_gray).zfill(interval_2)
                child_1_x1_rand = int(child_1_x1_bin, 2)
                child_1_x2_rand = int(child_1_x2_bin, 2)
                child_1_x1_res = x1_min + (x1_max - x1_min)*child_1_x1_rand/interval
                child_1_x2_res = x2_min + (x2_max - x2_min)*child_1_x2_rand/interval
                child_1_f_xi = expression.subs([(x1, child_1_x1_res), (x2, child_1_x2_res)])
                pop_elms.append([child_1_x1_res,child_1_x2_res,child_1_x1_bin,child_1_x2_bin,child_1_x1_gray,child_1_x2_gray,child_1_x1_rand,child_1_x2_rand,child_1_f_xi])

                child_2_x1_gray = crossing[2]
                child_2_x2_gray = crossing[3]

                child_2_x1_bin = gray_to_bin(child_1_x1_gray).zfill(interval_2)
                child_2_x2_bin = gray_to_bin(child_1_x2_gray).zfill(interval_2)
                child_2_x1_rand = int(child_1_x1_bin, 2)
                child_2_x2_rand = int(child_1_x2_bin, 2)
                child_2_x1_res = x1_min + (x1_max - x1_min)*child_1_x1_rand/interval
                child_2_x2_res = x2_min + (x2_max - x2_min)*child_1_x2_rand/interval
                child_2_f_xi = expression.subs([(x1, child_1_x1_res), (x2, child_1_x2_res)])
                pop_elms.append([child_2_x1_res,child_2_x2_res,child_2_x1_bin,child_2_x2_bin,child_2_x1_gray,child_2_x2_gray,child_2_x1_rand,child_2_x2_rand,child_2_f_xi])
            #мутация
            for i in range(len(pop_elms)):
                if random.random() <= mutation_prob:
                    rand = random.randint(0, interval_2-1)
                    if int(pop_elms[i][4][rand]) == 1:
                        pop_elms[i][4] = pop_elms[i][4][0:rand] + '0' + pop_elms[i][4][rand+1:]
                        pop_elms[i][2] = gray_to_bin(pop_elms[i][4]).zfill(interval_2)
                        pop_elms[i][6] = int(pop_elms[i][2], 2)
                        pop_elms[i][0] = x1_min + (x1_max - x1_min)*pop_elms[i][6] /interval

                    else:
                        pop_elms[i][4] = pop_elms[i][4][0:rand] + '1' + pop_elms[i][4][rand+1:]
                        pop_elms[i][2] = gray_to_bin(pop_elms[i][4]).zfill(interval_2)
                        pop_elms[i][6] = int(pop_elms[i][2], 2)
                        pop_elms[i][0] = x1_min + (x1_max - x1_min)*pop_elms[i][6] /interval


                    if int(pop_elms[i][5][rand]) == 1:
                        pop_elms[i][5] = pop_elms[i][5][0:rand] + '0' + pop_elms[i][5][rand+1:]
                        pop_elms[i][3] = gray_to_bin(pop_elms[i][5]).zfill(interval_2)
                        pop_elms[i][7] = int(pop_elms[i][3], 2)
                        pop_elms[i][1] = x1_min + (x1_max - x1_min)*pop_elms[i][7] /interval

                    else:
                        pop_elms[i][5] = pop_elms[i][5][0:rand] + '1' + pop_elms[i][5][rand+1:]
                        pop_elms[i][3] = gray_to_bin(pop_elms[i][5]).zfill(interval_2)
                        pop_elms[i][7] = int(pop_elms[i][3], 2)
                        pop_elms[i][1] = x1_min + (x1_max - x1_min)*pop_elms[i][7] /interval


                    pop_elms[i][8] = expression.subs([(x1, pop_elms[i][0]), (x2, pop_elms[i][1])])

            pop_elms = sorted(pop_elms, key=lambda pop_elms: pop_elms[8])
            del pop_elms[population_count:]
    
    else:
        for z in range(generation):
            size = len(pop_elms)
            if size * selection_prob % 2 == 0:
                pop_size = int(len(pop_elms) * selection_prob)
            else:
                pop_size = int(len(pop_elms) * selection_prob + 1)
            del pop_elms[pop_size:size]
            random.shuffle(pop_elms)
            size = int(len(pop_elms)*crossing_prob)
            for i in range (0,size,2):
                #скрещивание
                crossing = cross(сrossing_v,pop_elms,i,interval_2)
                child_1_x1_gray = crossing[0]
                child_1_x2_gray = crossing[1]
                child_1_x1_bin = gray_to_bin(child_1_x1_gray).zfill(interval_2)
                child_1_x2_bin = gray_to_bin(child_1_x2_gray).zfill(interval_2)
                child_1_x1_rand = int(child_1_x1_bin, 2)
                child_1_x2_rand = int(child_1_x2_bin, 2)
                child_1_x1_res = x1_min + (x1_max - x1_min)*child_1_x1_rand/interval
                child_1_x2_res = x2_min + (x2_max - x2_min)*child_1_x2_rand/interval
                child_1_f_xi = expression.subs([(x1, child_1_x1_res), (x2, child_1_x2_res)])
                pop_elms.append([child_1_x1_res,child_1_x2_res,child_1_x1_bin,child_1_x2_bin,child_1_x1_gray,child_1_x2_gray,child_1_x1_rand,child_1_x2_rand,child_1_f_xi])

                child_2_x1_gray = crossing[2]
                child_2_x2_gray = crossing[3]

                child_2_x1_bin = gray_to_bin(child_1_x1_gray).zfill(interval_2)
                child_2_x2_bin = gray_to_bin(child_1_x2_gray).zfill(interval_2)
                child_2_x1_rand = int(child_1_x1_bin, 2)
                child_2_x2_rand = int(child_1_x2_bin, 2)
                child_2_x1_res = x1_min + (x1_max - x1_min)*child_1_x1_rand/interval
                child_2_x2_res = x2_min + (x2_max - x2_min)*child_1_x2_rand/interval
                child_2_f_xi = expression.subs([(x1, child_1_x1_res), (x2, child_1_x2_res)])
                pop_elms.append([child_2_x1_res,child_2_x2_res,child_2_x1_bin,child_2_x2_bin,child_2_x1_gray,child_2_x2_gray,child_2_x1_rand,child_2_x2_rand,child_2_f_xi])
            #мутация
            for i in range(len(pop_elms)):
                if random.random() <= mutation_prob:
                    rand = random.randint(0, interval_2-1)
                    if int(pop_elms[i][4][rand]) == 1:
                        pop_elms[i][4] = pop_elms[i][4][0:rand] + '0' + pop_elms[i][4][rand+1:]
                        pop_elms[i][2] = gray_to_bin(pop_elms[i][4]).zfill(interval_2)
                        pop_elms[i][6] = int(pop_elms[i][2], 2)
                        pop_elms[i][0] = x1_min + (x1_max - x1_min)*pop_elms[i][6] /interval

                    else:
                        pop_elms[i][4] = pop_elms[i][4][0:rand] + '1' + pop_elms[i][4][rand+1:]
                        pop_elms[i][2] = gray_to_bin(pop_elms[i][4]).zfill(interval_2)
                        pop_elms[i][6] = int(pop_elms[i][2], 2)
                        pop_elms[i][0] = x1_min + (x1_max - x1_min)*pop_elms[i][6] /interval


                    if int(pop_elms[i][5][rand]) == 1:
                        pop_elms[i][5] = pop_elms[i][5][0:rand] + '0' + pop_elms[i][5][rand+1:]
                        pop_elms[i][3] = gray_to_bin(pop_elms[i][5]).zfill(interval_2)
                        pop_elms[i][7] = int(pop_elms[i][3], 2)
                        pop_elms[i][1] = x1_min + (x1_max - x1_min)*pop_elms[i][7] /interval

                    else:
                        pop_elms[i][5] = pop_elms[i][5][0:rand] + '1' + pop_elms[i][5][rand+1:]
                        pop_elms[i][3] = gray_to_bin(pop_elms[i][5]).zfill(interval_2)
                        pop_elms[i][7] = int(pop_elms[i][3], 2)
                        pop_elms[i][1] = x1_min + (x1_max - x1_min)*pop_elms[i][7] /interval


                    pop_elms[i][8] = expression.subs([(x1, pop_elms[i][0]), (x2, pop_elms[i][1])])

            pop_elms = sorted(pop_elms, key=lambda pop_elms: pop_elms[8])
            del pop_elms[population_count:]
    
    
    end = timeit.default_timer() - begin 
    print(str(round(end,5)) + " " + str(round(pop_elms[0][8],5)))
    return(round(pop_elms[0][8],accuracy),round(pop_elms[0][0],accuracy),round(pop_elms[0][1],accuracy),round(end,5))
 
def cross(сrossing_v,pop_elms,i,interval_2):
    if сrossing_v == 'Одноточечный':
        l = random.randint(1, interval_2-2)
        child_1_x1_gray = pop_elms[i][4][0:l+1] + pop_elms[i+1][4][l+1:interval_2]  
        child_1_x2_gray = pop_elms[i][5][0:l+1] + pop_elms[i+1][5][l+1:interval_2]
        
        child_2_x1_gray = pop_elms[i+1][4][0:l+1] + pop_elms[i][4][l+1:interval_2]  
        child_2_x2_gray = pop_elms[i+1][5][0:l+1] + pop_elms[i][5][l+1:interval_2]


    if сrossing_v == 'Двухточеченый':
        l = random.randint(1, 9)
        r = random.randint(l, interval_2-2)
        child_1_x1_gray = pop_elms[i][4][0:l+1] + pop_elms[i+1][4][l+1:r+1] + pop_elms[i][4][r+1:interval_2]  
        child_1_x2_gray = pop_elms[i][5][0:l+1] + pop_elms[i+1][5][l+1:r+1] + pop_elms[i][5][r+1:interval_2]
        
        child_2_x1_gray = pop_elms[i+1][4][0:l+1] + pop_elms[i][4][l+1:r+1] + pop_elms[i+1][4][r+1:interval_2]  
        child_2_x2_gray = pop_elms[i+1][5][0:l+1] + pop_elms[i][5][l+1:r+1] + pop_elms[i+1][5][r+1:interval_2]  
  

    if сrossing_v == 'Равномерный':
        res_string_x1 = ""
        res_string_x2 = ""
        for j in range(interval_2):
            if random.random() <= 0.5:
                res_string_x1 = res_string_x1 + pop_elms[i][4][j]
                res_string_x2 = res_string_x2 + pop_elms[i][5][j]
            else:
                res_string_x1 = res_string_x1 + pop_elms[i+1][4][j]
                res_string_x2 = res_string_x2 + pop_elms[i+1][5][j]
        child_1_x1_gray = res_string_x1
        child_1_x2_gray = res_string_x2

        res_string_x1 = ""
        res_string_x2 = ""
        for j in range(interval_2):
            if random.random() <= 0.5:
                res_string_x1 = res_string_x1 + pop_elms[i][4][j]
                res_string_x2 = res_string_x2 + pop_elms[i][5][j]
            else:
                res_string_x1 = res_string_x1 + pop_elms[i+1][4][j]
                res_string_x2 = res_string_x2 + pop_elms[i+1][5][j]
        child_2_x1_gray = res_string_x1
        child_2_x2_gray = res_string_x2

    return(child_1_x1_gray,child_1_x2_gray,child_2_x1_gray,child_2_x2_gray)



def calculate_1():
    answer_1.config(text="")
    x_1.config(text="")
    x_2.config(text="")
    f_x_1.config(text="")
    time_1.config(text="")
    button1['state'] = tk.DISABLED
    seed_calc =int(seed.get())
    random.seed(seed_calc)
    expression = (func.get())
    expression = sympify(expression)
    x1_min = float(min_x1.get())
    x2_min = float(min_x2.get())
    x1_max = float(max_x1.get())
    x2_max = float(max_x2.get())
    accuracy = int(acc.get())
    
    generation = int(gen.get())
    population_count = int(population_c.get())
    selection_prob = float(selection_p.get())
    crossing_prob = float(crossing_p.get())
    mutation_prob = float(mutation_p.get())
    сrossing_v = str(сrossing_var.get())
    stop_v = str(stop_var.get())

    interval = int(interv.get())

    result = algorithm_1(generation,population_count,selection_prob,crossing_prob,mutation_prob,сrossing_v,stop_v,expression,x1_min,x2_min,x1_max,x2_max,accuracy,interval)
    answer_1.config(text="Ответ:")
    x_1.config(text="f(x): " + str(result[0]))
    x_2.config(text="x1: " + str(result[1]))
    f_x_1.config(text="x2: " + str(result[2]))
    time_1.config(text="Время: " + str(result[3]))
    
    button1['state'] = tk.NORMAL


ttk.Label(win, text="Функция:", ).grid(padx=3, pady=6)
func = ttk.Entry(win)
func.grid(padx=3, pady=3,sticky='we')
tk.Button(win,text="Открыть из файла",command=openFile1).grid(padx=3, pady=6,column=1,row=0)
ttk.Label(win, text="Число поколений:").grid(padx=3, pady=3)
gen = ttk.Entry(win)
gen.grid(padx=3, pady=3,sticky='we')
gen.insert(0, "500")

ttk.Label(win, text="Размер популяции:").grid(padx=3, pady=3)
population_c = ttk.Entry(win)
population_c.grid(padx=3, pady=3,sticky='we')
population_c.insert(0, "50")

ttk.Label(win, text="Вероятность отбора:").grid(padx=3, pady=3)
selection_p = ttk.Entry(win)
selection_p.grid(padx=3, pady=3,sticky='we')
selection_p.insert(0, "0.8")

ttk.Label(win, text="Вероятность скрещивания:").grid(padx=3, pady=3)
crossing_p = ttk.Entry(win)
crossing_p.grid(padx=3, pady=3,sticky='we')
crossing_p.insert(0, "0.8")

ttk.Label(win, text="Вероятность мутации:").grid(padx=3, pady=3)
mutation_p = ttk.Entry(win)
mutation_p.grid(padx=3, pady=3,sticky='we')
mutation_p.insert(0, "0.5")


ttk.Label(win, text="Точность:").grid(padx=3, pady=3)
acc = ttk.Spinbox(win, from_ = 1, to = 10)
acc.grid(padx=3, pady=3,sticky='we')
acc.insert(0, "5")


ttk.Label(win, text="seed:", ).grid(padx=3, pady=3)
seed = ttk.Entry(win)
seed.grid(padx=3, pady=3,sticky='we')
seed.insert(0, "10")


button1 = tk.Button(win,text="Вычислить",command=calculate_1)
button1.grid(padx=3, pady=3)


ttk.Label(win, text="Количество интервалов:", ).grid(padx=3, pady=3,row=0,column=3)
interv = ttk.Entry(win)
interv.grid(padx=3, pady=3,row=1,column=3)
interv.insert(0, "4096")


ttk.Label(win, text="Ограничения:", ).grid(padx=3, pady=3, column=2,row=2)
ttk.Label(win, text=" < x1 < ", ).grid(padx=3, pady=3, column=2,row=3)
ttk.Label(win, text=" < x2 < ", ).grid(padx=3, pady=3, column=2,row=4)
min_x1 = ttk.Entry(win)
min_x2 = ttk.Entry(win)
max_x1 = ttk.Entry(win)
max_x2 = ttk.Entry(win)

min_x1.grid(padx=3, pady=3, column=1,row=3)
min_x2.grid(padx=3, pady=3, column=1,row=4)
max_x1.grid(padx=3, pady=3, column=3,row=3)
max_x2.grid(padx=3, pady=3, column=3,row=4)
min_x1.insert(0, "-10")
min_x2.insert(0, "-10")
max_x1.insert(0, "10")
max_x2.insert(0, "10")
answer_1 = ttk.Label(win, text="")
answer_1.grid(padx=3, pady=3, column=1,row=10,sticky='w')
x_1 = ttk.Label(win, text="")
x_1.grid(padx=3, pady=3, column=1,row=11,sticky='w')
x_2 = ttk.Label(win, text="")
x_2.grid(padx=3, pady=3, column=1,row=12,sticky='w')
f_x_1 = ttk.Label(win, text="")
f_x_1.grid(padx=3, pady=3, column=1,row=13,sticky='w')
time_1 = ttk.Label(win, text="")
time_1.grid(padx=3, pady=3, column=1,row=14,sticky='w')




ttk.Label(win, text="Тип скрещивания:", ).grid(padx=3, pady=3, column=1,row=6)

СrossingList = [
"Одноточечный",
"Двухточечный",
"Равномерный",
] 

сrossing_var = tk.StringVar(win)
сrossing_var.set(СrossingList[0])

opt1 = tk.OptionMenu(win, сrossing_var, *СrossingList)
opt1.grid(padx=3, pady=3, column=1,row=7,columnspan=3,sticky='we')


ttk.Label(win, text="Критерий останова:", ).grid(padx=3, pady=3, column=1,row=8)

StopList = [
"Сформировано заданное число поколений",
"Достигнута популяция заданного предела качества",
] 

stop_var = tk.StringVar(win)
stop_var.set(StopList[0])

opt2 = tk.OptionMenu(win, stop_var, *StopList)
opt2.grid(padx=3, pady=3, column=1,row=9,columnspan=3,sticky='we')

















win.mainloop()