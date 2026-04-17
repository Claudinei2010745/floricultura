import tkinter as tk
from PIL import Image, ImageTk



from tela_vendas import abrir_tela_vendas
from custos import abrir_tela_custos
from estoque import abrir_estoque
from adicionar_item import abrir_tela_adicionar_item
from remover_item import abrir_remover_item
from relatorio_mensal import abrir_relatorio_mensal
from cancelar_venda import abrir_cancelar_venda
from alterar_item import abrir_alterar_item
from relatorio_diario import abrir_relatorio_diario

janela = tk.Tk()
# janela.title("Menu Vendas")
# janela.geometry("600x400")
janela.configure(bg="#FFC0CB")

img = Image.open("flor.png")   # abre imagem (PIL)
img = img.resize((250, 250))   # redimensiona aqui

img_tk = ImageTk.PhotoImage(img)  # só depois converte

# título
# título
titulo = tk.Label(janela, text="IMPÉRIO DAS PLANTAS", font=("Arial", 18), fg="green")
titulo.pack(pady=(10, 0))

# subtítulo
subtitulo = tk.Label(janela, text="MENU DE VENDAS", font=("Arial", 14), fg="green")
subtitulo.pack(pady=(0, 15))

# caixa branca
frame = tk.Frame(janela, bg="white", bd=2, relief="ridge")
frame.pack(padx=20, pady=10, fill="both", expand=True)

# ===== FUNÇÕES =====

def relatorio_diario():
    print("Relatório Diário")

def estoque():
    print("Estoque")

def adicionar_item():
    print("Adicionar Item")

def remover_item():
    print("Remover Item")

def relatorio_mensal():
    print("Relatório Mensal")

# ===== BOTÕES =====
btn_vendas = tk.Button(frame, text="Tela de Vendas", width=20, height=2, command=abrir_tela_vendas)
btn_rel_dia = tk.Button(frame, text="Relatório Diário", width=20, height=2, command=abrir_relatorio_diario)

btn_estoque = tk.Button(frame, text="Estoque", width=20, height=2, command=abrir_estoque)
btn_add = tk.Button(frame, text="Adicionar Item", width=20, height=2, command=abrir_tela_adicionar_item)

btn_remove = tk.Button(frame, text="Remover Item", width=20, height=2, command=abrir_remover_item)
btn_rel_mes = tk.Button(frame, text="Relatório Mensal", width=20, height=2, command=abrir_relatorio_mensal)

btn_custos = tk.Button(frame, text="Custos", width=20, height=2, command=abrir_tela_custos)
btn_cancelar = tk.Button(frame,text="Cancelar Venda",width=20,height=2,command=abrir_cancelar_venda)

btn_alterar = tk.Button(frame, text="Alterar Produto", width=20, height=2, command=abrir_alterar_item)

# ===== ORGANIZAÇÃO EM GRADE =====
btn_vendas.grid(row=0, column=0, padx=10, pady=10)
btn_rel_dia.grid(row=0, column=1, padx=10, pady=10)

btn_estoque.grid(row=1, column=0, padx=10, pady=10)
btn_add.grid(row=1, column=1, padx=10, pady=10)

btn_remove.grid(row=2, column=0, padx=10, pady=10)
btn_rel_mes.grid(row=2, column=1, padx=10, pady=10)

btn_custos.grid(row=3, column=0, padx=10, pady=10)
btn_cancelar.grid(row=3, column=1, padx=10, pady=10)

btn_alterar.grid(row=4, column=0, padx=10, pady=10)
label_img = tk.Label(frame, image=img_tk, bg="white")
label_img.image = img_tk
label_img.grid(row=0, column=2, rowspan=5, padx=20, pady=10)

# janela = tk.Tk()
janela.geometry("700x450")

canvas = tk.Canvas(janela, width=600, height=400)
canvas.pack(fill="both", expand=True)

janela.mainloop()