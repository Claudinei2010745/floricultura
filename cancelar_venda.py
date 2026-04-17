import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
from utils import normalizar_codigo

ARQUIVO_VENDAS = "vendas.json"
ARQUIVO_PRODUTOS = "produtos.json"


# ===== CARREGAR =====
def carregar_vendas():
    if os.path.exists(ARQUIVO_VENDAS):
        try:
            with open(ARQUIVO_VENDAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def carregar_produtos():
    if os.path.exists(ARQUIVO_PRODUTOS):
        with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def salvar_vendas(vendas):
    with open(ARQUIVO_VENDAS, "w", encoding="utf-8") as f:
        json.dump(vendas, f, indent=4, ensure_ascii=False)


def salvar_produtos(produtos):
    with open(ARQUIVO_PRODUTOS, "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)


# ===== TELA =====
def abrir_cancelar_venda():

    vendas = carregar_vendas()
    produtos = carregar_produtos()

    janela = tk.Toplevel()
    janela.title("Cancelar Venda")
    janela.geometry("700x500")

    tk.Label(janela, text="Data (dd/mm/aaaa)").pack()

    entry_data = tk.Entry(janela)
    entry_data.pack()

    lista = tk.Listbox(janela, width=100)
    lista.pack(fill="both", expand=True, pady=10)

    detalhes = tk.Text(janela, height=10)
    detalhes.pack(fill="x", padx=10, pady=5)

    vendas_filtradas = []

    # ===== BUSCAR =====
    def buscar():

        lista.delete(0, tk.END)
        detalhes.delete("1.0", tk.END)
        vendas_filtradas.clear()

        data = entry_data.get().strip()

        try:
            data_digitada = datetime.strptime(data, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Erro", "Use dd/mm/aaaa")
            return

        for i, venda in enumerate(vendas):

            data_venda = datetime.strptime(venda["data"], "%d/%m/%Y %H:%M").date()

            if data_venda == data_digitada:

                vendas_filtradas.append((i, venda))

                status = venda.get("status", "ATIVA")

                lista.insert(
                    tk.END,
                    f"{venda['data']} - R${venda['total']} - {status}"
                )

    # ===== MOSTRAR DETALHES =====
    def mostrar_detalhes(event):

        selecionado = lista.curselection()

        if not selecionado:
            return

        index = selecionado[0]

        if index >= len(vendas_filtradas):
            return

        i_venda, venda = vendas_filtradas[index]

        detalhes.delete("1.0", tk.END)

        status = venda.get("status", "ATIVA")

        detalhes.insert(tk.END, f"DATA: {venda['data']}\n")
        detalhes.insert(tk.END, f"STATUS: {status}\n")
        detalhes.insert(tk.END, "-" * 40 + "\n\n")

        for cod, item in venda["itens"].items():
            subtotal = item["preco"] * item["qtd"]

            detalhes.insert(
                tk.END,
                f"{item['nome']} | Qtd: {item['qtd']} | R$ {subtotal:.2f}\n"
            )

        detalhes.insert(tk.END, f"\nTOTAL: R$ {venda['total']:.2f}")

    # ===== CANCELAR =====
    def cancelar():

        selecionado = lista.curselection()

        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma venda!")
            return

        index = selecionado[0]

        if index >= len(vendas_filtradas):
            messagebox.showerror("Erro", "Seleção inválida!")
            return

        i_venda, venda = vendas_filtradas[index]

        if venda.get("status") == "CANCELADA":
            messagebox.showwarning("Aviso", "Essa venda já foi cancelada!")
            return

        resposta = messagebox.askyesno(
            "Confirmar Cancelamento",
            "Deseja realmente cancelar essa venda?"
        )

        if not resposta:
            return

        # ===== CANCELAR =====
        vendas[i_venda]["status"] = "CANCELADA"
        vendas[i_venda]["motivo_cancelamento"] = "Cancelada pelo usuário"

        # ===== DEVOLVER ESTOQUE =====
        for cod, item in venda["itens"].items():
            cod = normalizar_codigo(cod)

            for p_cod in produtos:
                if normalizar_codigo(p_cod) == cod:
                    produtos[p_cod]["qtd"] += item["qtd"]

        salvar_vendas(vendas)
        salvar_produtos(produtos)

        messagebox.showinfo("Sucesso", "Venda cancelada!")

        buscar()

    # ===== EVENTOS =====
    lista.bind("<<ListboxSelect>>", mostrar_detalhes)

    # ===== BOTÕES =====
    tk.Button(janela, text="Buscar", command=buscar).pack(pady=5)
    tk.Button(janela, text="Cancelar Venda", command=cancelar).pack(pady=5)

    entry_data.focus()