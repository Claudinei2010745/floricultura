import tkinter as tk
import json
import os
from tkinter import messagebox
from datetime import datetime

ARQUIVO = "dados/produtos.json"

# ===== CARREGAR PRODUTOS =====
if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r") as f:
        produtos = json.load(f)
else:
    produtos = {}

def abrir_tela_vendas():
    VENDAS_ARQUIVO = "dados/vendas.json"
    venda = {}

    janela = tk.Toplevel()
    janela.title("Tela de Vendas")
    janela.geometry("600x500")
    janela.transient()
    janela.grab_set()
    janela.focus_force()

    total = 0
    produto_selecionado = None  # ✔ CONTROLE SIMPLES

    # ===== BUSCA CÓDIGO =====
    def normalizar_codigo(codigo):
        return str(int(codigo))

    def buscar_codigo(codigo_digitado):
        codigo_digitado = normalizar_codigo(codigo_digitado)

        for codigo in produtos:
            if normalizar_codigo(codigo) == codigo_digitado:
                return codigo

        return None

    # ===== ADICIONAR PRODUTO =====
    def adicionar_por_codigo(codigo):
        nonlocal total, produto_selecionado

        # ✔ BLOQUEIO PRINCIPAL
        if codigo not in produtos:
            messagebox.showwarning("Atenção", "Selecione um produto primeiro!")
            return

        produto_selecionado = codigo

        produto = produtos[codigo]

        qtd_texto = entry_qtd.get()

        if qtd_texto == "":
            qtd = 1
        else:
            try:
                qtd = int(qtd_texto)
            except:
                messagebox.showerror("Erro", "Quantidade inválida!")
                return

        resposta = messagebox.askyesno(
            "Confirmar",
            f"Deseja adicionar?\n\n{codigo} - {produto['nome']}\nQtd: {qtd}\nValor unitário: R$ {produto['preco']:.2f}".replace(".", ",")
        )

        if not resposta:
            return

        if codigo in venda:
            venda[codigo]["qtd"] += qtd
        else:
            venda[codigo] = {
                "nome": produto["nome"],
                "preco": produto["preco"],
                "qtd": qtd
            }

        atualizar_lista_venda()

        entry_busca.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)
        entry_busca.focus()

    # ===== LISTA VENDA =====
    def atualizar_lista_venda():
        nonlocal total

        lista_venda.delete(0, tk.END)
        total = 0

        for codigo in venda:
            item = venda[codigo]
            subtotal = item["preco"] * item["qtd"]

            texto = f"{codigo} - {item['nome']} | Qtd: {item['qtd']} | R$ {subtotal:.2f}".replace(".", ",")
            lista_venda.insert(tk.END, texto)

            total += subtotal

        label_total.config(text=f"Total: R$ {total:.2f}".replace(".", ","))

    # ===== BUSCA =====
    def atualizar_lista(event):
        if event.keysym == "Return":
            return

        texto = entry_busca.get().lower()

        lista_produtos.delete(0, tk.END)

        for codigo in sorted(produtos.keys()):
            dados = produtos[codigo]
            nome = dados["nome"].lower()

            if texto in codigo.lower() or texto in nome:
                item = f"{codigo} - {dados['nome']} - R$ {dados['preco']:.2f}".replace(".", ",")
                lista_produtos.insert(tk.END, item)

    # ===== SELECIONAR PRODUTO =====
    def adicionar_item(event):
        selecionado = lista_produtos.get(tk.ACTIVE)

        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto primeiro!")
            return

        codigo = selecionado.split(" - ")[0]
        adicionar_por_codigo(codigo)

    def verificar_codigo():
        codigo_digitado = entry_busca.get().strip()

        codigo_encontrado = buscar_codigo(codigo_digitado)

        if codigo_encontrado:
            adicionar_por_codigo(codigo_encontrado)
        else:
            messagebox.showerror("Erro", "Produto não encontrado!")

    def enter_pressionado(event):
        verificar_codigo()
        return "break"

    # ===== FINALIZAR VENDA =====
    def finalizar_venda():
        nonlocal produto_selecionado

        if not venda:
            messagebox.showwarning("Aviso", "Nenhum item na venda!")
            return

        if not messagebox.askyesno("Finalizar", "Deseja finalizar a venda?"):
            return

        if os.path.exists(VENDAS_ARQUIVO):
            with open(VENDAS_ARQUIVO, "r") as f:
                vendas = json.load(f)
        else:
            vendas = []

        nova_venda = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "itens": venda,
            "total": total
        }

        vendas.append(nova_venda)

        with open(VENDAS_ARQUIVO, "w") as f:
            json.dump(vendas, f, indent=4)

        venda.clear()
        produto_selecionado = None

        atualizar_lista_venda()

        lista_produtos.delete(0, tk.END)
        entry_busca.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)

        messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")

    # ===== INTERFACE =====
    frame_busca = tk.Frame(janela)
    frame_busca.pack(pady=10)

    tk.Label(frame_busca, text="Produto").grid(row=0, column=0)
    entry_busca = tk.Entry(frame_busca, width=25)
    entry_busca.grid(row=1, column=0)

    tk.Label(frame_busca, text="Qtd").grid(row=0, column=1)
    entry_qtd = tk.Entry(frame_busca, width=5)
    entry_qtd.grid(row=1, column=1)

    entry_busca.bind("<Return>", enter_pressionado)
    entry_qtd.bind("<Return>", enter_pressionado)
    entry_busca.bind("<KeyRelease>", atualizar_lista)

    lista_produtos = tk.Listbox(janela, width=50, height=8)
    lista_produtos.pack(pady=10)

    lista_produtos.bind("<Double-Button-1>", adicionar_item)

    tk.Label(janela, text="Itens da venda").pack()

    lista_venda = tk.Listbox(janela, width=50)
    lista_venda.pack(pady=10)

    label_total = tk.Label(janela, text="Total: R$ 0,00", font=("Arial", 12, "bold"))
    label_total.pack(pady=10)

    tk.Button(
        janela,
        text="Finalizar Venda",
        bg="green",
        fg="white",
        width=20,
        height=2,
        command=finalizar_venda
    ).pack(pady=10)
