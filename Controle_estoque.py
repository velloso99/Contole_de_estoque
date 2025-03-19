from mold import*
from tkinter import filedialog

#Criando a janela
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("500x300")
root.configure(background=co0)
root.resizable(width=False, height=False)
root.overrideredirect(1)
largura_root = 500
altura_root = 300
#obter tamanho da tela
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
# Calcular posição para centralizar
pos_x = ( largura_tela-largura_root )//2
pos_y = (altura_tela - altura_root)//2
# Definir geometria da janela (LxA+X+Y)
root.geometry(f"{largura_root}x{altura_root}+{pos_x}+{pos_y}")

Style = Style(root)
Style.theme_use("clam")
Style.configure("green.Horizontal.TProgressbar", 
                foreground="green", 
                background="green")

#------------------------------------------------------------------------
frame_login = Frame(root, width=500, height=300, bg=co0)
frame_login.grid(row=0 , column=0, sticky=NSEW)
#-----------------------------------------------------------------------


def abrir_novo_usuario():
    for widget in frame_login.winfo_children():
        widget.destroy()
    novo_usuario()


#------------------------------------------------------------------------
def login():
    global root
    # Verificando login e abrir novo arquivo
    def verificar_login():
        
        global usuario, senha 
        
        usuario = e_user.get()
        senha = e_senha.get()
        
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute("SELECT*FROM login WHERE usuario=? AND senha=?", (usuario, senha))
        resultado = cursor.fetchall()
        if resultado:
            for i in range(101):  # De 0 a 100
                barra['value'] = i  # Atualiza a barra de progresso
                porcentagem_label.config(text=f"{i}%")  # Atualiza o texto da porcentagem
                root.update_idletasks()  # Atualiza a interface
                root.after(5)  # Tempo de espera (20ms)
            root.withdraw() 
            painel_geral()
            
        else:
            messagebox.showerror("Erro", "Usuario ou senha incorretos!")
        cursor.close()
        
    lbl_status = Label(frame_login, text="", font=('Ivy 15 bold'), bg=co0, fg=co1)
    lbl_status.place(x=325, y=220)

    l_titulo = Label(frame_login, text="Faça seu login", font=('Ivy 20 bold'), bg=co0, fg=co1)
    l_titulo.place(x=240, y=15, anchor=CENTER)

    l_user = Label(frame_login, text="Usuario", font=('Ivy 15 bold'), bg=co0, fg=co1)
    l_user.place(x=240, y=60, anchor=CENTER)
    e_user= Entry(frame_login, width=25, justify=LEFT, font=('Ivy 15 bold'),  relief='solid')
    e_user.place(x=250, y=100, anchor=CENTER)

    l_senha =Label(frame_login, text="Senha", font=('Ivy 15 bold'), bg=co0, fg=co1)
    l_senha.place(x=240, y=140, anchor=CENTER)
    e_senha= Entry(frame_login, width=25, justify=LEFT, font=('Ivy 15 bold'),show="*",  relief='solid')
    e_senha.place(x=250, y=180, anchor=CENTER)

    bt_enter = Button(frame_login, command=verificar_login, text="Enter", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_enter.place(x=45, y=225)

    bt_n_usuario = Button(frame_login, command=abrir_novo_usuario, text="Novo Usuario", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_n_usuario.place(x=110, y=225)
    
    bt_esqueceu = Button(frame_login, command=esqueceu_senha , text="Esqueceu a Senha", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_esqueceu.place(x=240, y=225)

    bt_n_fechar = Button(frame_login, command=root.destroy , text="Fechar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_n_fechar.place(x=410, y=225)
    
    barra = Progressbar(frame_login, length=250, mode="determinate",style="green.Horizontal.TProgressbar" )
    barra.place(x=170, y=275)
    porcentagem_label =Label(frame_login, text="0%", font=("Arial", 12) )
    porcentagem_label.place(x=120, y=275)
#***************************************************************************************************
def novo_usuario():
    
    frame_n_senha = Frame(root, width=500, height=300, bg=co0)
    frame_n_senha.grid(row=0, column=0, sticky=NSEW)
    
    def cadastrar_usuario():
        
        usuario = e_user.get().strip()
        senha = e_senha.get().strip()
    
        # Verifica se os campos estão preenchidos
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        # Verifica se o usuário já existe no banco
        if verificar_usuario(usuario):
            messagebox.showerror("Erro", "Usuário já cadastrado!")
            return
        for i in range(101):  # De 0 a 100
            barra['value'] = i  # Atualiza a barra de progresso
            porcentagem_label.config(text=f"{i}%")  # Atualiza o texto da porcentagem
            root.update_idletasks()  # Atualiza a interface
            root.after(5)  # Tempo de espera (20ms)
            
        root.destroy()
        #subprocess.run(["python", "login.py"])
        # Criar login no banco de dados
        criar_login((usuario, senha))  # Passando como tupla

        # Limpa os campos após o cadastro
        e_user.delete(0, END)
        e_senha.delete(0, END)
        
        
    barra = ttk.Progressbar(frame_n_senha, length=250, mode="determinate",style="green.Horizontal.TProgressbar")
    barra.place(x=170, y=275)
    porcentagem_label = tk.Label(frame_n_senha, text="0%")
    porcentagem_label.place(x=120, y=275)
    
    l_titulo = Label(frame_n_senha, text="Cadastrar um novo usuario", font=('Ivy 20 bold'), bg=co0, fg=co1)
    l_titulo.place(x=230, y=15, anchor=CENTER)
    
    l_user = Label(frame_n_senha, text="Usuario", font=('Ivy 15 bold'), bg=co0, fg=co1)
    l_user.place(x=240, y=60, anchor=CENTER)
    e_user= Entry(frame_n_senha, width=25, justify=LEFT, font=('Ivy 15 bold'),  relief='solid')
    e_user.place(x=250, y=100, anchor=CENTER)

    l_senha =Label(frame_n_senha, text="Senha", font=('Ivy 15 bold'), bg=co0, fg=co1)
    l_senha.place(x=240, y=140, anchor=CENTER)
    e_senha= Entry(frame_n_senha, width=25, justify=LEFT, font=('Ivy 15 bold'),show="*",  relief='solid')
    e_senha.place(x=250, y=180, anchor=CENTER)

    bt_enter = Button(frame_n_senha, command=cadastrar_usuario, text="Enter", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_enter.place(x=105, y=225)
    
    bt_fechar = Button(frame_n_senha, command=root.destroy, text="Atualizar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_fechar.place(x=200, y=225)
#***************************************************************************************************     
def esqueceu_senha():
    
    #Criar uma nova janela
    root1 = Toplevel(root) 
    root1.title("Atulizar Senha")
    root1.geometry("400x400")
    #root.overrideredirect(1)      
    largura_root1 = 400
    altura_root1 = 400
    #obter tamanho da tela
    largura_tela = root1.winfo_screenwidth()
    altura_tela = root1.winfo_screenheight()
    # Calcular posição para centralizar
    pos_x = ( largura_tela-largura_root1 )//2
    pos_y = (altura_tela - altura_root1)//2
    # Definir geometria da janela (LxA+X+Y)
    root1.geometry(f"{largura_root}x{altura_root1}+{pos_x}+{pos_y}")   
    
    frame_Login = Frame(root1, width=250, height=300, bg=co0)
    frame_Login.grid(row=0, column=2,padx=0, pady=30 ,sticky=W)

    frame_tabela = Frame(root1, width=250, height=310, bg=co0 )
    frame_tabela.grid(row=0, column=1, sticky=E)
    
    def update_login():
    
        try:
            tree_itens = tree_login.focus()
            tree_dicionario = tree_login.item(tree_itens)
            tree_lista = tree_dicionario['values']
        
            valor_id = tree_lista[0]
        
            e_user.delete(0, END)
            e_senha.delete(0, END)

            e_user.insert(0, tree_lista[1])
            e_senha.insert(0, tree_lista[2])
        
            def update():
            
                user = e_user.get().strip()
                senha = e_senha.get().strip()
            
                lista =[ user, senha, valor_id]
                
                #verificando caso algum campo esteja vazio
                for i in lista:
                    if i == '':
                        messagebox.showerror('Erro', 'Preencha todos os campos!')  
                        return
                atualizar_Login(lista)
                # Mostrando a mensagem de sucesso
                messagebox.showinfo('Sucesso', 'Os dados Atualizados com sucesso!' )    

                # Limpa os campos
                e_user.delete(0, END)
                e_senha.delete(0, END)

                # Chama a função que exibe os logins atualizados (se existir)
                mostrar_login()
                botao_update.destroy()
                
            botao_update = Button(frame_Login, command= update,  anchor=CENTER,text='Salvar e Atualizar'.upper(), width=18, overrelief=RIDGE, font=('Ivy 10'), bg=co3, fg=co1)
            botao_update.place(x=45, y=270) 
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um dos login na tabela')
    
    def del_usuario():
        try:
            tree_itens = tree_login.focus()
            tree_dicionario = tree_login.item(tree_itens)
            tree_lista = tree_dicionario['values']
            
            valor_id = tree_lista[0]
            
            # deletar dados no Banco de Dados
            deletar_usuario([valor_id])
            
            #Mostrando a menssagem de sucesso
            messagebox.showinfo('Sucesso', 'Usuario e senha deletado com sucesso!')
            
            #mostrando os valores na tabela
            mostrar_login()
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um dos usuarios na tabela')
            
    l_titulo = Label(root1, text="Atualizar Usuario e Senha", font=('Ivy 20 bold'), bg=co0, fg=co1)
    l_titulo.place(x=201, y=15, anchor=CENTER)
    
    # TRabalhando no frame logo

    l_user = Label(frame_Login, text="Usuario", font=('Ivy 15 bold'), bg=co0, fg=co1)
    l_user.place(x=130, y=15, anchor=CENTER)
    e_user= Entry(frame_Login, width=15, justify=LEFT, font=('Ivy 15 bold'),  relief='solid')
    e_user.place(x=130, y=50, anchor=CENTER)

    l_senha = Label(frame_Login, text="Senha", font=('Ivy 15 bold'), bg=co0, fg=co1)
    l_senha.place(x=130, y=85, anchor=CENTER)
    e_senha= Entry(frame_Login, width=15, justify=LEFT, font=('Ivy 15 bold'),show="*",  relief='solid')
    e_senha.place(x=130, y=120, anchor=CENTER)


    bt_enter = Button(frame_Login, command=update_login, text="Atualizar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_enter.place(x=85, y=145)

    #bt_voltar = Button(frame_Login, command=voltar_login, text="Voltar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    #bt_voltar.place(x=95, y=190)

    bt_excluir = Button(frame_Login, command=del_usuario, text="Deletar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_excluir.place(x=85, y=190)

    #bt_excluir.place(x=85, y=230)
    
    def mostrar_login():
        
        app_nome = Label(frame_tabela, text="Login", height=1, pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
        app_nome.grid(row=0, column=0, padx=0, pady=10, sticky=NSEW)

        # Definição do cabeçalho
        list_header = ['ID','Usuario' ]
    
        # Obtém os dados do estoque
        df_list = ver_login() # Certifique-se de que essa função retorna os dados corretamente
    
        global tree_login
    
        # Criando a Treeview
        tree_login = ttk.Treeview(frame_tabela, selectmode="extended", columns=list_header, show="headings")

        # Barras de rolagem
        vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree_login.yview)
        hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree_login.xview)  # Corrigido aqui

        tree_login.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
        # Posicionando os widgets
        tree_login.grid(column=0, row=1, sticky='nsew')
        vsb.grid(column=1, row=1, sticky='ns')
        hsb.grid(column=0, row=2, sticky='ew')
    
        frame_Login.grid_rowconfigure(0, weight=12)

        # Configuração das colunas
        hd = ["nw", "nw"]
        h = [40,100]
    
        for n, col in enumerate(list_header):
            tree_login.heading(col, text=col.title(), anchor=NW)
            tree_login.column(col, width=h[n], anchor=hd[n])

        # Inserindo os dados
        if df_list:
            for item in df_list:
                    tree_login.insert("", "end", values=item)

    mostrar_login()

    l_titulo = Label(root1, text="Selecione o usuario na tabela, \n após o usuario selecionado, \n  clique no botão atualizar", font=('Ivy 10 bold'), bg=co0, fg=co1)
    l_titulo.place(x=175, y=370, anchor=CENTER)
#***************************************************************************************************
def painel_geral():
    
    global root
    
    #Criar uma nova janela
    root = Toplevel(root) 
    root.title("Painel de Controle")
    root.geometry("900x900")
    root.configure(background=co0)
    root.resizable(width=False, height=False)
    largura_root = 900
    altura_root = 900
    #obter tamanho da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    # Calcular posição para centralizar
    pos_x = ( largura_tela-largura_root )//2
    pos_y = (altura_tela - altura_root)//2
    # Definir geometria da janela (LxA+X+Y)
    root.geometry(f"{largura_root}x{altura_root}+{pos_x}+{pos_y}")
    

    frame_painel = Frame(root, width=900, height=900, bg=co0)
    frame_painel.place(x=0, y=0)
    
    p_titulo = Label(frame_painel, text="Cadastro de Estoque ", font=('Ivy 20 bold'), bg=co0, fg=co1)
    p_titulo.place(x=450, y=400, anchor=CENTER)

    p_titulo = Label(frame_painel, text="Software destinado para  estoque.", font=('Ivy 10 '), bg=co0, fg=co1)
    p_titulo.place(x=450, y=500, anchor=CENTER)

    p_titulo = Label(frame_painel, text="Criado e desenvolvido por: VellosoDev. ", font=('Ivy 10 '), bg=co0, fg=co1)
    p_titulo.place(x=450, y=600, anchor=CENTER)
    
    bt_estoque = Button(frame_painel, command=estoque, text="Estoque", bd=3, bg=co6, fg=co1, font=('verdana', 11, 'bold'))
    bt_estoque.place(x=350, y=50)
    
    bt_fornecedor = Button(frame_painel, command=fornecedor, text="Fornecedor", bd=3, bg=co6, fg=co1, font=('verdana', 11, 'bold'))
    bt_fornecedor.place(x=240, y=50)
    
    bt_fechar = Button(frame_painel, command=root.destroy, text="Fechar", bd=3, bg=co6, fg=co1, font=('verdana', 11, 'bold'))
    bt_fechar.place(x=160, y=50)
                    
    bt_relatorio= Button(frame_painel, command=relatorio, text="Relatórios", bd=3, bg=co6, fg=co1, font=('verdana', 11, 'bold'))
    bt_relatorio.place(x=438, y=50)     
    
    bt_atualizacao= Button(frame_painel, command=atulizar, text="Atualização", bd=3, bg=co6, fg=co1, font=('verdana', 11, 'bold'))
    bt_atualizacao.place(x=538, y=50) 
#***************************************************************************************************
def atulizar():
    
    # Configuração
    VERSAO_ATUAL = "1.0"  # Versão atual do software
    UPDATE_URL = "https://www.dropbox.com/scl/fi/vlktpn0q0cris2e57gn3e/update.json?rlkey=e9333hx720igm6c4e96egv82z&st=0kfy9s8j&dl=1"  # Link para o JSON
    INSTALADOR_NOME = "Controle_de_estoque.exe"

    def verificar_atualizacao():
        try:
            messagebox.showinfo("Verificando", "Verificando atualizações...")

            # Baixa o arquivo JSON com as informações da atualização
            response = requests.get(UPDATE_URL)
            response.raise_for_status()  # Lança erro se houver falha

            # Converte JSON para dicionário
            update_data = json.loads(response.text)

            nova_versao = update_data.get("versao")
            download_url = update_data.get("url")

            if not nova_versao or not download_url:
                messagebox.showerror("Erro", "Erro ao verificar atualização.")
                return

            # Compara a versão
            if nova_versao > VERSAO_ATUAL:
                resposta = messagebox.askyesno("Atualização Disponível", 
                                            f"Uma nova versão {nova_versao} está disponível. Deseja baixar?")
                if resposta:
                    baixar_instalador(download_url)
            else:
                messagebox.showinfo("Atualização", "Seu software já está atualizado.")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao verificar atualização:\n{e}")

    def baixar_instalador(url):
        try:
            messagebox.showinfo("Download", "Baixando atualização...")
        
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(INSTALADOR_NOME, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            messagebox.showinfo("Sucesso", "Download concluído! Instalando atualização...")
            os.system(INSTALADOR_NOME)  # Executa o instalador
            exit()

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao baixar atualização:\n{e}")

    # Criando a interface Tkinter
    root = tk.Tk()
    root.title("Verificador de Atualização")
    root.geometry("300x200")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    label = tk.Label(frame, text="Verificar Atualização", font=("Arial", 12))
    label.pack(pady=10)

    btn_verificar = tk.Button(frame, text="Verificar", command=verificar_atualizacao)
    btn_verificar.pack(pady=10)
#***************************************************************************************************  

         
def relatorio():
    
    #Criar uma nova janela
    root4 = Toplevel(root) 
    root4.title("Relatórios")
    root4.geometry("900x900")
    root4.configure(background=co0)
    root4.resizable(width=False, height=False)
    largura_root = 900
    altura_root = 900
    #obter tamanho da tela
    largura_tela = root4.winfo_screenwidth()
    altura_tela = root4.winfo_screenheight()
    # Calcular posição para centralizar
    pos_x = ( largura_tela-largura_root )//2
    pos_y = (altura_tela - altura_root)//2
    # Definir geometria da janela (LxA+X+Y)
    root4.geometry(f"{largura_root}x{altura_root}+{pos_x}+{pos_y}")
    
    
    frame_painel = Frame(root4, width=900, height=900, bg=co0)
    frame_painel.place(x=0, y=0)
    
    # Definir a tabela (treeview)
    tree = ttk.Treeview(frame_painel, columns=("Produto", "Quantidade", "Categoria", "valor_total_Produto"), show="headings")
    tree.heading("Produto", text="Produto")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Categoria", text="Categoria")
    tree.pack()

    # Função para exibir o relatório
    def gerar_relatorio():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT produto, quantidade, categoria, valor_total_Produto FROM estoque")
        resultados = cursor.fetchall()
        conn.close()

        # Limpar a tabela antes de inserir novos dados
        for row in tree.get_children():
            tree.delete(row)

        # Inserir dados na tabela
        for produto, quantidade, categoria, valor_total_Produto  in resultados:
            tree.insert("", "end", values=(produto, quantidade, categoria, valor_total_Produto))

    # Função para gerar o gráfico
    def gerar_grafico():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT produto, quantidade, valor_total_Produto FROM estoque")
        resultados = cursor.fetchall()
        conn.close()

        if resultados:
            produtos = [row[0] for row in resultados]
            quantidades = [row[1] for row in resultados]

            # Criar o gráfico
            fig, ax = plt.subplots()
            ax.bar(produtos, quantidades, color="lightblue")
            ax.set_title("Estoque de Produtos")
            ax.set_xlabel("Produtos")
            ax.set_ylabel("Quantidade")

            # Exibir o gráfico no Tkinter
            canvas = FigureCanvasTkAgg(fig, master=frame_painel)
            canvas.get_tk_widget().pack()
            canvas.draw()
        else:
            messagebox.showinfo("Informação", "Nenhum dado disponível para gerar o gráfico.")

        # Frame para o relatório
        columns = ("Produto", "Quantidade", "Categoria", "valor total Produto")
        tree = ttk.Treeview(frame_painel, columns=columns, show="headings")
        tree.heading("Produto", text="Produto")
        tree.heading("Quantidade", text="Quantidade")
        tree.heading("Categoria", text="Categoria")
        tree.heading("valor total Produto", text="valor total Produto")
        tree.pack(fill="both", expand=True)
    
    def executar_tarefas():
        gerar_relatorio()
        gerar_grafico()

    # Criando um botão unificado
    btn_unificado = ttk.Button(frame_painel, text="Gerar Tudo", command=executar_tarefas)
    btn_unificado.pack(pady=10)

#***************************************************************************************************        
def estoque(): 
    
    #Criar uma nova janela
    root5 = Toplevel(root) 
    root5.title("Painel de Controle")
    root5.geometry("900x900")
    root5.configure(background=co0)
    root5.resizable(width=False, height=False)
    largura_root = 900
    altura_root = 900
    #obter tamanho da tela
    largura_tela = root5.winfo_screenwidth()
    altura_tela = root5.winfo_screenheight()
    # Calcular posição para centralizar
    pos_x = ( largura_tela-largura_root )//2
    pos_y = (altura_tela - altura_root)//2
    # Definir geometria da janela (LxA+X+Y)
    root5.geometry(f"{largura_root}x{altura_root}+{pos_x}+{pos_y}")
    
    
    
    def calcular_estoque(event=None):
        try:
            quantidade_text = e_quantidade.get().strip()
            preco_text = e_preco_custo.get().strip()
            if not quantidade_text or not preco_text:  # Check for empty inputs
                raise ValueError  # This triggers the error handling block
            quantidade = int(quantidade_text)
            valor_unitario = float(preco_text)
            total = quantidade * valor_unitario
            e_valor_total_Produto.delete(0, tk.END)
            e_valor_total_Produto.insert(0, f"{total:.2f}")
        except ValueError:
            e_valor_total_Produto.delete(0, tk.END)
            e_valor_total_Produto.insert(0, "Erro")
    
        
    def novo_produto():
        
        fornecedor = c_fornecedor.get().strip()
        produto = e_produto.get().strip()
        quantidade = e_quantidade.get().strip()
        categoria = c_categoria.get().strip()
        preco_custo = e_preco_custo.get().strip()
        valor_total_Produto = e_valor_total_Produto.get().strip()
        ean = e_ean.get().strip()
        valor_total_estoque = e_valor_total_estoque.get().strip()
       
       
        lista =[fornecedor,produto,quantidade,categoria,preco_custo,valor_total_Produto,ean,valor_total_estoque]
        # Check for empty fields
        campos = ["Fornecedor", "Produto", "Quantidade", "Categoria", "Preço de Custo", "Valor Total Produto", "EAN", "Valor Total Estoque"]
    
        for campo, valor in zip(campos, lista):
            if not valor:
                messagebox.showerror('Erro', f'Preencha o campo: {campo}')
                return
        criar_estoque(lista)
        messagebox.showinfo('Sucesso', 'Os produtos inseridos com sucesso!')
           
        c_fornecedor.delete(0, tk.END)
        e_produto.delete(0, tk.END)
        e_quantidade.delete(0, tk.END)
        c_categoria.delete(0, tk.END)
        e_preco_custo.delete(0, tk.END)
        e_valor_total_Produto.delete(0, tk.END)
        e_ean.delete(0, tk.END)
        e_valor_total_estoque.delete(0, tk.END)
        
        # Clear inputs
        for widget in [c_fornecedor, e_produto, e_quantidade, c_categoria, e_preco_custo, e_valor_total_Produto, e_ean, e_valor_total_estoque]:
         widget.delete(0, tk.END)
                 
        mostrar_produtos()
        
    def atualizar_produto():
        
        try:
            tree_itens = tree_estoque.focus()
            tree_dicionario = tree_estoque.item(tree_itens)
            tree_lista = tree_dicionario['values']
            
            valor_id = tree_lista[0]
        
            c_fornecedor.delete(0, END)
            e_produto.delete(0, END)
            e_quantidade.delete(0, END)
            c_categoria.delete(0, END)
            e_preco_custo.delete(0, END)
            e_valor_total_Produto.delete(0, END)
            e_ean.delete(0, END)
            e_valor_total_estoque.delete(0, END)
            
            c_fornecedor.insert(0, tree_lista[1])
            e_produto.insert(0, tree_lista[2])
            e_quantidade.insert(0, tree_lista[3])
            c_categoria.insert(0, tree_lista[4])
            e_preco_custo.insert(0, tree_lista[5])
            e_valor_total_Produto.insert(0, tree_lista[6])
            e_ean.insert(0, tree_lista[7])
            e_valor_total_estoque.insert(0, tree_lista[8])
            
            def update():
                
                fornecedor = c_fornecedor.get()
                produto = e_produto.get()
                quantidade = e_quantidade.get()
                categoria = c_categoria.get()
                preco_custo = e_preco_custo.get()
                valor_total_Produto = e_valor_total_Produto.get()
                ean = e_ean.get()
                valor_total_estoque = e_valor_total_estoque.get()
                
                lista= [fornecedor, produto,quantidade,categoria,preco_custo,valor_total_Produto,ean,valor_total_estoque, valor_id]
    
                atualizar_estoque(lista)
                messagebox.showinfo("Sucesso","Produto atualizado com sucesso!")
                
                c_fornecedor.delete(0, END)
                e_produto.delete(0, END)
                e_quantidade.delete(0, END)
                c_categoria.delete(0, END)
                e_preco_custo.delete(0, END)
                e_valor_total_Produto.delete(0, END)
                e_ean.delete(0, END)
                e_valor_total_estoque.delete(0,END)
            
                mostrar_produtos()
                botao_update.destroy()
                
            botao_update = Button(frame_cad_geral, command= update,  anchor=CENTER,text='Salvar e Atualizar'.upper(), width=18, overrelief=RIDGE, font=('Ivy 7'), bg=co3, fg=co1)
            botao_update.place(x=710, y=130)  
        except IndexError:
            messagebox.showerror('Erro', 'Selecione os dados na tabela')
  
    def del_produto():
        try:
            tree_itens = tree_estoque.focus()
            tree_dicionario = tree_estoque.item(tree_itens)
            tree_lista = tree_dicionario['values']
            
            valor_id = tree_lista[0]
            
            # deletar dados no Banco de Dados
            deletar_estoque([valor_id])
            
            #Mostrando a menssagem de sucesso
            messagebox.showinfo('Sucesso', 'Produtos deletado com sucesso!')
            
            #mostrando os valores na tabela
            mostrar_produtos()
        except IndexError:
         messagebox.showerror('Erro', 'Selecione um dos produto na tabela')
    # Função para buscar e exibir a soma dos valores no banco
    def atualizar_valor_total():
        try:
            # Conectar ao banco de dados
            with sqlite3.connect("database.db") as conexao:  # Melhora segurança e evita vazamento de conexões
                cursor = conexao.cursor()
                cursor.execute("SELECT SUM(valor_total_Produto) FROM estoque")
                resultado = cursor.fetchone()

            # Define o valor atualizado ou 0.00 caso não haja registros
            valor_estoque = float(resultado[0]) if resultado[0] is not None else 0.00

            # Atualiza a Entry automaticamente
            e_valor_total_estoque.config(state="normal")
            e_valor_total_estoque.delete(0, tk.END)
            e_valor_total_estoque.insert(0, f"{valor_estoque:.2f}")  # Formato decimal
            e_valor_total_estoque.config(state="readonly")

        except Exception as e:
            e_valor_total_estoque.config(state="normal")
            e_valor_total_estoque.delete(0, tk.END)
            e_valor_total_estoque.insert(0, f"Erro: {e}")  # Exibe erro na Entry
            e_valor_total_estoque.config(state="readonly")

    #  Definir a função de atualização automática UMA VEZ fora da função principal
    def atualizar_automaticamente():
        atualizar_valor_total()
        frame_cad_geral.after(5000, atualizar_automaticamente)  # Atualiza a cada 5 segundos
        
    
    frame_cad_titulo = Frame(root5, width=900, height=50, bg=co0 )
    frame_cad_titulo.grid(row=0, column=0, sticky=NSEW)
    
    frame_cad_geral = Frame(root5, width=900, height=500, bg=co0 )
    frame_cad_geral.grid(row=1, column=0, sticky=NSEW)
    
    frame_tabela = Frame(root5, width=900, height=350, bg=co0)
    frame_tabela.grid(row=3, column=0, sticky=NSEW)
        
    l_titulo= Label(frame_cad_titulo, text="Cadastre novos Produtos", font=('Ivy 20 bold'), bg=co0, fg=co1)
    l_titulo.place(x=450, y=25, anchor=CENTER)
    
    bt_estoque = Button(frame_cad_geral, command=novo_produto, text="Adicionar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_estoque.place(x=10, y=10)
    
    bt_delete = Button(frame_cad_geral, command=del_produto, text="Delete", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_delete.place(x=100, y=10)
    
    bt_atualizar = Button(frame_cad_geral, command=atualizar_produto, text="Atualizar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_atualizar.place(x=170, y=10)
    
    bt_procurar = Button(frame_cad_geral, command=None, text="Procurar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_procurar.place(x=260, y=10)
    
    bt_imprimir = Button(frame_cad_geral, command=None, text="Imprimir", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_imprimir.place(x=345, y=10)
    
    bt_cad_produto = Button(frame_cad_geral, command=categoria, text="Cadastrar Produto", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_cad_produto.place(x=435, y=10)
    
    bt_cad_fornecedor = Button(frame_cad_geral, command=fornecedor, text="Fornecedores", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_cad_fornecedor.place(x=605, y=10)
    
    #bt_cad_voltar = Button(frame_cad_geral, command=abrir_painel, text="Voltar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    #bt_cad_voltar.place(x=738, y=10)
    
    a_id = Label(frame_cad_geral, text="Id:", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_id.place(x=10, y=60)
    e_id = Entry(frame_cad_geral, width=10, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_id.place(x=75, y=60)
    
    a_produto = Label(frame_cad_geral, text="Produto:", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_produto.place(x=10, y=90)
    e_produto = Entry(frame_cad_geral, width=30, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_produto.place(x=75, y=90)
    
    a_quantidade = Label(frame_cad_geral, text="Quantidade:", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_quantidade.place(x=10, y=120)
    e_quantidade = Entry(frame_cad_geral, width=10, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_quantidade.bind("<KeyRelease>", calcular_estoque) 
    e_quantidade.place(x=95, y=120)
    
    c_categoria = ttk.Combobox(frame_cad_geral, width=18, font=('Ivy 8 bold'))
    c_categoria.set('Categorias')
    c_categoria['values'] = ver_categoria()
    c_categoria.place(x=10, y=150)
    
    #Pegando as Fornecedores
    fornecedores = Ver_fornecedor()  # Fetches supplier data.
    # Extract the second element (index 1) from each entry in fornecedores.
    lista_fornecedores = [i[2] for i in fornecedores]
    # Create the Combobox.
    c_fornecedor = ttk.Combobox(frame_cad_geral, width=30, font=('Ivy 8 bold'))
    c_fornecedor['values'] = lista_fornecedores  # Set the list of options.
    c_fornecedor.set(lista_fornecedores[0] if lista_fornecedores else "Fornecedores")  # Set the default value.
    c_fornecedor.place(x=10, y=180)  # Define its position.
    
    a_preco_custo = Label(frame_cad_geral, text="Preço de Custo (R$):", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_preco_custo.place(x=10, y=210)
    e_preco_custo = Entry(frame_cad_geral ,width=20, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_preco_custo.bind("<KeyRelease>", calcular_estoque) 
    e_preco_custo.place(x=145, y=210)
    
    a_valor_total_Produto = Label(frame_cad_geral, text="Valor total em estoque por produto:(R$):", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_valor_total_Produto.place(x=10, y=240)
    e_valor_total_Produto = Entry(frame_cad_geral,width=20,state="normal", justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_valor_total_Produto.place(x=265, y=240)
 
    a_valor_total_estoque = Label(frame_cad_geral, text="Valor Total em estoque(R$):", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_valor_total_estoque.place(x=10, y=270)
    e_valor_total_estoque = Entry(frame_cad_geral, state="readonly", width=20, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_valor_total_estoque.place(x=200, y=270)
    atualizar_automaticamente()  
    
    a_ean = Label(frame_cad_geral, text="EAN:", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_ean.place(x=270, y=60)
    e_ean = Entry(frame_cad_geral, width=20, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid", )
    e_ean.place(x=310, y=60)

    
    
    def mostrar_produtos():
        
        app_nome = Label(frame_tabela, text="Tabela de Produtos", height=1, pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
        app_nome.grid(row=0, column=0, padx=0, pady=10, sticky=NSEW)

        # Definição do cabeçalho
        list_header = ['id', 'fornecedor', 'produto', 'quantidade', 'categoria',  'preco_custo','valor_total_Produto', 'valor_total_em_estoque', 'ean']
    
        # Obtém os dados do estoque
        df_list = ver_estoque()  # Certifique-se de que essa função retorna os dados corretamente
    
        global tree_estoque
    
        # Criando a Treeview
        tree_estoque = ttk.Treeview(frame_tabela, selectmode="extended", columns=list_header, show="headings")

        # Barras de rolagem
        vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree_estoque.yview)
        hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree_estoque.xview)  # Corrigido aqui

        tree_estoque.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
        # Posicionando os widgets
        tree_estoque.grid(column=0, row=1, sticky='nsew')
        vsb.grid(column=1, row=1, sticky='ns')
        hsb.grid(column=0, row=2, sticky='ew')
    
        frame_tabela.grid_rowconfigure(0, weight=12)

        # Configuração das colunas
        hd = ["nw", "nw", "nw", "center", "center", "center", "center", "center", "center"]
        h = [40, 150, 150, 70, 70, 150, 150, 100,100 ]
    
        for n, col in enumerate(list_header):
            tree_estoque.heading(col, text=col.title(), anchor=NW)
            tree_estoque.column(col, width=h[n], anchor=hd[n])

        # Inserindo os dados
        if df_list:
            for item in df_list:
                tree_estoque.insert("", "end", values=item)
    mostrar_produtos()
#***************************************************************************************************   
def categoria():
    
    # Criar uma nova janela
    root2 = Toplevel()
    root2.title("Categorias")
    root2.geometry("300x150")

    # Obter tamanho da tela e centralizar janela
    largura_tela = root2.winfo_screenwidth()
    altura_tela = root2.winfo_screenheight()
    largura_janela, altura_janela = 300, 150
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root2.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # Criar Widgets (fora da função interna)
    l_titulo = Label(root2, text="Cadastrar Categoria", font=("Ivy", 10), bg=co0, fg=co1)
    l_titulo.pack(pady=10)

    e_cat = Entry(root2, width=30, justify="left", relief="solid")
    e_cat.pack(pady=5)

    def nova_categoria():
        nome = e_cat.get().strip()  # Remove espaços extras
        if nome == "":
            messagebox.showerror("Erro", "Preencha o campo!")
            return
        
        criar_categoria([nome])  # Adiciona ao banco
        messagebox.showinfo("Sucesso", "Categoria cadastrada com sucesso!")
        root2.destroy()  # Fecha a janela após sucesso

    # Botão corrigido (posicionado corretamente)
    bt_cad_produto = Button(root2, text="Cadastrar", command=nova_categoria, bd=3, bg=co0, fg=co1, font=("verdana", 10, "bold"))
    bt_cad_produto.pack(pady=10)
    
    bt_del_produto = Button(root2, text="Deletar", command=nova_categoria, bd=3, bg=co0, fg=co1, font=("verdana", 10, "bold"))
    bt_del_produto.pack(pady=10)
#*************************************************************************************************** 
def fornecedor():
    
    # Criar uma nova janela
    root3 = Toplevel()
    root3.title("Fornecedores")
    root3.geometry("600x650")
    
    root3.configure(background=co0)
    root3.resizable(width=False, height=False)
    #janela.overrideredirect(1)
    largura_janela = 600
    altura_janela = 650
    # Obter tamanho da tela
    largura_tela = root3.winfo_screenwidth()
    altura_tela = root3.winfo_screenheight()
    # Calcular posição para centralizar
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    # Definir geometria da janela (LxA+X+Y)
    root3.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    
    frame_cad_titulo = Frame(root3, width=900, height=50, bg=co0)
    frame_cad_titulo.grid(row=0, column=0, sticky=NSEW)
    
    frame_cad_botoes = Frame(root3, width=900, height=50, bg=co0)
    frame_cad_botoes.grid(row=1, column=0, sticky=NSEW)
   
    frame_cad_produtos = Frame(root3, width=900, height=250, bg=co0)
    frame_cad_produtos.grid(row=2, column=0, sticky=NSEW)
    
    frame_tabela = Frame(root3, width=900, height=550, bg=co0)
    frame_tabela.grid(row=3, column=0, sticky=NSEW)
        
    l_titulo= Label(frame_cad_titulo, text="Cadastre um novo fornecedor", font=('Ivy 20 bold'), bg=co0, fg=co1)
    l_titulo.place(x=300, y=25, anchor=CENTER)
    
    def novo_fornecedor():
        cnpj = e_cnpj.get()
        razao_social = e_razao_social.get()
        nome_fantasia = e_nome_fantasia.get()
        vendedor = e_vendedor.get()
        
        lista = [cnpj, razao_social, nome_fantasia, vendedor]
        
        for i in lista:
            if i =='':
                messagebox.showerror('Erro', 'Preencha todos os campos!')
                return
        criar_fornecedor(lista)
        messagebox.showinfo('Sucesso', 'Fornecedor adicionado com sucesso!')
        
        e_cnpj.delete(0, END)
        e_razao_social.delete(0, END)
        e_nome_fantasia.delete(0, END)
        e_vendedor.delete(0, END)
        
        mostrar_fornecedores() 
        
    def del_fornecedor():
        try:
            tree_itens = tree_fornecedores.focus()
            tree_dicionario = tree_fornecedores.item(tree_itens)
            tree_lista = tree_dicionario['values']
            
            valor_id = tree_lista[0]
            
            # deletar dados no Banco de Dados
            deletar_fornecedor([valor_id])
            
            #Mostrando a menssagem de sucesso
            messagebox.showinfo('Sucesso', 'Fornecedor deletado com sucesso!')
            
            #mostrando os valores na tabela
            mostrar_fornecedores()
        except IndexError:
         messagebox.showerror('Erro', 'Selecione um dos fornecedores na tabela')
        
        
    def mostrar_fornecedores():
        
        app_nome = Label(frame_tabela, text="Tabela de Produtos", height=1, pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
        app_nome.grid(row=0, column=0, padx=0, pady=10, sticky=NSEW)

        # Definição do cabeçalho
        list_header = ['id', 'cnpj', 'razao_social', 'nome_fantasia', 'vendedor' ]
    
        # Obtém os dados do estoque
        df_list = Ver_fornecedor()  # Certifique-se de que essa função retorna os dados corretamente
    
        global tree_fornecedores
    
        # Criando a Treeview
        tree_fornecedores = ttk.Treeview(frame_tabela, selectmode="extended", columns=list_header, show="headings")

        # Barras de rolagem
        vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree_fornecedores.yview)
        hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree_fornecedores.xview)  # Corrigido aqui

        tree_fornecedores.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
        # Posicionando os widgets
        tree_fornecedores.grid(column=0, row=1, sticky='nsew')
        vsb.grid(column=1, row=1, sticky='ns')
        hsb.grid(column=0, row=2, sticky='ew')
    
        frame_tabela.grid_rowconfigure(0, weight=12)

        # Configuração das colunas
        hd = ["nw", "nw", "nw", "nw", "nw", "nw"]
        h = [30, 90, 150, 150, 150]
    
        for n, col in enumerate(list_header):
            tree_fornecedores.heading(col, text=col.title(), anchor=NW)
            tree_fornecedores.column(col, width=h[n], anchor=hd[n])

        # Inserindo os dados
        if df_list:
            for item in df_list:
                tree_fornecedores.insert("", "end", values=item)

    mostrar_fornecedores()  
    
    bt_add = Button(frame_cad_botoes, command=novo_fornecedor, text="Adicionar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_add.place(x=10, y=10)
    
    bt_delete = Button(frame_cad_botoes, command=del_fornecedor, text="Delete", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_delete.place(x=102, y=10)
    
    bt_update = Button(frame_cad_botoes, command=None, text="Atualizar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_update.place(x=174, y=10)
    
    bt_procurar = Button(frame_cad_botoes, command=None, text="Procurar", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_procurar.place(x=266, y=10)
    
    bt_imprimir = Button(frame_cad_botoes, command=None, text="Imprimir", bd=3, bg=co0, fg=co1, font=('verdana', 11, 'bold'))
    bt_imprimir.place(x=358, y=10)
    
    
    a_id = Label(frame_cad_produtos, text="ID:", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_id.place(x=10, y=40)
    e_id = Entry(frame_cad_produtos, width=10, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_id.place(x=55, y=40)
    
    a_cnpj = Label(frame_cad_produtos, text="CNPJ:", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_cnpj.place(x=10, y=80)
    e_cnpj = Entry(frame_cad_produtos, width=50, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_cnpj.place(x=55, y=80)
    
    a_razao_social = Label(frame_cad_produtos, text="Razão Social:", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_razao_social.place(x=10, y=120)
    e_razao_social = Entry(frame_cad_produtos, width=50, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_razao_social.place(x=105, y=120)
    
    a_nome_fantasia = Label(frame_cad_produtos, text="Nome Fantasia:", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_nome_fantasia.place(x=10, y=160)
    e_nome_fantasia = Entry(frame_cad_produtos, width=50, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_nome_fantasia.place(x=115, y=160)
    
    a_vendedor = Label(frame_cad_produtos, text="Vendedor:", font=('Ivy 10 bold'), bg=co0,fg=co1)
    a_vendedor.place(x=10, y=200)
    e_vendedor = Entry(frame_cad_produtos, width=50, justify=LEFT, font=('Ivy 10 bold'), highlightthickness=1, relief="solid")
    e_vendedor.place(x=115, y=200)
    
        
     
login()
root.mainloop()