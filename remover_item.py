import tkinter as tk
from tkinter import messagebox
import json
import os

ARQUIVO = "produtos.json"

# ===== CARREGAR DADOS =====
if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r") as f:
        produtos = json.load(f)
else:
    produtos = {}

def salvar():
    with open(ARQUIVO, "w") as f:
        json.dump(produtos, f, indent=4)

def abrir_remover_item():
    janela = tk.Toplevel()
    janela.title("Remover Item")
    janela.geometry("400x400")

    # ===== FUNÇÃO REMOVER =====
    def remover():
        codigo = entry_codigo.get()

        if codigo == "":
            return

        if codigo not in produtos:
            messagebox.showerror("Erro", "Código não encontrado!")
            return

        # confirmação
        resposta = messagebox.askyesno("Confirmar", "Deseja remover este item?")

        if resposta:
            del produtos[codigo]
            salvar()

            atualizar_lista()

            entry_codigo.delete(0, tk.END)
            entry_codigo.focus()

    # ===== ATUALIZAR LISTA =====
    def atualizar_lista():
        lista.delete(0, tk.END)

        for codigo in sorted(produtos.keys()):
            dados = produtos[codigo]
            texto = f"{codigo} - {dados['nome']} - R$ {dados['preco']:.2f}".replace(".", ",")
            lista.insert(tk.END, texto)

    # ===== CAMPO =====
    tk.Label(janela, text="Código do produto").pack()
    entry_codigo = tk.Entry(janela)
    entry_codigo.pack()

    tk.Button(janela, text="Remover", command=remover).pack(pady=10)

    # ===== LISTA =====
    lista = tk.Listbox(janela, width=55)
    lista.pack(pady=10)

    atualizar_lista()

    entry_codigo.focus()