import tkinter as tk
from tkinter import ttk, messagebox
import requests

class ConcessionariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Concessionária")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.root.maxsize(1200, 900)
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), padding=5)
        self.style.configure('TLabel', font=('Helvetica', 12), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 12), padding=5)
        self.style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'), padding=10)
        self.style.configure('Info.TLabel', font=('Helvetica', 14), padding=5)
        self.style.configure('Accent.TButton', font=('Helvetica', 12, 'bold'), padding=10, foreground='black', background='#4CAF50')
        self.style.map('Accent.TButton', foreground=[('active', 'black')], background=[('active', '#45a049')])
        self.style.configure('Warning.TLabel', foreground='red')

        self.create_choice_widgets()

    def create_choice_widgets(self):
        self.clear_widgets()

        title_label = ttk.Label(self.root, text="Escolha seu perfil:", style='Title.TLabel')
        title_label.pack(pady=20)

        comprador_button = ttk.Button(self.root, text="Comprador", style='Accent.TButton', command=self.create_comprador_widgets)
        comprador_button.pack(pady=10)

        vendedor_button = ttk.Button(self.root, text="Vendedor", style='Accent.TButton', command=self.create_vendedor_widgets)
        vendedor_button.pack(pady=10)

    def create_comprador_widgets(self):
        self.clear_widgets()

        title_label = ttk.Label(self.root, text="Comprador", style='Title.TLabel')
        title_label.pack(pady=20)

        carros_frame = ttk.Frame(self.root)
        carros_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        carros_label = ttk.Label(carros_frame, text="Lista de Carros Disponíveis:", style='Info.TLabel')
        carros_label.pack(pady=5)

        scrollbar = ttk.Scrollbar(carros_frame, orient=tk.VERTICAL)
        self.carros_listbox = tk.Listbox(carros_frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.carros_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.carros_listbox.pack(fill=tk.BOTH, expand=True)

        cliente_frame = ttk.Frame(self.root)
        cliente_frame.pack(pady=10)

        cliente_nome_label = ttk.Label(cliente_frame, text="Nome do Cliente:", style='Info.TLabel')
        cliente_nome_label.grid(row=0, column=0, padx=5)

        self.cliente_nome_entry = ttk.Entry(cliente_frame)
        self.cliente_nome_entry.grid(row=0, column=1, padx=5)

        registrar_venda_button = ttk.Button(cliente_frame, text="Registrar Venda", style='Accent.TButton', command=self.registrar_venda)
        registrar_venda_button.grid(row=0, column=2, padx=5)

        voltar_button = ttk.Button(cliente_frame, text="Voltar", style='Accent.TButton', command=self.create_choice_widgets)
        voltar_button.grid(row=0, column=3, padx=5)

        self.listar_carros()

    def create_vendedor_widgets(self):
        self.clear_widgets()

        title_label = ttk.Label(self.root, text="Vendedor", style='Title.TLabel')
        title_label.pack(pady=20)

        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=10)

        ttk.Label(info_frame, text="Preencha as informações do carro:", style='Info.TLabel').grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(info_frame, text="Marca:", style='Info.TLabel').grid(row=1, column=0, pady=5)
        self.marca_entry = ttk.Entry(info_frame)
        self.marca_entry.grid(row=1, column=1, pady=5)

        ttk.Label(info_frame, text="Modelo:", style='Info.TLabel').grid(row=2, column=0, pady=5)
        self.modelo_entry = ttk.Entry(info_frame)
        self.modelo_entry.grid(row=2, column=1, pady=5)

        ttk.Label(info_frame, text="Ano:", style='Info.TLabel').grid(row=3, column=0, pady=5)
        self.ano_entry = ttk.Entry(info_frame)
        self.ano_entry.grid(row=3, column=1, pady=5)

        ttk.Label(info_frame, text="Preço:", style='Info.TLabel').grid(row=4, column=0, pady=5)
        self.preco_entry = ttk.Entry(info_frame)
        self.preco_entry.grid(row=4, column=1, pady=5)

        ttk.Label(info_frame, text="Cor:", style='Info.TLabel').grid(row=5, column=0, pady=5)
        self.cor_entry = ttk.Entry(info_frame)
        self.cor_entry.grid(row=5, column=1, pady=5)

        vendedor_button = ttk.Button(info_frame, text="Cadastrar Carro", style='Accent.TButton', command=self.cadastrar_carro)
        vendedor_button.grid(row=6, column=0, columnspan=2, pady=10)

        voltar_button = ttk.Button(info_frame, text="Voltar", style='Accent.TButton', command=self.create_choice_widgets)
        voltar_button.grid(row=7, column=0, columnspan=2, pady=10)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def listar_carros(self):
        response = requests.get("http://localhost:8000/carros/")
        if response.status_code == 200:
            carros = response.json()
            for carro in carros:
                self.carros_listbox.insert(tk.END, f"{carro['id']} - {carro['marca']} {carro['modelo']} ({carro['ano']}) - {carro['cor']} - R${carro['preco']}")
        else:
            messagebox.showerror("Erro", "Não foi possível listar os carros")

    def registrar_venda(self):
        selected_car = self.carros_listbox.get(tk.ACTIVE)
        if not selected_car:
            messagebox.showwarning("Atenção", "Selecione um carro")
            return

        carro_id = selected_car.split(' - ')[0]
        cliente_nome = self.cliente_nome_entry.get()
        if not cliente_nome:
            messagebox.showwarning("Atenção", "Insira o nome do cliente")
            return

        data = {'carro_id': carro_id, 'cliente_nome': cliente_nome}
        response = requests.post("http://localhost:8000/registrar_venda/", data=data)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso")
        else:
            messagebox.showerror("Erro", "Não foi possível registrar a venda")

    def cadastrar_carro(self):
        marca = self.marca_entry.get()
        modelo = self.modelo_entry.get()
        ano = self.ano_entry.get()
        preco = self.preco_entry.get()
        cor = self.cor_entry.get()

        if not marca or not modelo or not ano or not preco or not cor:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        data = {'marca': marca, 'modelo': modelo, 'ano': ano, 'preco': preco, 'cor': cor}
        response = requests.post("http://localhost:8000/cadastrar_carro/", data=data)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Carro cadastrado com sucesso")
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar o carro")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConcessionariaApp(root)
    root.mainloop()
