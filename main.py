# -*- coding: utf-8 -*-
"""
Created on Sat May 22 12:56:37 2021

@author: rodri
"""
import time 

class No:
     
     def __init__(self, key, dir, esq):
          self.item = key
          self.dir = dir
          self.esq = esq



class InterfaceUsuario:
    
    def __init__(self):
        self.tab = {}
        self.tokens = None
        self.root = None
        self.lista = []
        self.gera_indices_local()
        self.menu()
       
    def _is_int(self, numero):
        try: 
            num = int(numero)
            return True
        except:
            return False
    
    def nosucessor(self, apaga): # O parametro é a referencia para o No que deseja-se apagar
      paidosucessor = apaga
      sucessor = apaga
      atual = apaga.dir # vai para a subarvore a direita

      while atual != None: # enquanto nao chegar no Nó mais a esquerda
           paidosucessor = sucessor
           sucessor = atual
           atual = atual.esq # caminha para a esquerda

      # *********************************************************************************
      # quando sair do while "sucessor" será o Nó mais a esquerda da subarvore a direita
      # "paidosucessor" será o o pai de sucessor e "apaga" o Nó que deverá ser eliminado
      # *********************************************************************************
      if sucessor != apaga.dir: # se sucessor nao é o filho a direita do Nó que deverá ser eliminado
           paidosucessor.esq = sucessor.dir # pai herda os filhos do sucessor que sempre serão a direita
           # lembrando que o sucessor nunca poderá ter filhos a esquerda, pois, ele sempre será o
           # Nó mais a esquerda da subarvore a direita do Nó apaga.
           # lembrando também que sucessor sempre será o filho a esquerda do pai
           sucessor.dir = apaga.dir # guardando a referencia a direita do sucessor para 
                                    # quando ele assumir a posição correta na arvore
      return sucessor

    def inOrder(self, atual):
         if atual != None:
              self.inOrder(atual.esq)
              print(atual.item,end=" ")
              if (atual.item not in self.lista):
                  self.lista.append(atual.item)
              self.inOrder(atual.dir)
  
    def preOrder(self, atual):
         if atual != None:
              if (atual.item not in self.lista):
                self.lista.append(atual.item)
              print(atual.item,end=" ")
              self.preOrder(atual.esq)
              self.preOrder(atual.dir)
       
    def posOrder(self, atual):
         if atual != None:
              self.posOrder(atual.esq)
              self.posOrder(atual.dir)
              print(atual.item,end=" ")
              if (atual.item not in self.lista):
                  self.lista.append(atual.item)

  
    def altura(self, atual):
          if atual == None or atual.esq == None and atual.dir == None:
               return 0
          else:
             if self.altura(atual.esq) > self.altura(atual.dir):
                return  1 + self.altura(atual.esq) 
             else:
                return  1 + self.altura(atual.dir) 
  
    def folhas(self, atual):
         if atual == None:
              return 0
         if atual.esq == None and atual.dir == None:
              return 1
         return self.folhas(atual.esq) + self.folhas(atual.dir)

  
    def contarNos(self, atual):
        if atual == None:
             return 0
        else:
             return  1 + self.contarNos(atual.esq) + self.contarNos(atual.dir)

    def minn(self):
         atual = self.root
         anterior = None
         while atual != None:
              anterior = atual
              atual = atual.esq
         return anterior

    def maxx(self):
         atual = self.root
         anterior = None
         while atual != None:
              anterior = atual
              atual = atual.dir
         return anterior

    def caminhar(self):
          print(" Exibindo em ordem: ",end="")
          self.inOrder(self.root)
          print("\n Exibindo em pos-ordem: ",end="")
          self.posOrder(self.root)
          print("\n Exibindo em pre-ordem: ",end="")
          self.preOrder(self.root)
          print("\n Exibindo em ordem crescente: ",end="")
          self.OrdemCrescente(self.root)
          print("\n Exibindo em ordem decrescente: ",end="")
          self.OrdemDecrescente(self.root)
          print("\n Altura da arvore: %d" %(self.altura(self.root)))
          print(" Quantidade de folhas: %d"  %(self.folhas(self.root)))
          print(" Quantidade de Nós: %d" %(self.contarNos(self.root)))

    def buscar_arvore(self, chave):
         if self.root == None:
              return None # se arvore vazia
         atual = self.root # começa a procurar desde raiz
         while chave not in  atual.item: # enquanto nao encontrou
             indice = atual.item.split(' - ')[1]  
             if chave < indice:
                 atual = atual.esq # caminha para esquerda
             else:
                 atual = atual.dir # caminha para direita
             if atual == None:
               return None # encontrou uma folha -> sai
         return atual  # terminou o laço while e chegou aqui é pq encontrou item    

     # O sucessor é o Nó mais a esquerda da subarvore a direita do No que foi passado como parametro do metodo
     
    def inserir_arvore(self, v):
          novo = No(v, None, None) # cria um novo Nó
          if self.root == None:
               self.root = novo
          else: # se nao for a raiz
               atual = self.root
               while True:
                    anterior = atual
                    if v <= atual.item: # ir para esquerda
                         atual = atual.esq
                         if atual == None:
                                anterior.esq = novo
                                return
                    # fim da condição ir a esquerda
                    else: # ir para direita
                         atual = atual.dir
                         if atual == None:
                                 anterior.dir = novo
                                 return
                    # fim da condição ir a direita
                    
    def ordena_dados(self): 
        arq = open('tweets.txt', 'r+', encoding="utf8")
        arq_write = open('gravacao.txt', 'w+', encoding="utf8")
        tokens = []
        for linha in arq: 
            if (self._is_int(linha[:19])): 
                tokens.append(linha[:19])                        
        
        self.tokens = sorted(tokens)
        for token in self.tokens: 
            arq.seek(0)
            for linha in arq: 
                if self._is_int(linha[:19]):
                    if int(token) == int(linha[:19]): 
                        arq_write.write(linha)
                        break

    def pesquisa_binaria_hashtags(self):
        arquivo = open("indices_hashtags.txt","r", encoding="utf8")
        termo = input("Digite o índice procurado")
        inicio = 0
        fim = len(arquivo.readlines())
        inicio_original = fim
        arquivo.seek(0)     
        
        while (1):
            meio = inicio + (fim-1)/2    
            meio = int(meio)
            linha = arquivo.readline(meio)
            posicao = linha.split(' - ')
            
            if meio == inicio_original or meio < 0: 
                print("índice não encontrado")
                return 
                
            if int(termo) == int(posicao[0]): 
                print("Termo encontrado na posição: " + posicao[0] + ' com a hashtag: ' + posicao[1])
                id_tweet = posicao[1]
                break
            
            if int(posicao[0]) > int(termo): 
                fim = fim - 1
            
            if int(posicao[0]) < int(termo): 
                inicio = inicio + 1
        
        arquivo = open("gravacao.txt","r", encoding="utf8")
        termo = id_tweet
        inicio = 1
        fim = len(arquivo.readlines())
        inicio_original = fim
        arquivo.seek(0)
        
        while (1):
            meio = inicio + (fim-1)/2    
            meio = int(meio)
            linha = arquivo.readline(meio)
            posicao = linha[:19]
            
            if meio == inicio_original or meio < 0: 
                print("índice não encontrado")
                return 
                
            if termo in linha: 
                print("Termo encontrado na posição: " + posicao + ' -- ' + linha)
                id_tweet = posicao[1]
                break
            
            if int(posicao) > int(termo): 
                fim = fim - 1
            
            if int(posicao) < int(termo): 
                inicio = inicio + 1
        
        arquivo.close()
        
    def pesquisa_binaria(self):
        arquivo = open("indices.txt","r", encoding="utf8")
        termo = input("Digite o índice procurado")
        inicio = 0
        fim = len(arquivo.readlines())
        inicio_original = fim
        arquivo.seek(0)     
        
        while (1):
            meio = inicio + (fim-1)/2    
            meio = int(meio)
            linha = arquivo.readline(meio)
            posicao = linha.split(' - ')
            
            if meio == inicio_original or meio < 0: 
                print("índice não encontrado")
                return 
                
            if int(termo) == int(posicao[0]): 
                print("Termo encontrado na posição: " + posicao[0] + ' com o id do tweet: ' + posicao[1])
                id_tweet = posicao[1]
                break
            
            if int(posicao[0]) > int(termo): 
                fim = fim - 1
            
            if int(posicao[0]) < int(termo): 
                inicio = inicio + 1
        
        arquivo = open("gravacao.txt","r", encoding="utf8")
        termo = id_tweet
        inicio = 1
        fim = len(arquivo.readlines())
        inicio_original = fim
        
        arquivo.seek(0)
        
        while (1):
            meio = inicio + (fim-1)/2    
            meio = int(meio)
            linha = arquivo.readline(meio)
            posicao = linha[:19]
            
            if meio == inicio_original or meio < 0: 
                print("índice não encontrado")
                return 
                
            if int(termo) == int(posicao): 
                print("Termo encontrado na posição: " + posicao + ' -- ' + linha)
                id_tweet = posicao[1]
                break
            
            if int(posicao) > int(termo): 
                fim = fim - 1
            
            if int(posicao) < int(termo): 
                inicio = inicio + 1
        
        arquivo.close()
     
    def pesquisa_binaria_local(self, p_termo):
        arquivo = open("indices_local.txt","r", encoding="utf8")
        if p_termo: 
            termo = p_termo.item.split(' - ')[1].strip()
        else:
            termo = input("Digite o índice procurado")
        id_termo = p_termo.item.split(' - ')[0].strip()
        inicio = 0
        fim = len(arquivo.readlines())
        inicio_original = fim
        arquivo.seek(0)     
        while (1):
            meio = inicio + (fim-1)/2    
            meio = int(meio)
            linha = arquivo.readline(meio)
            posicao = linha.split(' - ')
            
            if meio == inicio_original or meio < 0: 
                print("índice não encontrado 1")
                return 
                
            if termo in posicao[1].lower(): 
                print("Termo encontrado na posição: " + posicao[0] + ' com o local: ' + posicao[1])
                id_tweet = posicao[0]
                break
            
            if int(posicao[0]) > int(id_termo): 
                fim = fim - 1
            
            if int(posicao[0]) < int(id_termo): 
                inicio = inicio + 1
        
        arquivo = open("gravacao.txt","r", encoding="utf8")
        termo = id_tweet
        inicio = 1
        fim = len(arquivo.readlines())
        inicio_original = fim
        arquivo.seek(0)
        
        while (1):
            meio = inicio + (fim-1)/2    
            meio = int(meio)
            linha = arquivo.readline(meio)
            posicao = linha[:19]
            
            if meio == inicio_original or meio < 0: 
                print("índice não encontrado")
                return 
                
            if termo in linha: 
                print("Termo encontrado na posição: " + posicao + ' -- ' + linha)
                id_tweet = posicao[1]
                break
            
            if int(posicao) > int(termo): 
                fim = fim - 1
            
            if int(posicao) < int(termo): 
                inicio = inicio + 1
        
        arquivo.close()

    def mostrar_dados(self): 
        arq = open('gravacao.txt', 'r+', enconding="utf8")
        for linha in arq: 
            print(linha)
        arq.close()

    def gera_indices(self): 
        arq_indices = open('indices.txt', 'w+')
        arq_gravacao = open('gravacao.txt', 'r+', encoding="utf8")
        count = 0
        
        for linha in arq_gravacao: 
            indice = linha[:19]
            linha_escrita = "%s - %s \n" %(count, indice)
            arq_indices.write(linha_escrita)
            count += 1
            
    def gera_indices_hashtags(self): 
        arq_indices = open('indices_hashtags.txt', 'w+',  encoding="utf8")
        arq_gravacao = open('gravacao.txt', 'r+', encoding="utf8")
        count = 0
        
        for linha in arq_gravacao: 
            indice = linha[378:]
            linha_escrita = "%s - %s \n" %(count, indice)
            arq_indices.write(linha_escrita)
            count += 1
   
    def gera_indices_local(self): 
        arq_indices = open('indices_local.txt', 'w+',  encoding="utf8")
        arq_gravacao = open('gravacao.txt', 'r+', encoding="utf8")
        count = 0
        
        for linha in arq_gravacao: 
            indice = linha[327:377].strip().replace(', ', '')
            linha_escrita = "%s - %s \n" %(count, indice)
            arq_indices.write(linha_escrita)
            count += 1
    
    def gera_hash(self, chave): 
        return hash(float(chave) + time.time())
    
    
    def gera_indices_hash(self): 
        arquivo = open('gravacao.txt', 'r+',  encoding="utf8")
        dic = {}
        for linha in arquivo: 
            data = linha[319:327]
            dic[self.gera_hash(data)] = linha
            time.sleep(0.000000000000000000000000000000000000000001)
        self.tab = dic 
        
        #for i in dic:     
         #   print(i)
          #  break
        
    def pesquisa_hash(self): 
        response = input("Digite o Hash")
        cod_hash = str(self.tab.get(response))
        print(self.tab[cod_hash])
    
    def insere_dados_arvore(self): 
        arq_gravacao = open('gravacao.txt', 'r+', encoding="utf8")
        for linha in arq_gravacao: 
            indice = linha[327:377]
            indice = indice.lower().strip()
            linha = "%s - %s" %(linha[:19], indice)
            self.inserir_arvore(linha)

    def caminhar(self):
        print(" Exibindo em ordem: ",end="")
        self.inOrder(self.root)
        print("\n Exibindo em pos-ordem: ",end="")
        self.posOrder(self.root)
        print("\n Exibindo em pre-ordem: ",end="")
        self.preOrder(self.root)
        print("\n Altura da arvore: %d" %(self.altura(self.root)))
        print(" Quantidade de folhas: %d"  %(self.folhas(self.root)))
        print(" Quantidade de Nós: %d" %(self.contarNos(self.root)))
     
    def resposta_hipotese(self): 
        arq_gravacao = open('indices_local.txt', 'r+', encoding="utf8")
        arq_gravacao2 = open('indices_local.txt', 'r+', encoding="utf8")
        estado_mais_comentarios = dict()
        count = 0
        for linha in arq_gravacao: 
            estado = linha.split(' - ')[1].strip()
            arq_gravacao2.seek(0)
            quantidade = 0
            count += 1
            if len(estado.lower()) > 1 and estado.lower() not in 'brasil':
                for linha2 in arq_gravacao2: 
                    estado2 = linha2.split(' - ')[1].strip()
                    if estado.lower() in estado2.lower():
                        quantidade += 1
                        estado_mais_comentarios[count] = {
                            'estado': estado.lower().strip(), 
                            'quantidade': quantidade
                        }
                    
        estado = 'Nenhum'
        maior = 0
        
        for item in estado_mais_comentarios: 
           if estado_mais_comentarios.get(item)['quantidade'] > maior:
               maior = estado_mais_comentarios.get(item)['quantidade']
               estado = estado_mais_comentarios.get(item)['estado']        
        print(estado)

    def menu(self):
        print("0 - SAIR")
        print("1 - Ler API")
        print("2 - Ordenar Dados")
        print("3 - Gerar índices por hashtags")
        print("4 - Gerar índices")
        print("5 - Gerar índices por hash")
        print("6 - Pesquisa binária")
        print("7 - Pesquisa binária hashtags")
        print("8 - Pesquisa por hash")
        print("9 - Inserir dados na árvore binária")
        print("10 - Buscar dados na árvore binária")
        print("11 - Exibe os dados da árvore binária")
        print("12 - Resposta da hipótese (Qual estado comenta mais sobre vacina?)")
        
        response = input("O que deseja fazer?")
    
        while (response != 0):
    
            if (int(response) == 1):
                self.mostrar_dados()
            elif (int(response) == 2):
                self.ordena_dados()
            elif (int(response) == 3):
                self.gera_indices_hashtags()
            elif (int(response) == 4):
                self.gera_indices()
            elif (int(response) == 5):
                self.gera_indices_hash()
            elif (int(response) == 6):
                self.pesquisa_binaria()
            elif (int(response) == 7):
                self.pesquisa_binaria_hashtags()
            elif (int(response) == 8):
                self.pesquisa_hash()
            elif (int(response) == 9): 
                self.insere_dados_arvore()
            elif (int(response) == 10):
                x = input("Digite o local procurado: ")
                termo = self.buscar_arvore(x)
                if (termo):
                    self.pesquisa_binaria_local(termo)
                else: 
                    print("Número não encontrado!")
            elif (int(response) == 11): 
                self.caminhar()
            elif (int(response) == 12): 
                self.resposta_hipotese()
            elif (int(response) == 0): 
                print("Execução fechada!")
                return
            
            print("0 - SAIR")
            print("1 - Ler API")
            print("2 - Ordenar Dados")
            print("3 - Gerar índices por hashtags")
            print("4 - Gerar índices")
            print("5 - Gerar índices por hash")
            print("6 - Pesquisa binária")
            print("7 - Pesquisa binária hashtags")
            print("8 - Pesquisa por hash")
            print("9 - Inserir dados na árvore binária")
            print("10 - Buscar dados na árvore binária")
            print("11 - Exibe os dados da árvore binária")
            print("12 - Resposta da hipótese (Qual estado comenta mais sobre vacina?)")
            response = input("O que deseja fazer?")
    
        return 
    
InterfaceUsuario()