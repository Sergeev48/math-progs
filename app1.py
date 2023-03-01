import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import numpy as np
from sympy import *
import timeit
import math
from scipy.optimize import minimize


win = tk.Tk()
win.title('Реализация и исследование методов Монте-Карло и имитации отжига')
win.geometry("600x500")
win.resizable(False,False)

tabControl = ttk.Notebook(win)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='метод Монте-Карло')
tabControl.add(tab2, text ='метод имитации отжига')
tabControl.pack(expand = 1, fill ="both")

tab1.grid_columnconfigure(0,minsize=200)
tab2.grid_columnconfigure(0,minsize=200)


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
    
def openFile2():
    tf = filedialog.askopenfilename(
        initialdir="", 
        title="Open Text file", 
        filetypes=(("Text Files", "*.txt"),)
        )
    tf = open(tf)  # or tf = open(tf, 'r')
    data = tf.read()
    func2.delete(0,tk.END)
    func2.insert(END, data)
    tf.close()


x1,x2 = symbols("x1 x2")

def algorithm_1(N, expression,x1min,x2min,x1max,x2max,accuracy):
    begin = timeit.default_timer() 
    fmin = np.inf
    xmin1 = np.nan
    xmin2 = np.nan
    for i in range(N):
        tab1.update()
        progressbar1['value'] += 100/N
        x1_rand = np.random.uniform(x1min, x1max)
        x2_rand = np.random.uniform(x2min, x2max)
        f_xi = expression.subs([(x1, x1_rand), (x2, x2_rand)])
        if f_xi < fmin:
            xmin1 = x1_rand
            xmin2 = x2_rand
            fmin = f_xi
    end = timeit.default_timer() - begin 
    return(round(fmin,accuracy),round(xmin1,accuracy),round(xmin2,accuracy),round(end,2))
 
def algorithm_2(T,L,r,eps,expression,x1min,x2min,x1max,x2max,accuracy):
    begin = timeit.default_timer() 
    x1_rand = np.random.uniform(x1min, x1max)
    x2_rand = np.random.uniform(x2min, x2max)
    f_xi = expression.subs([(x1, x1_rand), (x2, x2_rand)])
    x = Symbol('x')
    z = solve(0.9**x - 0.0001, x)
    z = round(int(z[0]))
    while(T > pow(10, -4)):
        for i in range(L):
            progressbar2['value'] += 100/L/z
            tab2.update()
            x1_eps = np.random.uniform(x1_rand - eps, x1_rand + eps)
            x2_eps = np.random.uniform(x1_rand - eps, x1_rand + eps)
            f_eps = expression.subs([(x1, x1_eps), (x2, x2_eps)])
            if (f_eps < f_xi):
                x1_rand = x1_eps
                x2_rand = x2_eps
                f_xi = f_eps
            else:
                k = math.exp(-(f_eps - f_xi)/T)
                q = np.random.uniform(0, 1)
                if (k > q):
                    x1_rand = x1_eps
                    x2_rand = x2_eps
                    f_xi = f_eps
        T = r*T
    expr = lambdify((x1,x2),expression)
    def my_func_v(x):
        return expr(*tuple(x))
    result = minimize(my_func_v,(x1_rand,x2_rand), method='nelder-mead',
               options={'xatol': 1e-8, 'disp': True})
    end = timeit.default_timer() - begin # получаем разницу в секундах
    return(round(result.fun,accuracy),round(result.x[0],accuracy),round(result.x[1],accuracy),round(end,2))

def calculate_1():
    progressbar1['value'] = 0
    answer_1.config(text="")
    x_1.config(text="")
    x_2.config(text="")
    f_x_1.config(text="")
    time_1.config(text="")
    progressbar1.grid(column=1,row=8)
    button1['state'] = tk.DISABLED
    seed_calc =int(seed.get())
    np.random.seed(seed_calc)
    Num = int(points.get())
    expression = (func.get())
    expression = sympify(expression)
    x1min = float(min_x1.get())
    x2min = float(min_x2.get())
    x1max = float(max_x1.get())
    x2max = float(max_x2.get())
    accuracy = int(acc.get())
    result = algorithm_1(Num, expression,x1min,x2min,x1max,x2max,accuracy)
    progressbar1.grid_forget()
    answer_1.config(text="Ответ:")
    x_1.config(text="f(x): " + str(result[0]))
    x_2.config(text="x1: " + str(result[1]))
    f_x_1.config(text="x2: " + str(result[2]))
    time_1.config(text="Время: " + str(result[3]))
    
    button1['state'] = tk.NORMAL


def calculate_2():
    progressbar2['value'] = 0
    answer_2.config(text="")
    x_1_2.config(text="")
    x_2_2.config(text="")
    f_x_2.config(text="")
    time_2.config(text="")
    progressbar2.grid(column=1,row=14)
    button2['state'] = tk.DISABLED
    seed_calc =int(seed2.get())
    np.random.seed(seed_calc)
    expression = (func2.get())
    expression = sympify(expression)
    Temp = int(temperature.get())
    Cyc = int(cycles.get())
    r = float(coef.get())
    eps = float(ocr.get())
    x1min = float(min2_x1.get())
    x2min = float(min2_x2.get())
    x1max = float(max2_x1.get())
    x2max = float(max2_x2.get())
    accuracy = int(acc2.get())
    result = algorithm_2(Temp,Cyc,r,eps,expression,x1min,x2min,x1max,x2max,accuracy)
    progressbar2.grid_forget()
    answer_2.config(text="Ответ:")
    x_1_2.config(text="f(x): " + str(result[0]))
    x_2_2.config(text="x1: " + str(result[1]))
    f_x_2.config(text="x2: " + str(result[2]))
    time_2.config(text="Время: " + str(result[3]))
    button2['state'] = tk.NORMAL

ttk.Label(tab1, text="Функция:", ).grid(padx=6, pady=6)
func = ttk.Entry(tab1)
func.grid(padx=6, pady=6,sticky='we')
tk.Button(tab1,text="Открыть из файла",command=openFile1).grid(padx=6, pady=6,column=1,row=0)
ttk.Label(tab1, text="Число точек:").grid(padx=6, pady=6)
points = ttk.Entry(tab1)
points.grid(padx=6, pady=6,sticky='we')
points.insert(0, "1000")

ttk.Label(tab1, text="Точность:").grid(padx=6, pady=6)
acc = ttk.Spinbox(tab1, from_ = 1, to = 10)
acc.grid(padx=6, pady=6,sticky='we')
acc.insert(0, "5")


ttk.Label(tab1, text="seed:", ).grid(padx=6, pady=6)
seed = ttk.Entry(tab1)
seed.grid(padx=6, pady=6,sticky='we')
seed.insert(0, "10")

button1 = tk.Button(tab1,text="Вычислить",command=calculate_1)
button1.grid(padx=6, pady=6)



ttk.Label(tab1, text="Ограничения:", ).grid(padx=6, pady=6, column=2,row=2)
ttk.Label(tab1, text=" < x1 < ", ).grid(padx=6, pady=6, column=2,row=3)
ttk.Label(tab1, text=" < x2 < ", ).grid(padx=6, pady=6, column=2,row=4)
min_x1 = ttk.Entry(tab1)
min_x2 = ttk.Entry(tab1)
max_x1 = ttk.Entry(tab1)
max_x2 = ttk.Entry(tab1)

min_x1.grid(padx=6, pady=6, column=1,row=3)
min_x2.grid(padx=6, pady=6, column=1,row=4)
max_x1.grid(padx=6, pady=6, column=3,row=3)
max_x2.grid(padx=6, pady=6, column=3,row=4)
min_x1.insert(0, "-10")
min_x2.insert(0, "-10")
max_x1.insert(0, "10")
max_x2.insert(0, "10")
answer_1 = ttk.Label(tab1, text="")
answer_1.grid(padx=6, pady=6, column=1,row=5,sticky='w')
x_1 = ttk.Label(tab1, text="")
x_1.grid(padx=6, pady=6, column=1,row=6,sticky='w')
x_2 = ttk.Label(tab1, text="")
x_2.grid(padx=6, pady=6, column=1,row=7,sticky='w')
f_x_1 = ttk.Label(tab1, text="")
f_x_1.grid(padx=6, pady=6, column=1,row=8,sticky='w')
time_1 = ttk.Label(tab1, text="")
time_1.grid(padx=6, pady=6, column=1,row=9,sticky='w')

progressbar1 = ttk.Progressbar(tab1,orient="horizontal", length=150, value=0)

progressbar2 = ttk.Progressbar(tab2,orient="horizontal", length=150, value=0)
















ttk.Label(tab2, text="Функция:", ).grid(padx=1, pady=1)
func2 = ttk.Entry(tab2)
func2.grid(padx=1, pady=1,sticky='we')
tk.Button(tab2,text="Открыть из файла",command=openFile2).grid(padx=1, pady=1,column=1,row=0)

ttk.Label(tab2, text="Количество циклов:").grid(padx=1, pady=1)
cycles = ttk.Entry(tab2)
cycles.grid(padx=1, pady=1,sticky='we')
cycles.insert(0, "1000")

ttk.Label(tab2, text="Температура:").grid(padx=1, pady=1)
temperature = ttk.Entry(tab2)
temperature.grid(padx=1, pady=1,sticky='we')
temperature.insert(0, "1")

ttk.Label(tab2, text="Коэффициент\nснижения температуры:").grid(padx=1, pady=1)
coef = ttk.Entry(tab2)
coef.grid(padx=1, pady=1,sticky='we')
coef.insert(0, "0.9")

ttk.Label(tab2, text="Окрестность\nдля выбора точек:").grid(padx=1, pady=1)
ocr = ttk.Entry(tab2)
ocr.grid(padx=1, pady=1,sticky='we')
ocr.insert(0, "0.01")



ttk.Label(tab2, text="Точность:").grid(padx=1, pady=1)
acc2 = ttk.Spinbox(tab2, from_ = 1, to = 10)
acc2.grid(padx=1, pady=1,sticky='we')
acc2.insert(0, "5")


ttk.Label(tab2, text="seed:", ).grid(padx=1, pady=1)
seed2 = ttk.Entry(tab2)
seed2.grid(padx=1, pady=1,sticky='we')
seed2.insert(0, "10")

button2 = tk.Button(tab2,text="Вычислить",command=calculate_2)
button2.grid(padx=6, pady=6)



ttk.Label(tab2, text="Ограничения:", ).grid(padx=6, pady=6, column=2,row=2)
ttk.Label(tab2, text=" < x1 < ", ).grid(padx=6, pady=6, column=2,row=3)
ttk.Label(tab2, text=" < x2 < ", ).grid(padx=6, pady=6, column=2,row=4)
min2_x1 = ttk.Entry(tab2)
min2_x2 = ttk.Entry(tab2)
max2_x1 = ttk.Entry(tab2)
max2_x2 = ttk.Entry(tab2)

min2_x1.grid(padx=6, pady=6, column=1,row=3)
min2_x2.grid(padx=6, pady=6, column=1,row=4)
max2_x1.grid(padx=6, pady=6, column=3,row=3)
max2_x2.grid(padx=6, pady=6, column=3,row=4)
min2_x1.insert(0, "-10")
min2_x2.insert(0, "-10")
max2_x1.insert(0, "10")
max2_x2.insert(0, "10")
answer_2 = ttk.Label(tab2, text="")
answer_2.grid(padx=6, pady=6, column=1,row=5,sticky='w')
x_1_2 = ttk.Label(tab2, text="")
x_1_2.grid(padx=6, pady=6, column=1,row=6,sticky='w')
x_2_2 = ttk.Label(tab2, text="")
x_2_2.grid(padx=6, pady=6, column=1,row=7,sticky='w')
f_x_2 = ttk.Label(tab2, text="")
f_x_2.grid(padx=6, pady=6, column=1,row=8,sticky='w')
time_2 = ttk.Label(tab2, text="")
time_2.grid(padx=6, pady=6, column=1,row=9,sticky='w')








win.mainloop()