import tkinter as tk
from tkinter import messagebox
import json
import os

ARQUIVO = "dados/produtos.json"

# ===== CARREGAR PRODUTOS =====

def normalizar_codigo(codigo):
    return str(int(codigo)) if codigo.isdigit() else codigo

if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r") as f:
        produtos = json.load(f)
else:
    produtos = {}

def salvar():
    with open(ARQUIVO, "w") as f:
        json.dump(produtos, f, indent=4)

def abrir_tela_adicionar_item():

    janela = tk.Toplevel()
    janela.title("Adicionar Produto")
    janela.geometry("500x450")

    # ===== CAMPOS =====
    tk.Label(janela, text="Código").pack()
    entry_codigo = tk.Entry(janela)
    entry_codigo.pack()

    tk.Label(janela, text="Nome").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Preço").pack()
    entry_preco = tk.Entry(janela)
    entry_preco.pack()

    tk.Label(janela, text="Custo").pack()
    entry_custo = tk.Entry(janela)
    entry_custo.pack()

    tk.Label(janela, text="Quantidade").pack()
    entry_qtd = tk.Entry(janela)
    entry_qtd.pack()

    lista = tk.Listbox(janela, width=60)
    lista.pack(pady=10)

    # ===== CADASTRAR =====
    def cadastrar():
        codigo = entry_codigo.get().strip()
        nome = entry_nome.get().strip()
        preco = entry_preco.get().strip()
        custo = entry_custo.get().strip()
        qtd = entry_qtd.get().strip()

        # 🔥 VALIDAÇÃO
        if not codigo or not nome or not preco or not custo or not qtd:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            preco = float(preco.replace(",", "."))
            custo = float(custo.replace(",", "."))
            qtd = int(qtd)
        except:
            messagebox.showerror("Erro", "Valores inválidos!")
            return

        # 🔥 VERIFICA DUPLICIDADE (ignorando zeros)
        codigo_real = buscar_codigo_real(codigo)

        if codigo_real:
            messagebox.showerror("Erro", f"Código já cadastrado! ({codigo_real})")
            entry_codigo.focus_set()
            return

        # 🔥 SALVA O PRODUTO
        produtos[codigo] = {
            "nome": nome,
            "preco": preco,
            "custo": custo,
            "qtd": qtd
        }

        salvar()

        # 🔥 MOSTRA NA LISTA
        lista.insert(
            tk.END,
            f"{codigo} - {nome} | Qtd: {qtd} | R$ {preco:.2f}".replace(".", ",")
        )

        # 🧹 LIMPAR CAMPOS (AGORA SIM, NO FINAL)
        entry_codigo.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_custo.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)

        entry_codigo.focus_set()

    def atualizar_lista_nome(event):
        texto = entry_nome.get().lower().strip()

        lista.delete(0, tk.END)

        if texto == "":
            return

        for codigo, dados in produtos.items():
            nome = dados["nome"].lower()

            if texto in nome:
                item = f"{codigo} - {dados['nome']} | Qtd: {dados.get('qtd', 0)}"
                lista.insert(tk.END, item)

    # 🧹 LIMPAR CAMPOS
    entry_codigo.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_nome.bind("<KeyRelease>", atualizar_lista_nome)
    entry_preco.delete(0, tk.END)
    entry_custo.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)




    # ===== ENTER FUNCIONANDO =====

    def buscar_codigo_real(codigo_digitado):
        codigo_digitado = normalizar_codigo(codigo_digitado)

        for cod in produtos:
            if normalizar_codigo(cod) == codigo_digitado:
                return cod  # 🔥 retorna o código ORIGINAL (ex: "010")

        return None

    def enter_codigo(event):
        codigo_digitado = entry_codigo.get().strip()

        codigo_real = buscar_codigo_real(codigo_digitado)

        if codigo_real:
            messagebox.showerror("Erro", f"Código já cadastrado! ({codigo_real})")
            entry_codigo.focus_set()
            return "break"

        entry_nome.focus_set()


    def enter_nome(event):
        entry_preco.focus()

    def enter_preco(event):
        entry_custo.focus()

    def enter_custo(event):
        entry_qtd.focus()

    def enter_qtd(event):
        cadastrar()

    # ===== BINDS =====
    entry_codigo.bind("<Return>", enter_codigo)
    entry_nome.bind("<Return>", enter_nome)
    entry_nome.bind("<KeyRelease>", atualizar_lista_nome)
    entry_preco.bind("<Return>", enter_preco)
    entry_custo.bind("<Return>", enter_custo)
    entry_qtd.bind("<Return>", enter_qtd)

    # ===== BOTÃO =====
    tk.Button(janela, text="Cadastrar", command=cadastrar).pack(pady=10)

    entry_codigo.focus()
