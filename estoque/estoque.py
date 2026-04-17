import tkinter as tk
from tkinter import messagebox
import json
import os
from utils import normalizar_codigo

ARQUIVO = "produtos.json"
ESTOQUE_MINIMO = 5
executando = False
# ===== CARREGAR PRODUTOS =====
def carregar_produtos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return {}

def salvar(produtos):
    with open(ARQUIVO, "w") as f:
        json.dump(produtos, f, indent=4)

# ===== BUSCAR CÓDIGO REAL (IGNORA ZERO À ESQUERDA) =====
def buscar_codigo_real(codigo_digitado, produtos):
    codigo_digitado = normalizar_codigo(codigo_digitado)

    for cod in produtos:
        if normalizar_codigo(cod) == codigo_digitado:
            return cod

    return None

# ===== TELA ESTOQUE =====
def abrir_estoque():
    produtos = carregar_produtos()

    # 🔥 GARANTE QUE TODOS TENHAM QTD
    for codigo in produtos:
        if "qtd" not in produtos[codigo]:
            produtos[codigo]["qtd"] = 0

    janela = tk.Toplevel()
    janela.title("Estoque")
    janela.geometry("700x500")

    # ===== LISTA =====
    lista = tk.Listbox(janela, width=80)
    lista.pack(pady=10, fill="both", expand=True)

    def verificar_estoque_baixo():
        baixos = []

        for codigo, p in produtos.items():
            if p.get("qtd", 0) <= ESTOQUE_MINIMO:
                baixos.append(f"{codigo} - {p['nome']} (Qtd: {p.get('qtd', 0)})")

        if baixos:
            mensagem = "⚠️ Estoque baixo:\n\n" + "\n".join(baixos)
            messagebox.showwarning("Atenção", mensagem)

    def atualizar_lista():
        lista.delete(0, tk.END)

        for codigo in sorted(produtos.keys()):
            p = produtos[codigo]

            alerta = "⚠️ " if p.get("qtd", 0) <= ESTOQUE_MINIMO else ""

            texto = f"{alerta}{codigo} - {p['nome']} | Qtd: {p['qtd']} | R$ {p['preco']:.2f}"
            lista.insert(tk.END, texto.replace(".", ","))

    atualizar_lista()
    atualizar_lista()
    verificar_estoque_baixo()

    # ===== FRAME CONTROLE =====
    frame = tk.Frame(janela)
    frame.pack(pady=10)

    tk.Label(frame, text="Código").grid(row=0, column=0, padx=5)
    entry_codigo = tk.Entry(frame, width=10)
    entry_codigo.grid(row=1, column=0, padx=5)

    tk.Label(frame, text="Quantidade").grid(row=0, column=1, padx=5)
    entry_qtd = tk.Entry(frame, width=10)
    entry_qtd.grid(row=1, column=1, padx=5)

    # ===== ADICIONAR ESTOQUE =====
    def adicionar():
        global executando

        if executando:
            return

        executando = True

        codigo_digitado = entry_codigo.get().strip()
        codigo_real = buscar_codigo_real(codigo_digitado, produtos)

        if not codigo_real:
            messagebox.showerror("Erro", "Produto não encontrado!")
            executando = False
            return

        try:
            qtd = int(entry_qtd.get().strip())
        except:
            messagebox.showerror("Erro", "Quantidade inválida!")
            executando = False
            return

        produto = produtos[codigo_real]

        resposta = messagebox.askyesno(
            "Confirmar",
            f"Deseja adicionar?\n\n"
            f"{codigo_real} - {produto['nome']}\n"
            f"Quantidade: {qtd}"
        )

        if not resposta:
            executando = False
            return

        produtos[codigo_real]["qtd"] += qtd
        salvar(produtos)

        atualizar_lista()

        entry_codigo.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)
        entry_codigo.focus_set()

        executando = False

    # ===== REMOVER ESTOQUE =====
    def remover():
        global executando

        if executando:
            return

        executando = True

        codigo_digitado = entry_codigo.get().strip()
        codigo_real = buscar_codigo_real(codigo_digitado, produtos)

        if not codigo_real:
            messagebox.showerror("Erro", "Produto não encontrado!")
            executando = False
            return

        try:
            qtd = int(entry_qtd.get().strip())
        except:
            messagebox.showerror("Erro", "Quantidade inválida!")
            executando = False
            return

        if produtos[codigo_real]["qtd"] < qtd:
            messagebox.showerror("Erro", "Estoque insuficiente!")
            executando = False
            return

        produto = produtos[codigo_real]

        resposta = messagebox.askyesno(
            "Confirmar",
            f"Deseja remover?\n\n"
            f"{codigo_real} - {produto['nome']}\n"
            f"Quantidade: {qtd}"
        )

        if not resposta:
            executando = False
            return

        produtos[codigo_real]["qtd"] -= qtd
        salvar(produtos)

        atualizar_lista()

        entry_codigo.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)
        entry_codigo.focus_set()

        executando = False

    # ===== BOTÕES =====
    tk.Button(frame, text="Adicionar", command=adicionar).grid(row=1, column=2, padx=5)
    tk.Button(frame, text="Remover", command=remover).grid(row=1, column=3, padx=5)

    # ===== ENTER =====
    def enter_codigo(event):
        entry_qtd.focus()

    def enter_qtd(event):
        adicionar()
        return "break"

    def enter_remover(event):
        remover()
        return "break"

    entry_codigo.bind("<Return>", enter_codigo)
    entry_qtd.bind("<Return>", enter_qtd)

    entry_codigo.focus()