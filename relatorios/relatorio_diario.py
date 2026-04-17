import tkinter as tk
import json
import os
from datetime import datetime

VENDAS_ARQUIVO = "dados/vendas.json"

def abrir_relatorio_diario():

    janela = tk.Toplevel()
    janela.title("Relatório Diário")
    janela.geometry("600x500")

    hoje = datetime.now().strftime("%d/%m/%Y")

    frame_lista = tk.Frame(janela)
    frame_lista.pack(fill="both", expand=True, padx=(20, 10), pady=10)

    scrollbar = tk.Scrollbar(frame_lista)
    scrollbar.pack(side="right", fill="y")

    lista = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set)
    lista.pack(side="left", fill="both", expand=True, padx=(5, 0))
    lista.config(font=("Consolas", 10))


    scrollbar.config(command=lista.yview)

    total_dia = 0
    qtd_vendas = 0

    if os.path.exists(VENDAS_ARQUIVO):
        with open(VENDAS_ARQUIVO, "r") as f:
            vendas = json.load(f)
    else:
        vendas = []

    for venda in vendas:
        status = venda.get("status", "ATIVA")

        if hoje in venda["data"]:

            qtd_vendas += 1
            total_dia += venda["total"]

            lista.insert(tk.END, f"Data: {venda['data']} - Total: R${venda['total']} - {status}")
            lista.insert(tk.END, "-" * 50)

            for codigo, item in venda["itens"].items():
                subtotal = item["preco"] * item["qtd"]

                texto_item = f"{codigo} - {item['nome']} | Qtd: {item['qtd']} | R$ {subtotal:.2f}".replace(".", ",")
                lista.insert(tk.END, texto_item)

            lista.insert(tk.END, f"Total da venda: R$ {venda['total']:.2f}".replace(".", ","))
            lista.insert(tk.END, "=" * 50)

            # 🔹 TOTAL DA VENDA
            lista.insert(tk.END, f" Total da venda: R$ {venda['total']:.2f}".replace(".", ","))
            lista.insert(tk.END, "=" * 50)

    label_total = tk.Label(janela, text=f"Total do dia: R$ {total_dia:.2f}".replace(".", ","), font=("Arial", 12, "bold"))
    label_total.pack(pady=5)

    label_qtd = tk.Label(janela, text=f"Quantidade de vendas: {qtd_vendas}")
    label_qtd.pack(pady=5)
