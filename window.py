from config import (example_token, example_user, example_repository, window_title)
from gitcli import Gitcli
from githubanalyser import GitHubAnalyser
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import networkx as nx


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title(window_title)
        self.root.geometry('450x' + str(self.root.winfo_screenheight()) + '+0+0')

        self.main_frame = Frame(self.root)
        self.main_frame.pack(side=tk.TOP, fill=tk.Y)

        self.input_frame = Frame(self.main_frame)
        self.input_frame.pack(side=tk.BOTTOM, padx=5)

        self.fig = Figure(figsize=(5, 5), dpi=72)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.main_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax = self.fig.add_subplot(111)
        self.gitcli = ''
        self.githubAnalyzer = ''
        self.token_input = Entry()
        self.user_input = Entry()
        self.repo_input = Entry()

    def example(self):
        self.ax.clear()
        self.gitcli = Gitcli(example_token, example_user, example_repository)
        if self.gitcli.token == '':
            messagebox.showinfo('Токен не установлен', 'Установите значение поля "example_token" в файле конфигурации!')
            return
        self.githubAnalyzer = GitHubAnalyser(self.gitcli)
        self.draw(self.githubAnalyzer)

    def enter(self):
        self.ax.clear()
        self.gitcli = Gitcli(self.token_input.get(), self.user_input.get(), self.repo_input.get())
        if self.gitcli.token == '':
            messagebox.showinfo('Токен не установлен', 'Установите значение поля "Токен"!')
            return
        self.githubAnalyzer = GitHubAnalyser(self.gitcli)
        self.draw(self.githubAnalyzer)

    def draw(self, analyzer):
        g = analyzer.getGraph()
        g = analyzer.getMoreGraph(g)
        nx.draw(g, node_color=analyzer.color_map, with_labels=True, ax=self.ax)
        self.canvas.draw()

    def start(self):
        token_label = Label(master=self.input_frame, text="Токен", fg="#eee", bg="#333")
        token_label.pack(pady=5)
        self.token_input = Entry(master=self.input_frame, width=50)
        self.token_input.pack()

        user_label = Label(master=self.input_frame, text="Пользователь", fg="#eee", bg="#333")
        user_label.pack(pady=5)
        self.user_input = Entry(master=self.input_frame, width=50)
        self.user_input.pack()

        repo_label = Label(master=self.input_frame, text="Название репозитория", fg="#eee", bg="#333")
        repo_label.pack(pady=5)
        self.repo_input = Entry(master=self.input_frame, width=50)
        self.repo_input.pack()

        example_button = tk.Button(master=self.input_frame, text="Пример", command=self.example)
        example_button.pack(side=tk.LEFT, pady=5)
        enter_button = tk.Button(master=self.input_frame, text="Расчитать", command=self.enter)
        enter_button.pack(side=tk.RIGHT, pady=5)
        tk.mainloop()
