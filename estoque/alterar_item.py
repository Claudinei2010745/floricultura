import tkinter as tk
from tkinter import messagebox
import json
import os

ARQUIVO = "produtos.json"

# ===== CARREGAR =====
if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r") as f:
        produtos = json.load(f)
else:
    produtos = {}

def salvar():
    with open(ARQUIVO, "w") as f:
        json.dump(produtos, f, indent=4)

def abrir_alterar_item():
    janela = tk.Toplevel()
    janela.title("Alterar Produto")
    janela.geometry("400x400")

    # ===== FUNÇÃO BUSCAR =====
    def buscar():
        codigo = entry_busca.get()

        if codigo not in produtos:
            messagebox.showerror("Erro", "Produto não encontrado!")
            return

        dados = produtos[codigo]

        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, codigo)

        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, dados["nome"])

        entry_preco.delete(0, tk.END)
        entry_preco.insert(0, str(dados["preco"]).replace(".", ","))

    # ===== FUNÇÃO SALVAR ALTERAÇÃO =====
    def salvar_alteracao():
        codigo_antigo = entry_busca.get()
        novo_codigo = entry_codigo.get()
        nome = entry_nome.get()
        preco = entry_preco.get()

        if novo_codigo == "" or nome == "" or preco == "":
            return

        try:
            preco = float(preco.replace(",", "."))
        except:
            messagebox.showerror("Erro", "Preço inválido!")
            return

        # se mudou o código
        if novo_codigo != codigo_antigo:
            if novo_codigo in produtos:
                messagebox.showerror("Erro", "Novo código já existe!")
                return

            del produtos[codigo_antigo]

        produtos[novo_codigo] = {
            "nome": nome,
            "preco": preco
        }

        salvar()
        atualizar_lista()

        messagebox.showinfo("Sucesso", "Produto atualizado!")

    # ===== ATUALIZAR LISTA =====
    def atualizar_lista():
        lista.delete(0, tk.END)

        for codigo in sorted(produtos.keys()):
            dados = produtos[codigo]
            texto = f"{codigo} - {dados['nome']} - R$ {dados['preco']:.2f}".replace(".", ",")
            lista.insert(tk.END, texto)

    # ===== BUSCA =====
    tk.Label(janela, text="Digite o código").pack()
    entry_busca = tk.Entry(janela)
    entry_busca.pack()

    tk.Button(janela, text="Buscar", command=buscar).pack(pady=5)

    # ===== CAMPOS =====
    tk.Label(janela, text="Novo Código").pack()
    entry_codigo = tk.Entry(janela)
    entry_codigo.pack()

    tk.Label(janela, text="Nome").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Preço").pack()
    entry_preco = tk.Entry(janela)
    entry_preco.pack()

    tk.Button(janela, text="Salvar Alteração", command=salvar_alteracao).pack(pady=10)

    # ===== LISTA =====
    lista = tk.Listbox(janela, width=40)
    lista.pack(pady=10)

    atualizar_lista()

    entry_busca.focus()