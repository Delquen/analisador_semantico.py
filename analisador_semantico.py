# ----------------------------------------------------------------------------------- ANALISE LEXICA -----------------------------------------------------------------------------------------------------------------------------------------
# O arquivo do codigo eh aberto para que seja feita a Analise Lexica
# Favor inserir o nome do arquivo em que se encontra o codigo .txt dentro da funcao open()
arquivo = open('variaveis.txt')

# Declaracao das variaveis, listas e matrizes usadas no codigo
linhas = 19
caracteres = []
tokens = []

# Lista que contem as palavras reservadas, necessarias para serem  verificadas na definicao do token
palavras_reservadas = ['algoritmo', 'variaveis', 'contantes', 'registro', 'funcao', 'retorno', 'vazio', 'se', 'senao',
'enquanto', 'para', 'leia', 'escreva', 'inteiro', 'real', 'booleano', 'char', 'cadeia', 'verdadeiro', 'falso']
# Lista que contem os delimitadores, necessarios para serem verificadas na definicao do token
simbolos_delimitadores = ['(', ')', '{', '}', '[', ']', ',', ';']
# Lista que contem os operadores, necessarios para serem verificadas na definicao do token
simbolos_operadores = ['*', '.', '/', '+', '-', '>', '=', '<', '!', '&', '|']

# Lista que contem os operadores que trabalham com operacoes numericas
simbolos_operadores_num = ['*', '/', '+', '-', '>', '=', '<']

# Lista que armazenara os erros
lista_erros = []
# Lista que contem a legenda dos tokens, para detalhar melhor o resultado final
legenda_tokens = [[0, 'Espaco em branco, Intervalos de linha, \ n, \ r, \ t'], [1, 'Identificadores'], [2, 'Palavras Reservadas'],
[3, 'Numeros'], [4, 'Cadeia Constante'], [5, 'Caractere Constante'], [6, 'Delimitadores'], [7, 'Operadores'],
[8, 'Comentarios']]

# Declaracao das Variaveis e Iteradores utilizados no codigo
l = 1
coluna = 0
i = 0
erro_geral = False

lexema = ''
tipo_lexema = 0

estado = 0
estado_com = 0
estado_op = 0
estado_caractere = 0
numerico = 1
erro = 0

# Funcoes dos automatos e dos verificadores dos tipos de token
# Funcao dos Identificadores e Palavras Reservadas
def identificadores(atual, prox):
    global lexema
    global tipo_lexema
    global estado
    global l
    global coluna
    global tokens

    global estado_op


    #if (atual.isalpha() or atual.isdigit() or atual == '_') and (prox.isalpha() or prox.isdigit() or prox == '_'):
    #   lexema = lexema + atual
    #else:                                           # TRATAR ERRO DE IDENTIFICADORES AQUI

    lexema = lexema + atual

    if prox.isalpha() or prox.isdigit() or prox == '_':
        lexema = lexema

    elif prox in simbolos_delimitadores or prox.isspace() or prox in simbolos_operadores:

        if len(lexema) > 23:
            erros(atual, prox)

        else:

            if estado_op == 0:

                for palavra in palavras_reservadas:
                    if lexema == palavra:
                        tipo_lexema = 2

                tokens.append([])
                tokens[coluna].append(lexema)
                tokens[coluna].append(tipo_lexema)
                tokens[coluna].append(l)

                estado_op = 0
                coluna += 1
                lexema = ''
                tipo_lexema = 0

            else:
                erros(atual,prox)

    else:
        estado_op = 1

# Funcao dos Numeros
def numeros(atual, prox):
    global lexema
    global tipo_lexema
    global estado
    global l
    global coluna
    global tokens
    global i
    global numerico

    if numerico == 1:

        if atual.isdigit() and (prox.isdigit() or prox == '.'):
            lexema = lexema + atual

        elif atual == '.' and prox.isdigit() and estado < 1:
            lexema = lexema + atual
            estado += 1

        elif atual != '.'  and estado < 2:
            lexema = lexema + atual

            if prox.isspace() or prox == '' or prox == '\r' or prox == '\n' or prox == '\t':
                tokens.append([])
                tokens[coluna].append(lexema)
                tokens[coluna].append(tipo_lexema)
                tokens[coluna].append(l)

                coluna += 1
                lexema = ''

                tipo_lexema = 0
                estado = 0

            elif prox in simbolos_delimitadores:
                tokens.append([])
                tokens[coluna].append(lexema)
                tokens[coluna].append(tipo_lexema)
                tokens[coluna].append(l)

                coluna += 1
                lexema = ''

                tipo_lexema = 0
                estado = 0

            elif prox in simbolos_operadores_num:

                tokens.append([])
                tokens[coluna].append(lexema)
                tokens[coluna].append(tipo_lexema)
                tokens[coluna].append(l)

                coluna += 1
                lexema = ''

                tipo_lexema = 0
                estado = 0

            else:
                numerico = 0

        else:
            lexema = lexema + atual

            if prox.isspace() or prox == '' or prox == '\r' or prox == '\n' or prox == '\t':
                numerico = 1
                erros(atual, prox)
            elif prox in simbolos_delimitadores:
                numerico = 1
                erros(atual, prox)
            elif prox in simbolos_operadores_num:
                numerico = 1
                erros(atual, prox)
            else:
                numerico = 0

    else:
        lexema = lexema + atual

        if prox.isspace() or prox == '' or prox == '\r' or prox == '\n' or prox == '\t':
            numerico = 1
            erros(atual, prox)
        elif prox in simbolos_delimitadores:
            numerico = 1
            erros(atual, prox)
        elif prox in simbolos_operadores_num:
            numerico = 1
            erros(atual, prox)


# Funcao das Cadeias Constantes
def cadeia_constante(atual, prox):
    global lexema
    global tipo_lexema
    global estado
    global l
    global coluna
    global tokens
    global i

    if atual == '"':
        lexema = lexema + atual
        estado += 1

        if estado > 1:
            tokens.append([])
            tokens[coluna].append(lexema)
            tokens[coluna].append(tipo_lexema)
            tokens[coluna].append(l)

            coluna += 1

            estado = 0
            tipo_lexema = 0
            lexema = ''

    elif atual.isalpha != '"':
        lexema = lexema + atual

# Funcao do Caractere Constante
def caractere_constante(atual, prox):
    global lexema
    global tipo_lexema
    global estado
    global l
    global coluna
    global tokens
    global i

    global erro

    global estado_caractere

    if atual == "'" and estado_caractere <= 1:
        lexema = lexema + atual
        estado += 1

        if estado > 1:
            tokens.append([])
            tokens[coluna].append(lexema)
            tokens[coluna].append(tipo_lexema)
            tokens[coluna].append(l)

            coluna += 1

            estado_caractere = 0
            estado = 0
            tipo_lexema = 0
            lexema = ''

    elif atual.isalpha != "'" and estado_caractere <= 1:
        lexema = lexema + atual
        estado_caractere += 1

    elif estado_caractere  > 1:
        erros(atual, prox)

# Funcao dos Delimitadores
def delimitadores(atual):
    global lexema
    global tipo_lexema
    global estado
    global l
    global coluna
    global tokens
    global i

    lexema = atual
    tokens.append([])
    tokens[coluna].append(lexema)
    tokens[coluna].append(tipo_lexema)
    tokens[coluna].append(l)

    coluna += 1

    lexema = ''
    tipo_lexema = 0

# Funcao dos Operadores (EM FASES DE TESTES)
def operadores(atual, prox):
    global lexema
    global tipo_lexema
    global estado
    global estado_op
    global l
    global coluna
    global tokens
    global i

    # Zerando quando vir em seguida o segundo & ou |, para nao armazena-los novamente
    if estado_op == 1:
        estado_op = 0
    # Tratamento para os caracteres *, . e / que sao sempre unidades, como operadores
    elif atual == '*' or atual == '.' or atual == '/':
        lexema = atual
        tokens.append([])
        tokens[coluna].append(lexema)
        tokens[coluna].append(tipo_lexema)
        tokens[coluna].append(l)

        coluna += 1

        estado_op = 0

        lexema = ''
        tipo_lexema = 0         # TRATOR ERRO DE '&' AQUI
    # Tratamento para os caracteres & e | que devem estar sempre em duplas, como operadores
    elif estado_op != 1 and ((atual == '&' and prox == '&') or (atual == '|' and prox == '|')):
        lexema = atual + prox
        tokens.append([])
        tokens[coluna].append(lexema)
        tokens[coluna].append(tipo_lexema)
        tokens[coluna].append(l)

        coluna += 1

        estado_op = 1

        lexema = ''
        tipo_lexema = 0
    # Tratamento de erro para quando os caracteres & e | virem sozinhos
    elif (atual == '&' and prox != '&') or (atual == '|' and prox != '|'):
        lexema = atual

        lista_erros.append('%s caractere invalido, Linha %d' %(lexema, l))

        tipo_lexema = 0
        lexema = ''

    # Tratamento para os caracteres +, - e = que podem vir em duplas ou sozinhos
    elif atual == '+' or atual == '-' or atual == '=':

        if atual == prox:
            lexema = atual + prox
            tokens.append([])
            tokens[coluna].append(lexema)
            tokens[coluna].append(tipo_lexema)
            tokens[coluna].append(l)

            coluna += 1

            estado_op = 1

            lexema = ''
            tipo_lexema = 0
        elif atual != prox and prox == '=':
            lexema = atual + prox
            tokens.append([])
            tokens[coluna].append(lexema)
            tokens[coluna].append(tipo_lexema)
            tokens[coluna].append(l)

            coluna += 1

            estado_op = 1

            lexema = ''
            tipo_lexema = 0
        else:
            lexema = atual
            tokens.append([])
            tokens[coluna].append(lexema)
            tokens[coluna].append(tipo_lexema)
            tokens[coluna].append(l)

            coluna += 1

            estado_op = 0

            lexema = ''
            tipo_lexema = 0
    # Tratamento para os caracteres >, < e ! que podem vir sozinhos ou acompanhados de =
    elif atual == '>' or atual == '<' or atual == '!':

        if atual != prox and prox == '=':
            lexema = atual + prox
            tokens.append([])
            tokens[coluna].append(lexema)
            tokens[coluna].append(tipo_lexema)
            tokens[coluna].append(l)

            coluna += 1

            estado_op = 1

            lexema = ''
            tipo_lexema = 0
        else:
            lexema = atual
            tokens.append([])
            tokens[coluna].append(lexema)
            tokens[coluna].append(tipo_lexema)
            tokens[coluna].append(l)

            coluna += 1

            estado_op = 0

            lexema = ''
            tipo_lexema = 0

    else:
        lexema = ''
        tipo_lexema = 0

# Funcao dos Comentarios
def comentarios(atual, prox):
    global lexema
    global tipo_lexema
    global estado_com
    global l
    global coluna
    global tokens
    global i

    # Tratamento da deteccao de tipo de comentario
    if atual == '/' and estado_com == 0:

        if prox == '/':
            estado_com = 1
        elif prox == '*':
            estado_com = 2
    # Tratamento para quando houver intervalos de linha no comentario
    elif atual == '\r' and prox == '\n':
        # Tratamento para o final dos comentarios de linha
        if estado_com == 1:
            estado_com = 0
            tipo_lexema = 0
            l += 1
        # Tratamento para pulo de linha em comentarios de bloco
        elif estado_com == 2:
            l += 1
    # Tratamento para o final dos comentarios de bloco
    elif atual == '*' and prox == '/'  and estado_com == 2:     # TRATAR ERRO DE COMENTARIO DE BLOCO AQUI
        estado_com = 3
    elif estado_com == 3:
        estado_com = 0
        tipo_lexema = 0
    else:
        tipo_lexema = tipo_lexema

# Funcao dos Espacos em Branco, Tabulacoes e Intervalos de Linha
# Sao ignoradas e definem um novo lexema em branco
def novoLexema(atual, prox):
    global lexema
    global tipo_lexema
    global estado
    global estado_com
    global l
    global coluna
    global tokens
    global i

    if atual == '\r' and prox == '\n':
        lexema = ''
        l += 1
        # tokens.append([])
        # coluna = 0

        if (estado_com != 2 and estado_com != 3):
            tipo_lexema = 0

    elif atual == '':
        tipo_lexema = 0
        lexema = ''
    else:
        tipo_lexema = 0

# Funcao para tratar os erros
def erros(atual, prox):
    global lexema
    global tipo_lexema
    global estado
    global l
    global coluna
    global tokens
    global i

    global erro
    global erro_geral
    global estado_caractere
    global estado_op

    erro_geral = True

    # Tratamento de erro para Identificadores mal formados
    if tipo_lexema == 1:
        #tipo_lexema = 11
        #erro_identificador(atu_x!;al, prox)    ->  EXCLUIDO
        if len(lexema) > 23:
            lista_erros.append('O identificador %s esta muito grande, Linha %d' %(lexema, l))

            estado_op = 0
            estado = 0
            tipo_lexema = 0
            lexema = ''

        else:
            lista_erros.append('O identificador %s apresenta caractere(s) invalido(s), Linha %d' %(lexema, l))

            estado_op = 0
            estado = 0
            tipo_lexema = 0
            lexema = ''

    # Tratamento de erro para Numeros mal formulados (Ex: com mais de 1 ponto '.' para representacao decimal)
    elif tipo_lexema == 3:
        lista_erros.append('O numero %s apresenta caractere(s) invalido(s), Linha %d' %(lexema, l))

        estado = 0
        tipo_lexema = 0
        lexema = ''

    # Tratamento de erro para Caractere Constante com mais de 1 caractere
    elif tipo_lexema == 5:
        lexema = lexema + atual

        if atual == "'":
            lista_erros.append('O caractere constante %s apresenta mais de 1 caractere, Linha %d' %(lexema, l))

            estado_caractere = 0
            estado = 0
            tipo_lexema = 0
            lexema = ''
    # Tratamento de erro para simbolos nao pertencente a linguagem sendo utilizados no inicio dos termos
    # Tratamento de erro para simbolo nao pertecente a linguagem inserido nao acompanhado de numero ou identificador
    elif lexema == '' and prox.isalpha() == False and prox.isdigit() == False and prox != '_':
        lexema = atual
        lista_erros.append('%s caractere invalido, Linha %d' %(lexema, l))

        tipo_lexema = 0
        lexema = ''
    # SE ELE NAO ARMAZENA DE FORMA ISOLADA SIGNIFICA QUE ELE COMECOU UM IDENTIFICADOR OU NUMERO
    # Tratamento de erro para simbolo nao pertecente a linguagem inserido acompanhado de numero ou identificador
    else:
        lexema = lexema + atual

        if (prox.isspace() or prox == '' or prox == '\r' or prox == '\n' or prox == '\t') or prox in simbolos_delimitadores:
            lista_erros.append("O identificador %s apresenta caractere(s) invalido(s), Linha %d" %(lexema, l))
            # LEMBRAR DE TENTAR RETIRAR O ; DO FINAL
            tipo_lexema = 0
            lexema = ''


# Codigo que faz a leitura do arquivo
for linha in arquivo.readlines():

    linhas.append(linha)

    for caractere in linha:

        caracteres.append(caractere)

limite = len(caracteres)
i = 0

# Codigo que vai ler os caracteres de cada linha
# Fazendo a varredura de cada caractere de cada linha do codigo
for c in caracteres:
    # Este verifica se o caractere lido eh o ultimo caractere de todo o codigo
    if i < limite-1:

        if lexema == '' and tipo_lexema != 8:

            if c.isalpha():
                tipo_lexema = 1
                identificadores(c, caracteres[i+1])
            elif c.isdigit():
                tipo_lexema = 3
                numeros(c, caracteres[i+1])
            elif c == '"':
                tipo_lexema = 4
                cadeia_constante(c, caracteres[i+1])
            elif c == "'":
                tipo_lexema = 5
                caractere_constante(c, caracteres[i+1])
            elif c in simbolos_delimitadores:
                tipo_lexema = 6
                delimitadores(c)
            elif c == '/' and (caracteres[i+1] == '/' or caracteres[i+1] == '*'):
                tipo_lexema = 8
                comentarios(c, caracteres[i+1])
            elif c in simbolos_operadores:
                tipo_lexema = 7
                operadores(c, caracteres[i+1])
            elif c.isspace() or c == '' or c == '\r' or c == '\n' or c == '\t':
                tipo_lexema = 0
                novoLexema(c, caracteres[i+1])
            # Tratar erros aqui (verificar simbolos nao pertencentes a linguagem)
            # elif c in
            else:
                tipo_lexema = 10
                erros(c, caracteres[i+1])
                # continue

        else:

            if tipo_lexema == 1:
                identificadores(c, caracteres[i+1])
            elif tipo_lexema == 3:
                numeros(c, caracteres[i+1])
            elif tipo_lexema == 4:
                cadeia_constante(c, caracteres[i+1])
            elif tipo_lexema == 5:
                caractere_constante(c, caracteres[i+1])
            elif tipo_lexema == 6:
                delimitadores(c)
            elif tipo_lexema == 7:
                operadores(c, caracteres[i+1])
            elif tipo_lexema == 8:
                comentarios(c, caracteres[i+1])
            elif tipo_lexema == 0:
                novoLexema(c, caracteres[i+1])
            elif tipo_lexema == 10:
                erros(c, caracteres[i+1])
            else:
                continue

    # Se for o ultimo caractere do codigo eh feito um tratamento diferente
    # para nao exceder o tamanho da lista e dar erro
    else:

        if lexema == '' and tipo_lexema != 8:

            if c.isalpha():
                tipo_lexema = 1
                identificadores(c, c)
            elif c.isdigit():
                tipo_lexema = 3
                numeros(c, c)
            elif c == '"':
                tipo_lexema = 4
                cadeia_constante(c, c)
            elif c == "'":
                tipo_lexema = 5
                caractere_constante(c, c)
            elif c in simbolos_delimitadores:
                tipo_lexema = 6
                delimitadores(c)
            elif tipo_lexema == 8:
                tipo_lexema = 8
                #Tratamento de Erro para comentario de bloco nao fechado
                if estado_com == 2:
                    lista_erros.append('Comentarios de Bloco nao fechado (*/), Linha %d' % l)
                comentarios(c, c)
            elif c in simbolos_operadores:
                tipo_lexema = 7
                operadores(c, c)
            elif c.isspace() or c == '' or c == '\r' or c == '\n' or c == '\t':
                tipo_lexema = 0
                novoLexema(c, c)
            else:
                tipo_lexema = 10
                erros(c, c)

        else:

            if tipo_lexema == 1:
                identificadores(c, c)
            elif tipo_lexema == 3:
                numeros(c, c)
            elif tipo_lexema == 4:
                cadeia_constante(c, c)
                # Tratamento de erro para aspas duplas nao fechada
                if estado == 1:
                    lista_erros.append('Aspas duplas da Cadeia Constante nao fechada ("), Linha %d' % l)
            elif tipo_lexema == 5:
                caractere_constante(c, c)
                # Tratamento de erro para aspas simples nao fechada
                if estado_caractere > 1:
                    lista_erros.append("Aspas simples do Caractere Constante nao fechada ('), Linha %d" % l)
            elif tipo_lexema == 6:
                delimitadores(c)
            elif tipo_lexema == 7:
                operadores(c, c)
            elif tipo_lexema == 8:
                #Tratamento de Erro para comentario de bloco nao fechado
                if estado_com == 2:
                    lista_erros.append('Comentarios de Bloco nao fechado (*/), Linha %d' % l)
                comentarios(c, c)
            elif tipo_lexema == 0:
                novoLexema(c, c)
            elif tipo_lexema == 10:
                erros(c, c)
            else:
                tipo_lexema = 10
                erros(c, c)

    i += 1

# Abrindo arquivo para armazenar a Lista de Tokens
arquivo = open('tokens.txt', 'w')

# Armazenando a Lista de Erros, se existirem
if erro_geral:
    arquivo.write('Foram encontrados alguns Erros Lexicos:\n')

    for linha in lista_erros:
        arquivo.write('%s' % linha)
        arquivo.write('\n')
# Senao eh armazenada a mensagem de sucesso
else:
    arquivo.write('Tokens armazenados com sucesso!\n')

arquivo.write('\n')
# Armazenando a Lista de Tokens
arquivo.write('- Lista de Tokens:\n')
arquivo.write('[Lexema, Token, Linha]' + '\n')
for linha in tokens:
    arquivo.write('%s' % linha)
    arquivo.write('\n')

# Armazenando a Legenda da Tabelas de Tokens
arquivo.write('\n')
arquivo.write('- Tabela de Legenda dos Tokens:\n')
arquivo.write('[Codigo, Token]\n')
for linha in legenda_tokens:
    arquivo.write('%s' % linha)
    arquivo.write('\n')
# Fechando arquivo
arquivo.close()



# Abrindo arquivo para armazenar a Lista de Tokens para Analise Sintatica
arquivo = open('lexia.txt', 'w')

# Armazenando a Lista de Erros, se existirem
##if erro_geral:
##    arquivo.write('Foram encontrados alguns Erros Lexicos:\n')

##    for linha in lista_erros:
##        arquivo.write('%s' % linha)
##        arquivo.write('\n')
# Senao eh armazenada a mensagem de sucesso
##else:
##   arquivo.write('Tokens armazenados com sucesso!\n')

##arquivo.write('\n')
# Armazenando a Lista de Tokens
##arquivo.write('- Lista de Tokens:\n')
##arquivo.write('[Lexema, Token, Linha]' + '\n')
for linha in tokens:
    arquivo.write('%s' % linha)
    arquivo.write('\n')

# Armazenando a Legenda da Tabelas de Tokens
##arquivo.write('\n')
##arquivo.write('- Tabela de Legenda dos Tokens:\n')
##arquivo.write('[Codigo, Token]\n')
##for linha in legenda_tokens:
##    arquivo.write('%s' % linha)
##    arquivo.write('\n')
# Fechando arquivo
arquivo.close()




































# ----------------------------------------------------------------------------------- ANALISE SINTATICA -------------------------------------------------------------------------------------------------------------------------------------

# Adicionando o cifrao('$') para identificar final de codigo
tokens.append([])
tokens[coluna].append('$')
tokens[coluna].append(0)
tokens[coluna].append(l)

# Lendo array da lista de tokens para realizar a analise sintatica
for t in tokens:
    print (t)

# Declarando a pilha do analisador sintatico preditivo sem recursao
pilha = []                                    # Pilha que armazenara as producoes que seguirem corretamente a estrutura gramatical
pilha_comandos = []                 # Como <comandos> podem ser gerados uns dentros dos outros interminavelmente, uma pilha devera ser usada para tal
erros_sintaticos = []                  # Lista que armazenara os erros sintaticos
tipo_producao = []                     # Variavel que armazena os tipo de producao dos varios momentos diferentes

tipo_producao.append('start')        # Posicao [0] do vetor armazena o tipo de producao atual, da producao principal (alguma vinculada ao start)
tipo_producao.append('')                # Posicao [1] do vetor armazena o tipo de producao anterior
tipo_producao.append('')                # Posicao [2] do vetor armazena o tipo de producao intermediario
tipo_producao.append('')

tamanho = len(tokens)             # Variavel que armazena o tamanho da lista de tokens

controle = 0                               # Variavel que ajudara no controle dos tokens para que sigam as producoes da gramatica rigorosamente
controle_comando = []              # Variavel que ajudara no controle das producoes de <comandos> especificamente,
                                                   # porque <comandos> podem ser declarados varios dentro uns dos outros, logo um array dinamico eh necessario para realizar este controle
iterador = -1                                # Variavel para controlar o acesso as posicoes do array 'controle_comando'

novo_tipo = ''                             # Variavel utilizada para armazenar o registro que se tornara um novo tipo primitivo

# Declaracao de listas que armazenam os simbolos terminais (e nao-terminais) da gramatica
start_lista = ['registro', 'constantes', 'variaveis', 'funcao', 'algoritmo']
tipo_primitivo = ['cadeia', 'real', 'inteiro', 'char', 'booleano']
comandos_lista = ['se', 'enquanto', 'para', 'escreva', 'leia']
# Lista dos <comandos> que podem ter <comandos> dentro de si
comandos_producoes = ['se_declaracao', 'senao_declaracao', 'enquanto_declaracao', 'para_declaracao']

# Lista dos operadores relacionais e booleanos
op_relacional = ['<', '>', '=', '==', '!=', '>=', '<=']
op_booleano = ['&&', '||']
op_cont = ['++', '--']

# OBS: Algumas producoes VAZIAS sao tratadas indiretamente

# Declaracao das funcoes das producoes da gramatica
# Funcao da producao 1, a inicial da gramatica e da analise sintatica, <start>
def start(atual, prox):
    global pilha
    global tipo_producao
    global controle

    # controle = 0                                # Ideia para CONTROLAR em caso de ERROS no Registro, Constantes

    #---------------------------------------------------- TRATAR para IMPEDIR a INEXISTENCIA de <ALGORITMO> e <CONSTANTES>
    # Senao houver <constantes> o bloco deve existir vazio, <algoritmo> deve sempre existir e APENAS 1 bloco de <algoritmo>
    # Caso as situacoes acima nao ocorram, imprimir suas respectivas mensagens de erro
    # <VARIAVEIS> DEVEM vir SOMENTE APOS <CONSTANTES>

    if atual[0] == 'registro':
        tipo_producao[0] = 'registro'
        pilha.append(atual)
        # registro_declaracao(atual, prox)

    elif atual[0]  == 'constantes':
        tipo_producao[0] = 'constantes'
        pilha.append(atual)

    elif atual[0] == 'variaveis':
        tipo_producao[0] = 'variaveis'
        tipo_producao[3] = 'start'
        pilha.append(atual)

    elif atual[0] == 'funcao':
        tipo_producao[0] = 'funcao'
        pilha.append(atual)

    elif atual[0] == 'algoritmo':
        tipo_producao[0] = 'algoritmo'
        pilha.append(atual)

    else:
        print('error')


# Funcao da producao 2, <registro_declaracao>
def registro_declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle
    # Essas duas variaveis sao acrescentadas nessa funcao para que o registro se torne um novo tipo primitivo
    global novo_tipo
    global tipo_primitivo

    if  controle == 0:
        if atual[1] == 1:                       # Aqui ja usa como paramentro o tipo do token
            pilha.append(atual)
            controle = 1

            novo_tipo = atual[0]            # O identificador declarado nos registros eh armazenado na variavel 'novo tipo primitivo'

        else:
            erros_sintaticos.append("erro: faltou o identificador após registro")
            controle = 1

            if atual[0] == '{' and (prox[0] in tipo_primitivo or prox[1] == 1):
                pilha.append(atual)
                tipo_producao[0] = 'declaracao_reg'

            elif atual[0] == '{' and prox[0] == ';':
                erros_sintaticos.append("erro: faltou o tipo primitivo")
                erros_sintaticos.append("erro: faltou o identificador")
                pilha.append(atual)
                tipo_producao[0] = 'declaracao_reg'
                controle = 3

            elif atual[0] == '{' and prox[0] == '}':
                pilha.append(atual)
                tipo_producao[0] = 'declaracao_reg'

            elif atual[0] == '{' and prox[0] != '}':
                erros_sintaticos.append("erro: faltou o }")
                pilha.append(atual)
                tipo_producao[0] = 'declaracao_reg'

            elif atual[0] == ';' and prox == '}':
                erros_sintaticos.append("erro: faltou o {")
                erros_sintaticos.append("erro: faltou o tipo primitivo")
                erros_sintaticos.append("erro: faltou o identificador")
                pilha.append(atual)
                controle = 2

            elif atual[0] == ';' and prox[0] == '$':
                erros_sintaticos.append("erro: faltou o {")
                erros_sintaticos.append("erro: faltou o tipo primitivo")
                erros_sintaticos.append("erro: faltou o identificador")
                erros_sintaticos.append("erro: faltou o }")
                pilha.append(atual)

            elif atual[0] == ';':

                erros_sintaticos.append("erro: faltou o {")
                erros_sintaticos.append("erro: faltou o tipo primitivo")
                erros_sintaticos.append("erro: faltou o identificador")
                pilha.append(atual)

                if prox[0] in tipo_primitivo:
                    tipo_producao[0] = 'declaracao'
                    tipo_producao[1] = 'declaracao_reg'
                    controle = 1

                elif prox[1] == 1:
                    tipo_producao[0] = 'declaracao'
                    tipo_producao[1] = 'declaracao_reg'
                    controle = 2

                elif prox[0] == '}':
                    controle = 2

                else:
                    erros_sintaticos.append("erro: faltou o }")
                    erros_sintaticos.append("erro: isso não devia estar aqui!")
                    tipo_producao[0] = 'start'
                    controle = 0


            elif atual[0] == '}':
                erros_sintaticos.append("erro: faltou o {")
                pilha.append(atual)
                tipo_producao[0] = 'declaracao_reg'

    elif controle == 1:
        if atual[0] == '{':
            pilha.append(atual)
            tipo_producao[0] = 'declaracao_reg'
            controle = 1

        else:
            erros_sintaticos.append("erro: faltou o {")
            tipo_producao[0] = 'declaracao_reg'
            controle = 1

            if atual[0] == ';':
                erros_sintaticos.append("erro: faltou o tipo primitivo")
                erros_sintaticos.append("erro: faltou o identificador")
                tipo_producao[0] = 'declaracao_reg'
                controle = 3
                declaracao_reg(atual,prox)

    elif controle == 2:
        if atual[0] == '}':
            pilha.append(atual)
            tipo_primitivo.append(novo_tipo)        # Com a estrutura do registro sendo corretamente seguida e finalizada
                                                                          # o novo tipo primitivo eh adicionado na lista de 'tipos primitivos', se tornando definitivamente um
            tipo_producao[0] = 'start'
            controle = 0

        else:
            erros_sintaticos.append("erro: faltou o }")
            tipo_producao[0] = 'start'
            controle = 0
            start(atual,prox)

    else:
        print('error registro_declaracao')

# Funcao da producao 4, <declaracao_reg>
def declaracao_reg(atual, prox):
    global pilha
    global tipo_producao
    global controle

    if atual[0] in tipo_primitivo and controle == 1:
        tipo_producao[0] = 'declaracao'
        tipo_producao[1] = 'declaracao_reg'
        controle = 1
        declaracao(atual, prox)

    elif atual[1] == 1 and controle == 1:
        controle = 2
        tipo_producao[0] = 'declaracao'
        tipo_producao[1] = 'declaracao_reg'
        declaracao(atual, prox)

    elif atual[0] == ';' and controle == 1:
        erros_sintaticos.append("erro: faltou o tipo primitivo")
        erros_sintaticos.append("erro: faltou o identificador")

        if prox[0] == '}':
            tipo_producao[0] = 'registro'
            controle = 2

    elif controle == 3:

        if atual[0] == ';':
            pilha.append(atual)

            if prox[0] in tipo_primitivo:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_reg'
                controle = 1

            elif prox[1] == 1:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_reg'
                controle = 2

            elif prox[0] == '}':
                tipo_producao[0] = 'registro'
                tipo_producao[1] = ''
                controle = 2

            else:
                print("erro: isso não devia estar aqui!")
                tipo_producao[0] = 'registro'
                tipo_producao[1] = ''
                controle = 2

        elif atual[0] in tipo_primitivo:
            erros_sintaticos.append("erro: faltou o ;")
            tipo_producao[0] = 'declaracao'
            tipo_producao[1] = 'declaracao_reg'
            controle = 1
            declaracao(atual,prox)

        elif atual[1] == 1:
            erros_sintaticos.append("erro: faltou o ;")
            tipo_producao[0] = 'declaracao'
            tipo_producao[1] = 'declaracao_reg'
            controle = 2
            declaracao(atual,prox)

        elif prox[0] == ';':
            erros_sintaticos.append("erro: faltou o ;")
            controle = 3

        elif atual[0] == '}':
            erros_sintaticos.append("erro: faltou o ;")
            tipo_producao[0] = 'registro'
            tipo_producao[1] = ''
            controle = 2
            registro_declaracao(atual, prox)

        else:
            erros_sintaticos.append("erro: faltou o ;")

            if atual[0] in start_lista:
                controle = 0
                erros_sintaticos.append("erro: faltou o }")
                tipo_producao[0] = 'start'
                start(atual,prox)


            elif prox[0] in tipo_primitivo:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_reg'
                controle = 1


            elif prox[1] == 1:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_reg'
                controle = 2

            else:
                tipo_producao[0] = 'registro'
                tipo_producao[1] = ''
                controle = 2

    # Tratamento para o caso da producao <declaracao_reg> ser vazia
    elif atual[0] == '}' and controle == 1:
        controle = 2
        tipo_producao[0] = 'registro'
        tipo_producao[1] = ''
        registro_declaracao(atual, prox)

    else:
        print('error declaracao_reg')

# Funcao da producao 6, <declaracao>
def declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle

    if atual[0] in tipo_primitivo and controle == 1:
        pilha.append(atual)
        controle = 2

        if prox[1] == 1 and controle == 2:
            pilha.append(prox)
            controle = 3
            #tipo_producao[0] = tipo_producao[1]

        else:
            erros_sintaticos.append("erro: faltou o identificador")
            controle = 3
            tipo_producao[0] = tipo_producao[1]


    elif atual[1] == 1 and controle == 2:
        erros_sintaticos.append("erro: faltou o tipo primitivo")
        pilha.append(atual)
        controle = 3
        tipo_producao[0] = tipo_producao[1]

    elif atual[1] == 1 and controle == 3:
        tipo_producao[0] = tipo_producao[1]

        if tipo_producao[2] == 'constantes' and prox[0] == '$':
            erros_sintaticos.append("erro: faltou o =")
            erros_sintaticos.append("erro: faltou o valor primitivo")
            erros_sintaticos.append("erro: faltou o ;")
            erros_sintaticos.append("erro: faltou o }")

        elif prox[0] == '$':
            erros_sintaticos.append("erro: faltou o ;")
            erros_sintaticos.append("erro: faltou o }")

    else:
        print('error declaracao')

# Funcao da producao 12, <constantes_declaracao>
def constantes_declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle

    if controle == 0:
        if atual[0] == '{':
            pilha.append(atual)
            tipo_producao[0] = 'declaracao_const'
            controle = 1                                                # COMENTAR?
        else:
            erros_sintaticos.append("erro: faltou o {")
            tipo_producao[0] = 'declaracao_const'
            controle = 1                                                # COMENTAR?

    elif controle == 2:          # ALTERAR?
        if atual[0] == '}':
            pilha.append(atual)
            tipo_producao[0] = 'start'
            controle = 0
        else:
            erros_sintaticos.append("erro: faltou o }")
            tipo_producao[0] = 'start'
            controle = 0
            start(atual,prox)

    else:
        print('error constantes_declaracao')

# Funcao da producao 13, <declaracao_const>
def declaracao_const(atual, prox):
    global pilha
    global tipo_producao
    global controle

    if controle == 1:

        if atual[0] in tipo_primitivo:
            tipo_producao[0] = 'declaracao'
            tipo_producao[1] = 'declaracao_const'
            controle = 1
            declaracao(atual, prox)

        elif atual[1] == 1:
            tipo_producao[0] = 'declaracao'
            tipo_producao[1] = 'declaracao_const'
            controle = 2
            declaracao(atual, prox)

        elif atual[0] == '=':
            erros_sintaticos.append("erro: faltou o tipo primitivo")
            erros_sintaticos.append("erro: faltou o identificador")
            pilha.append(atual)
            controle = 4

        elif isvalorprimitivo(atual):
            erros_sintaticos.append("erro: faltou o tipo primitivo")
            erros_sintaticos.append("erro: faltou o identificador")
            erros_sintaticos.append("erro: faltou o =")
            pilha.append(atual)
            controle = 5

        elif atual[0] == ';':
            erros_sintaticos.append("erro: faltou o tipo primitivo")
            erros_sintaticos.append("erro: faltou o identificador")
            erros_sintaticos.append("erro: faltou o =")
            erros_sintaticos.append("erro: faltou o valor primitivo")
            pilha.append(atual)

            if prox[0] in tipo_primitivo:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_const'
                controle = 1
            else:
                tipo_producao[0] = 'constantes'
                tipo_producao[1] = ''
                controle = 2

        elif atual[0] == '}':
            tipo_producao[0] = 'constantes'
            tipo_producao[1] = ''
            controle = 2
            constantes_declaracao(atual, prox)

        else:
            erros_sintaticos.append("erro: isso não deveria estar aqui!")

################################## -----------------------------------ANALISAR AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII?''''''''''''''''''''''''''''-----------------------------------
    elif controle == 3:
        if  atual[0] == '=':
            pilha.append(atual)
            controle = 4

        elif isvalorprimitivo(atual):
            erros_sintaticos.append("erro: faltou o =")
            pilha.append(atual)
            controle = 5

        elif atual[0] == ';':                         # ALTERAR O TIPO DE CONTROLE AQUI?
            erros_sintaticos.append("erro: faltou o =")
            erros_sintaticos.append("erro: faltou o valor primitivo")
            pilha.append(atual)

            if prox[0] in tipo_primitivo:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_const'
                controle = 1
            else:
                tipo_producao[0] = 'constantes'
                tipo_producao[1] = ''
                controle = 2

        elif atual[0] == '}':
            erros_sintaticos.append("erro: faltou o =")
            erros_sintaticos.append("erro: faltou o valor primitivo")
            erros_sintaticos.append("erro: faltou o ;")
            tipo_producao[0] = 'constantes'
            tipo_producao[1] = ''
            controle = 2
            constantes_declaracao(atual, prox)

        else:
            erros_sintaticos.append("erro: faltou o =")
            erros_sintaticos.append("erro: faltou o valor primitivo")
            erros_sintaticos.append("erro: faltou o ;")

            if atual[0] in tipo_primitivo:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_const'
                controle = 1
                declaracao(atual, prox)

            elif atual[1] == 1:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_const'
                controle = 2
                declaracao(atual, prox)

            else:
                erros_sintaticos.append("erro: isso não deveria estar aqui!")

################################## -----------------------------------ANALISAR AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII'?'''''''''''''''''''''''''''-----------------------------------
    elif controle == 4:
        if isvalorprimitivo(atual):
            pilha.append(atual)
            controle = 5

        elif atual[0] == ';':
            erros_sintaticos.append("erro: faltou o valor primitivo")
            pilha.append(atual)

            if prox[0] in tipo_primitivo:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_const'
                controle = 1
            else:
                tipo_producao[0] = 'constantes'
                tipo_producao[1] = ''
                controle = 2

        elif atual[0] == '}':
            erros_sintaticos.append("erro: faltou o valor primitivo")
            erros_sintaticos.append("erro: faltou o ;")
            tipo_producao[0] = 'constantes'
            tipo_producao[1] = ''
            controle = 2
            constantes_declaracao(atual, prox)

        else:
            erros_sintaticos.append("erro: faltou o valor primitivo")
            erros_sintaticos.append("erro: faltou o ;")

            if atual[0] in tipo_primitivo:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_const'
                controle = 1
                declaracao(atual, prox)

            elif atual[1] == 1:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_const'
                controle = 2
                declaracao(atual, prox)

            else:
                erros_sintaticos.append("erro: isso não deveria estar aqui!")

    elif controle == 5:                         # ALTERAR O TIPO DE CONTROLE AQUI?

        if atual[0] == ';':
            pilha.append(atual)
            tipo_producao[0] = 'constantes'
            tipo_producao[1] = ''
            controle = 2

        else:
            erros_sintaticos.append("erro: faltou o ;")

            if atual[0] in tipo_primitivo:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_const'
                controle = 1
                declaracao(atual, prox)

            elif atual[1] == 1:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_const'
                controle = 2
                declaracao(atual, prox)

            elif atual[0] == '}':
                tipo_producao[0] = 'constantes'
                tipo_producao[1] = ''
                controle = 2
                constantes_declaracao(atual, prox)

            elif prox[0] in tipo_primitivo:
                tipo_producao[0] = 'declaracao'
                tipo_producao[1] = 'declaracao_const'
                controle = 1

            else:
                erros_sintaticos.append("erro: isso não deveria estar aqui!")
                tipo_producao[0] = 'constantes'
                tipo_producao[1] = ''
                controle = 2

    else:
        print('error declaracao_const')

# Funcao da producao 15, <valor_primitivo>
# Verifica se o parametro passado eh um valor primitivo, se sim, retorna 'true', senao retorna 'false'
def isvalorprimitivo(parametro):
    return parametro[1] == 3 or parametro[1] == 4 or parametro[1] == 5 or parametro[0] == 'verdadeiro' or parametro[0] == 'falso'

# Funcao da producao 21, <variaveis_declaracao>
def variaveis_declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle

    if atual[0] == '{' and controle == 0:
        pilha.append(atual)
        tipo_producao[0] = 'declaracao_var'
        controle = 1

        if prox[0] == '$':
            erros_sintaticos.append("erro: faltou o }")

    elif atual[0] == '}' and controle == 2:
        pilha.append(atual)
        tipo_producao[0] = 'start'

        if tipo_producao[0] == 'start':
            controle = 0
        elif tipo_producao[0] == 'funcao':
            controle = 7

    elif atual[0] != '{' and controle == 0:
        tipo_producao[0] = 'declaracao_var'
        controle = 1
        erros_sintaticos.append("erro: faltou o {")
        declaracao_var(atual, prox)

    elif atual[0] != '}' and controle == 2:
        tipo_producao[0] = 'start'
        controle = 0
        erros_sintaticos.append("erro: faltou o }")

# Funcao da producao 22, <declaracao_var>
def declaracao_var(atual, prox):
    global pilha
    global tipo_producao
    global controle

    # Estrutura de condicao para decidir se fico na producao 22: <declaracao> <identificador_deriva>; <declaracao_var>
    if atual[0] in tipo_primitivo and controle == 1:
        tipo_producao[0] = 'declaracao'
        tipo_producao[1] = 'declaracao_var'                 #ATENCAO: PODER HAVER ERRO AQUI EM CASO DE BUGS
        #controle = 1
        declaracao(atual, prox)

        if prox[0] == '$':
            erros_sintaticos.append("erro: faltou o ;")
            erros_sintaticos.append("erro: faltou o }")

    # ou vou para producao 23: token_identificador token_identificador; <declaracao_var>
    elif atual[1] == 1 and (controle == 1 or controle == 2):

        if controle == 1:
            pilha.append(atual)
            controle = 2
            tipo_producao[0] = 'declaracao'
            tipo_producao[1] = 'declaracao_var'                 #ATENCAO: PODER HAVER ERRO AQUI EM CASO DE BUGS
            declaracao(atual, prox)

            if prox[0] == '$':
                erros_sintaticos.append("erro: faltou o ;")
                erros_sintaticos.append("erro: faltou o }")

        elif controle == 2:
            pilha.append(atual)
            controle = 8

        else:
            print('error')

    elif atual[0] == ';' and controle == 1:
        erros_sintaticos.append("erro: faltou o tipo primitivo")
        erros_sintaticos.append("erro: faltou o identificador")

        if prox[0] == '$':
            erros_sintaticos.append("erro: faltou o }")

        # Tratamento para o caso da producao <declaracao_var> ser vazia
    elif atual[0] == '}' and controle == 1:
        controle = 2
        tipo_producao[0] = 'variaveis'
        tipo_producao[1] = ''
        variaveis_declaracao(atual, prox)

    elif controle == 3:                                     # Logica e tratamento um pouco diferente para 'identificador_deriva', mas muito funcional
        tipo_producao[1] = 'declaracao_var'    #NÃO PRECISA, DEPOIS DE TESTAR TIRAR
        tipo_producao[0] = 'identificador_deriva'

        if atual[0] == '[':
            controle = 4
            identificador_deriva(atual, prox)

        elif atual[0] == '=':
            controle = 7
            identificador_deriva(atual, prox)

        elif isvalorprimitivo(atual):
            controle = 3
            tipo_producao[0] = 'declaracao_var'

        elif atual[0] == ';':
            controle = 8

            if (prox[0] == '$'):
                erros_sintaticos.append("erro: faltou o }")

            declaracao_var(atual,prox)

        else:
            erros_sintaticos.append("erro: faltou o ;")
            controle = 8
            declaracao_var(atual,prox) #CONSERTAR ESSE BUG LOUCO AQUI MAIS TARDE!!!


    elif atual[0] == ';' or controle == 8:
        pilha.append(atual)

        if atual[0] in tipo_primitivo or atual[1] == 1:
            tipo_producao[0] = 'declaracao_var'
            controle = 1
            declaracao_var(atual, prox)

        if prox[0] in tipo_primitivo or prox[1] == 1:
            tipo_producao[0] = 'declaracao_var'
            controle = 1

        elif atual[0] == ';':
            controle = 8

        elif prox[0] == ';':
            controle = 8

        elif prox[0] == '}':
            erros_sintaticos.append("erro: faltou o ;")
            tipo_producao[0] = 'variaveis'
            tipo_producao[1] = ''
            tipo_producao[2] = ''
            controle = 2

        elif (atual[0] in tipo_primitivo or atual[1] == 1) and prox[0] == '$':
            erros_sintaticos.append("erro: faltou o ;")
            tipo_producao[0] = 'variaveis'
            tipo_producao[1] = ''
            tipo_producao[2] = ''
            controle = 2
            variaveis_declaracao(atual,prox)

        else:
            tipo_producao[0] = 'variaveis'
            tipo_producao[1] = ''
            tipo_producao[2] = ''
            controle = 2

    else:
        print('error declaracao_var')

# Funcao da producao 25, <identificador_deriva>
def identificador_deriva(atual, prox):
    global pilha
    global tipo_producao
    global controle

    if atual[0] == '[' and controle == 4:                                     # and controle == 3?
        tipo_producao[0] = 'matriz'
        tipo_producao[1] = 'identificador_deriva'
        tipo_producao[2] = 'declaracao_var'
        controle = 4
        matriz(atual, prox)

    elif atual[0] == '=' and controle == 7:                                 # and controle == 3?
        pilha.append(atual)

        if isvalorprimitivo(prox):
            tipo_producao[0] = 'declaracao_var'
            controle = 3

        else:
            erros_sintaticos.append("erro: faltou o tipo primitivo da inicialização")
            tipo_producao[0] = 'declaracao_var'
            controle = 8

    else:
        print('error identificador_deriva')

# Funcao da producao 28, <matriz>
def matriz(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    if atual[0] == '[' and controle == 4:
        pilha.append(atual)
        controle = 5

    elif type(int(atual[1])) and controle == 5:
        pilha.append(atual)
        controle = 6

    elif atual[0] == ']' and controle == 6:
        pilha.append(atual)

        if prox[0] == '[':
            controle = 4

        elif prox[0] == ';':
            tipo_producao[0] = 'declaracao_var'
            controle = 8

        # Significa que veio de <fator> em seguida voltar para <exp_simples> e deve vir <fator_deriva> em seguida
        elif (prox[0] == '*' or prox[0] == '/' or prox[0] == '+'  or prox[0] == '-' or prox[0] in op_relacional) and (controle_comando[iterador] == 4 and pilha_comandos.pop() == 'fator'):
            controle = 7

            # Depois de pegar a possivel <matriz> encerra <fator> e volta para <exp_simples>
            iterador -= 1
            controle_comando.pop()
            tipo_producao[0] = pilha_comandos.pop()

        else:
            erros_sintaticos.append("error: faltou o ;")
            tipo_producao[0] = 'declaracao_var'
            controle = 8

    else:
        print('error')

# Funcao da producao 32, <funcao_declaracao>
def funcao_declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global pilha_comandos

    # Condicao feita para a producao 46, <tipo_return>
    if controle == 0:

        if (atual[0] in tipo_primitivo or atual[0] == 'vazio'):
            pilha.append(atual)
            controle = 1

        else:
            erros_sintaticos.append("erro: faltou o tipo de retorno")
            controle = 1
            funcao_declaracao(atual,prox)

    elif controle == 1:

        if atual[1] == 1:
            pilha.append(atual)
            controle = 2

        else:
            erros_sintaticos.append("erro: faltou o identificador da função")
            controle = 2
            funcao_declaracao(atual,prox)


    elif controle == 2:

        if atual[0] == '(':
            pilha.append(atual)
            controle = 3

        else:
            erros_sintaticos.append("erro: faltou o (")
            controle = 3
            funcao_declaracao(atual,prox)

    elif controle == 3:

        if atual[0] in tipo_primitivo or atual[0] == 'registro':
            tipo_producao[0] = 'decl_param'
            tipo_producao[1] = 'funcao'
            controle = 1
            decl_param(atual, prox)

        else:
            erros_sintaticos.append("erro: faltou o tipo primitivo")
            tipo_producao[0] = 'decl_param'
            tipo_producao[1] = 'funcao'
            controle = 1
            decl_param(atual, prox)

    elif controle == 5:
        if atual[0] == ')':
            pilha.append(atual)
            controle = 6

        else:
            erros_sintaticos.append("erro: faltou o )")
            controle = 6
            funcao_declaracao(atual,prox)

    elif controle == 6:
        if atual[0] == '{':
            pilha.append(atual)
            controle = 7

        else:
            erros_sintaticos.append("erro: faltou o {")
            controle = 7
            funcao_declaracao(atual,prox)


    elif atual[0] == 'variaveis' and controle == 7:
        pilha.append(atual)
        controle = 0
        tipo_producao[0] = 'variaveis'
        tipo_producao[3] = 'funcao'
    # Mantendo controle = 7 mesmo entrando em P(21) <variaveis_declaracao>, trata o caso da propria P(21) ser vazia
    # e seguir para a producao alternativa P(43)

    # Verifica se o token atual eh um comando
    elif controle == 7:

        if (atual[0] in comandos_lista or atual[1] == 1):
            tipo_producao[3] = 'funcao'
            pilha_comandos.append('funcao')
            controle = 7

            tipo_producao[0] = 'comandos'
            # Chama a funcao da producao P(56), <comandos>
            comandos(atual,prox)

        else:
            erros_sintaticos.append("erro: faltaram os comandos")
            tipo_producao[3] = 'funcao'
            pilha_comandos.append('funcao')
            controle = 7

            tipo_producao[0] = 'comandos'
            # Chama a funcao da producao P(56), <comandos>
            comandos(atual,prox)

    # Mantendo controle = 7 mesmo entrando em P(42) ou P(43), trata o caso da P(44) <decl_comandos> ser vazia
    elif atual[0] == 'retorno' and controle == 7:
        pilha.append(atual)
        controle = 8

    # Tratamento para a producao P(49), <return_deriva>
    elif (isvalorprimitivo(atual) or atual[0] == 'vazio' or atual[1] == 1) and controle == 8:
        pilha.append(atual)

        if isvalorprimitivo(atual) or atual[0] == 'vazio':
            controle = 9
        elif atual[1] == 1:

            if prox[0] == '[':
                tipo_producao[0] = 'identificador_param_deriva'                     # PODE SER VAZIA
                tipo_producao[1] = 'funcao'
                controle = 1

            else:
                controle = 9

        else:
            print('error')

    # Tratamento para o ';' no final do retorno
    elif atual[0] == ';' and controle == 9:
        pilha.append(atual)
        controle = 10

    # Encontrando a ultima chave, finaliza a <funcao>
    elif atual[0] == '}' and controle == 10:
        pilha.append(atual)
        tipo_producao[0] = 'start'
        controle = 0
    # A funcao <start> trata bem a possibilidade de haver outro bloco de <funcao>, ou seja, vir um <funcao_declaracao>,
    # apos esta ter encerrada sua declaracao

    else:
        print('error')

# Funcao da producao 34, <decl_param>
def decl_param(atual, prox):
    global pilha
    global tipo_producao
    global controle

    if atual[0] in tipo_primitivo  and controle == 1:
        tipo_producao[0] = 'declaracao'
        tipo_producao[1] = 'decl_param'
        tipo_producao[2] = 'funcao'
        declaracao(atual, prox)

    elif atual[0] == '[' and controle == 3:
        tipo_producao[0] = 'identificador_param_deriva'                     # PODE SER VAZIA
        tipo_producao[1] = 'decl_param'
        tipo_producao[2] = 'funcao'
        controle = 1
        identificador_param_deriva(atual, prox)
    # Tratamento para producao 36, <deriva_param>
    elif atual[0] == ',' and controle == 3:
        pilha.append(atual)
        tipo_producao[0] = 'decl_param'
        controle = 1

# Nos proximos dois 'elif's' o Tratamento para a producao alternativa de <decl_param>, P(35) 'registro token_identificador <deriva_param>'
    elif atual[0] == 'registro' and controle == 1:
        pilha.append(atual)
        controle = 4

    elif atual[1] == 1 and controle == 4:
        pilha.append(atual)
        controle = 1

    # Tratamento para quando as producoes <identificador_param_deriva> e/ou <deriva_param> sao VAZIAS
    # ou <decl_param> chega ao final
    elif controle == 3:

        if(prox[0] == ')'):
            tipo_producao[0] = 'funcao'
            controle = 5
        else:
            print('error')

    else:
        print('error')

# Funcao das producoes 38 e 40, <identificador_param_deriva> e <matriz_param>, respectivamente
# Foram feitas juntas para nao ficar redundante
def identificador_param_deriva(atual, prox):
    global pilha
    global tipo_producao
    global controle

    if atual[0] == '[' and controle == 1:
        pilha.append(atual)
        controle = 2

    elif atual[0] == ']' and controle == 2:
        pilha.append(atual)

        if prox[0] == '[':
            controle = 1

        else:

            tipo_producao[0] = tipo_producao[1]

            if tipo_producao[1] == 'decl_param':
                controle = 3
            elif tipo_producao[1] == 'funcao':
                controle = 9
            # NAO precisa pra <algoritmo>, mas talvez precise pra <enquanto> ou <para>
            #elif tipo_producao[1] == 'algoritmo':
            #   controle = 2

    else:
        print('error')

# Funcao das producoes P(44) e P(56), <decl_comandos> e <comandos>, respectivamente
# Feita juntas para nao haver redundancias desnecessarias no codigo
def comandos(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    # Verifica qual comando eh para direciona-lo
    if atual[0] == 'se':
        pilha.append(atual)

        pilha_comandos.append('comandos')
        controle_comando.append(0)
        iterador += 1

        tipo_producao[0] = 'se_declaracao'
        tipo_producao[1] = 'comandos'               # ------ NAO precisa DISSO AQUI em CADA condicao, mas tudo bem, vamos deixa-lo ai

    elif atual[0] == 'enquanto':
        pilha.append(atual)

        pilha_comandos.append('comandos')
        controle_comando.append(0)
        iterador += 1

        tipo_producao[0] = 'enquanto_declaracao'
        tipo_producao[1] = 'comandos'

    elif atual[0] == 'para':
        pilha.append(atual)

        pilha_comandos.append('comandos')
        controle_comando.append(0)
        iterador += 1

        tipo_producao[0] = 'para_declaracao'
        tipo_producao[1] = 'comandos'

    elif atual[0] == 'escreva':
        pilha.append(atual)

        pilha_comandos.append('comandos')
        controle_comando.append(0)
        iterador += 1

        tipo_producao[0] = 'escreva_declaracao'
        tipo_producao[1] = 'comandos'

    elif atual[0] == 'leia':
        pilha.append(atual)

        pilha_comandos.append('comandos')
        controle_comando.append(0)
        iterador += 1

        tipo_producao[0] = 'leia_declaracao'
        tipo_producao[1] = 'comandos'

    elif atual[1] == 1:
        pilha.append(atual)

        pilha_comandos.append('comandos')
        controle_comando.append(0)
        iterador += 1

        tipo_producao[0] = 'exp_aritmetica'
        tipo_producao[1] = 'comandos'

    # Quando um comando terminar (com '}' ou ';'), verifica se ha outro ou se volta para producao anterior
    elif atual[0] == '}' or atual[0] == ';':
        pilha.append(atual)
        # Apos encerrar <comandos> verifica-se em qual producao <comandos> encontra-se dentro para retornar a ela
        # Verificando se o comando atual encontra-se dentro de outro comando
        if pilha_comandos[-1] in comandos_producoes:
            tipo_producao[0] = pilha_comandos.pop()

        # Verifica se o comando atual encontra-se dentro de uma <funcao>
        elif pilha_comandos[-1] == 'funcao':
            tipo_producao[0] = pilha_comandos.pop()
            # pilha_comandos.clear()
            controle = 7

        # Verifica se o comando atual encontra-se dentro de <algoritmo>
        elif pilha_comandos[-1] == 'algoritmo':
            tipo_producao[0] = pilha_comandos.pop()
            # pilha_comandos.clear()
            controle = 2

        else:
            print('error')

    else:
        print('error')

# Funcao da producao P(62), <se_declaracao>
def se_declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    if atual[0] == '(' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 1

    # Chamando a producao P(85), <exp_rel_bol> que inicia com P(97) <exp_simples>
    elif (atual[0] == '+' or atual[0] == '-' or atual[1] == 1 or atual[0].isdigit() or atual[0] == '(') and controle_comando[iterador] == 1:
        controle_comando[iterador] = 2

        pilha_comandos.append('se_declaracao')
        tipo_producao[0] = 'exp_simples'

        iterador += 1
        controle_comando.append(0)
        exp_simples(atual, prox)

    # Tratamento para as producoes P(88) e P(92), <op_relacional> e <op_rel_deriva>, respectivamente
    elif atual[0] in op_relacional and controle_comando[iterador] == 2:
        pilha.append(atual)
        controle_comando[iterador] = 3

    # Chamando a producao P(97), <exp_simples>, novamente por vir depois de <op_relacional>
    elif (atual[0] == '+' or atual[0] == '-' or atual[1] == 1 or atual[0].isdigit() or atual[0] == '(') and controle_comando[iterador] == 3:
        controle_comando[iterador] = 4

        pilha_comandos.append('se_declaracao')
        tipo_producao[0] = 'exp_simples'

        iterador += 1
        controle_comando.append(0)
        exp_simples(atual, prox)

    # <exp_rel_deriva>, P(86) comeca aqui
    # Tratamento para a producoes P(94), <op_booleano>
    elif atual[0] in op_booleano and controle_comando[iterador] == 4:
        pilha.append(atual)
        controle_comando[iterador] = 4

    # Chamando a producao P(97), <exp_simples>, novamente por vir depois de <op_booleano>
    elif (atual[0] == '+' or atual[0] == '-' or atual[1] == 1 or atual[0].isdigit() or atual[0] == '(') and controle_comando[iterador] == 4:
        controle_comando[iterador] = 5

        pilha_comandos.append('se_declaracao')
        tipo_producao[0] = 'exp_simples'

        iterador += 1
        controle_comando.append(0)
        exp_simples(atual, prox)

    # Chamando novamente P(88), <op_relacional> apos o <exp_simples>
    elif atual[0] in op_relacional and controle_comando[iterador] == 5:
        pilha.append(atual)
        controle_comando[iterador] = 6

    # Novamente vem um <exp_simples> apos um <op_relacional>
    elif (atual[0] == '+' or atual[0] == '-' or atual[1] == 1 or atual[0].isdigit() or atual[0] == '(') and controle_comando[iterador] == 6:
        controle_comando[iterador] = 7

        pilha_comandos.append('se_declaracao')
        tipo_producao[0] = 'exp_simples'

        iterador += 1
        controle_comando.append(0)
        exp_simples(atual, prox)

    # Caso <exp_rel_deriva> seja vazia, finaliza <exp_rel_bol> (controle_comando[iterador] == 4)
    # Com a <exp_rel_deriva> nao sendo vazia e finalizando <exp_rel_bol> (controle_comando[iterador] == 4)
    elif atual[0] == ')' and (controle_comando[iterador] == 4 or controle_comando[iterador] == 7):
        pilha.append(atual)
        controle_comando[iterador] = 8

    elif atual[0] == '{' and controle_comando[iterador] == 8:
        pilha.append(atual)
        controle_comando[iterador] = 9

    # Verificando se ha <comandos> dentro do <se>
    elif (atual[0] in comandos_lista or atual[1] == 1) and controle_comando[iterador] == 8:
        pilha_comandos.append('se_declaracao')

        tipo_producao[0] = 'comandos'
        # Chama a funcao da producao P(56), <comandos>
        comandos(atual,prox)

    # Encerrando o comando 'se' da producao P(62), <se_declaracao>, no caso de haver comando 'senao'
    elif atual[0] == '}' and prox[0] == 'senao' and controle_comando[iterador] == 8:
        pilha.append(atual)

        iterador -= 1
        controle_comando.pop()

        iterador += 1
        controle_comando.append(0)

        tipo_producao[0] = 'senao_declaracao'

    # Encerrando o comando 'se' da producao P(62), <se_declaracao>, no caso de nao haver comando 'senao' ('senao' ser vazio)
    elif atual[0] == '}' and controle_comando[iterador] == 8:
        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

        comandos(atual, prox)

    else:
        print('error')

# DICA: 'senao' eh um 'se' sem condicao
# ENCERRAR 'senao' da mesma forma que encerra 'se' quando nao ha 'senao' logo depois
# Funcao da producao P(63), <senao_declaracao>
def senao_declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    if atual[0] == 'senao' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 1

    if atual[0] == '{' and controle_comando[iterador] == 1:
        pilha.append(atual)
        controle_comando[iterador] = 2

    # Verificando se ha <comandos> dentro do <senao>
    elif (atual[0] in comandos_lista or atual[1] == 1) and controle_comando[iterador] == 2:
        pilha_comandos.append('senao_declaracao')

        tipo_producao[0] = 'comandos'
        # Chama a funcao da producao P(56), <comandos>
        comandos(atual,prox)

    # Mantedo a condicao com 'controle_comando[iterador] == 2' trato no caso de nao haver <comandos> dentro do <senao>
    # Encerrando o comando 'senao' da producao P(63), <senao_decl>
    elif atual[0] == '}' and controle_comando[iterador] == 2:
        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

        comandos(atual, prox)

    else:
        print('error')


# DICA: A estrutura do <enquanto_declaracao> eh igualzinha a do <se_declaracao>, mas sem o <senao_declaracao>
# Funcao da producao P(65), <enquanto_declaracao>
def enquanto_declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    if atual[0] == '(' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 1

    # Chamando a producao P(85), <exp_rel_bol> que inicia com P(97) <exp_simples>
    elif (atual[0] == '+' or atual[0] == '-' or atual[1] == 1 or atual[0].isdigit() or atual[0] == '(') and controle_comando[iterador] == 1:
        controle_comando[iterador] = 2

        pilha_comandos.append('enquanto_declaracao')
        tipo_producao[0] = 'exp_simples'

        iterador += 1
        controle_comando.append(0)
        exp_simples(atual, prox)

    # Tratamento para as producoes P(88) e P(92), <op_relacional> e <op_rel_deriva>, respectivamente
    elif atual[0] in op_relacional and controle_comando[iterador] == 2:
        pilha.append(atual)
        controle_comando[iterador] = 3

    # Chamando a producao P(97), <exp_simples>, novamente por vir depois de <op_relacional>
    elif (atual[0] == '+' or atual[0] == '-' or atual[1] == 1 or atual[0].isdigit() or atual[0] == '(') and controle_comando[iterador] == 3:
        controle_comando[iterador] = 4

        pilha_comandos.append('enquanto_declaracao')
        tipo_producao[0] = 'exp_simples'

        iterador += 1
        controle_comando.append(0)
        exp_simples(atual, prox)

    # <exp_rel_deriva>, P(86) comeca aqui
    # Tratamento para a producoes P(94), <op_booleano>
    elif atual[0] in op_booleano and controle_comando[iterador] == 4:
        pilha.append(atual)
        controle_comando[iterador] = 4

    # Chamando a producao P(97), <exp_simples>, novamente por vir depois de <op_booleano>
    elif (atual[0] == '+' or atual[0] == '-' or atual[1] == 1 or atual[0].isdigit() or atual[0] == '(') and controle_comando[iterador] == 4:
        controle_comando[iterador] = 5

        pilha_comandos.append('enquanto_declaracao')
        tipo_producao[0] = 'exp_simples'

        iterador += 1
        controle_comando.append(0)
        exp_simples(atual, prox)

    # Chamando novamente P(88), <op_relacional> apos o <exp_simples>
    elif atual[0] in op_relacional and controle_comando[iterador] == 5:
        pilha.append(atual)
        controle_comando[iterador] = 6

    # Novamente vem um <exp_simples> apos um <op_relacional>
    elif (atual[0] == '+' or atual[0] == '-' or atual[1] == 1 or atual[0].isdigit() or atual[0] == '(') and controle_comando[iterador] == 6:
        controle_comando[iterador] = 7

        pilha_comandos.append('enquanto_declaracao')
        tipo_producao[0] = 'exp_simples'

        iterador += 1
        controle_comando.append(0)
        exp_simples(atual, prox)

    # Caso <exp_rel_deriva> seja vazia, finaliza <exp_rel_bol> (controle_comando[iterador] == 4)
    # Com a <exp_rel_deriva> nao sendo vazia e finalizando <exp_rel_bol> (controle_comando[iterador] == 4)
    elif atual[0] == ')' and (controle_comando[iterador] == 4 or controle_comando[iterador] == 7):
        pilha.append(atual)
        controle_comando[iterador] = 8

    elif atual[0] == '{' and controle_comando[iterador] == 8:
        pilha.append(atual)
        controle_comando[iterador] = 9

    # Verificando se ha <comandos> dentro do <enquanto>
    elif (atual[0] in comandos_lista or atual[1] == 1) and controle_comando[iterador] == 8:
        pilha_comandos.append('enquanto_declaracao')

        tipo_producao[0] = 'comandos'
        # Chama a funcao da producao P(56), <comandos>
        comandos(atual,prox)

    # Encerrando o comando 'enquanto' da producao P(65), <enquanto_declaracao>
    elif atual[0] == '}' and controle_comando[iterador] == 8:
        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

        comandos(atual, prox)

    else:
        print('error')


# DICA: O <para_declaracao> somente possui <comandos> dentro e tratar o <op_relacional> igualzin como se trata no <se>
# Funcao da producao P(66), <para_declaracao>
def para_declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    if atual[0] == '(' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 1

    # Verifica se o token atual eh um 'token_identificador'
    elif atual[1] == '1' and controle_comando[iterador] == 1:
        pilha.append(atual)
        controle_comando[iterador] = 2

    elif atual[0] == '=' and controle_comando[iterador] == 2:
        pilha.append(atual)
        controle_comando[iterador] = 3

    # Verifica se o token atual eh um 'token_inteiro'
    elif atual[0].isdigit() and controle_comando[iterador] == 3:
        pilha.append(atual)
        controle_comando[iterador] = 4

    elif atual[0] == ';' and controle_comando[iterador] == 4:
        pilha.append(atual)
        controle_comando[iterador] = 5

    # Verifica se o token atual eh um 'token_identificador'
    elif atual[1] == '1' and controle_comando[iterador] == 5:
        pilha.append(atual)
        controle_comando[iterador] = 6

    # Tratamento para as producoes P(88) e P(92), <op_relacional> e <op_rel_deriva>, respectivamente
    elif atual[0] in op_relacional and controle_comando[iterador] == 6:
        pilha.append(atual)
        controle_comando[iterador] = 7

    # Verifica se o token atual eh um 'token_inteiro'
    elif atual[0].isdigit() and controle_comando[iterador] == 7:
        pilha.append(atual)
        controle_comando[iterador] = 8

    elif atual[0] == ';' and controle_comando[iterador] == 8:
        pilha.append(atual)
        controle_comando[iterador] = 9

    # Verifica se o token atual eh um 'token_identificador'
    elif atual[1] == '1' and controle_comando[iterador] == 9:
        pilha.append(atual)
        controle_comando[iterador] = 10

    # Tratamento para as producoes P(108), <op_cont>
    elif atual[0] in op_cont and controle_comando[iterador] == 10:
        pilha.append(atual)
        controle_comando[iterador] = 11

    # Fechando as condicoes do <para>
    if atual[0] == ')' and controle_comando[iterador] == 11:
        pilha.append(atual)
        controle_comando[iterador] = 12

    elif atual[0] == '{' and controle_comando[iterador] == 12:
        pilha.append(atual)
        controle_comando[iterador] = 13

    # Verificando se ha <comandos> dentro do <para>
    elif (atual[0] in comandos_lista or atual[1] == 1) and controle_comando[iterador] == 13:
        pilha_comandos.append('para_declaracao')

        tipo_producao[0] = 'comandos'
        # Chama a funcao da producao P(56), <comandos>
        comandos(atual,prox)

    # Encerrando o comando 'para' da producao P(66), <para_declaracao>
    elif atual[0] == '}' and controle_comando[iterador] == 13:
        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

        comandos(atual, prox)

    else:
        print('error')

# Funcao da producao P(67), <escreva_declaracao>
def escreva_declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    if atual[0] == '(' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 1

    # Comencando aqui a P(68), <exp_escreva>
    # Que comeca com P(72), <exp_imprime>
    elif (atual[1] == '4' or atual[1] == '5' or atual[1] == '1' or atual[0] == '(') and controle_comando[iterador] == 1:
        pilha.append(atual)
        controle_comando[iterador] = 2

        if atual[1] == '1':

            if prox[0] == '.' or prox[0] == '[':
                iterador += 1
                controle_comando.append(0)
                pilha_comandos.append('escreva_declaracao')
                tipo_producao[0] = 'identificador_imp_arm_deriva'

        elif atual[0] == '(':
            controle_comando[iterador] = 4

            iterador += 1
            controle_comando.append(0)
            pilha_comandos.append('escreva_declaracao')
            tipo_producao[0] = 'exp_simples'

    elif atual[0] == ')' and controle_comando[iterador] == 4:
        pilha.append(atual)
        controle_comando[iterador] = 2

    # Producao P(70), <exp_escreva_deriva>, que pode ser vazia
    elif atual[0] == ',' and controle_comando[iterador] == 2:
        pilha.append(atual)
        # Apos a virgula ',' vem um <exp_imprime>
        controle_comando[iterador] = 1

    # Outra producao P(68), <exp_escreva>, aqui que pode ser vazia
    # Que comeca com P(72), <exp_imprime>
    elif (atual[1] == '4' or atual[1] == '5' or atual[1] == '1' or atual[0] == '(') and controle_comando[iterador] == 2:
        pilha.append(atual)
        controle_comando[iterador] = 2

        if atual[1] == '1':

            if prox[0] == '.' or prox[0] == '[':
                iterador += 1
                controle_comando.append(0)
                pilha_comandos.append('escreva_declaracao')
                tipo_producao[0] = 'identificador_imp_arm_deriva'

        elif atual[0] == '(':
            controle_comando[iterador] = 4

            iterador += 1
            controle_comando.append(0)
            pilha_comandos.append('escreva_declaracao')
            tipo_producao[0] = 'exp_simples'

    # A condicao 'controle_comando[iterador] == 1' eh para caso a primeira <exp_escreva> seja vazia
    elif atual[0] == ')' and (controle_comando[iterador] == 2 or controle_comando[iterador] == 1):
        pilha.append(atual)
        controle_comando[iterador] = 3

    # Encerrando o comando 'escreva' da producao P(67), <escreva_declaracao>
    elif atual[0] == ';' and controle_comando[iterador] == 3:
        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

        comandos(atual, prox)

    else:
        print('error')


# Funcao da producao P(79), <leia_declaracao>
def leia_declaracao(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    if atual[0] == '(' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 1

    # Comencando aqui a P(80), <exp_leia>
    # Que comeca com P(84), <exp_armazena>
    elif atual[1] == '1' and controle_comando[iterador] == 1:
        pilha.append(atual)
        controle_comando[iterador] = 2

        if prox[0] == '.' or prox[0] == '[':
            iterador += 1
            controle_comando.append(0)
            pilha_comandos.append('leia_declaracao')
            tipo_producao[0] = 'identificador_imp_arm_deriva'

    # Producao P(82), <exp_leia_deriva>, que pode ser vazia
    elif atual[0] == ',' and controle_comando[iterador] == 2:
        pilha.append(atual)
        # Apos a virgula ',' vem um <exp_armazena>
        controle_comando[iterador] = 1

    # Outra producao P(68), <exp_leia>, aqui que pode ser vazia
    # Que comeca com P(84), <exp_armazena>
    elif atual[1] == '1' and controle_comando[iterador] == 2:
        pilha.append(atual)
        controle_comando[iterador] = 2

        if prox[0] == '.' or prox[0] == '[':
            iterador += 1
            controle_comando.append(0)
            pilha_comandos.append('leia_declaracao')
            tipo_producao[0] = 'identificador_imp_arm_deriva'

    # A condicao 'controle_comando[iterador] == 1' eh para caso a primeira <exp_leia> seja vazia
    elif atual[0] == ')' and (controle_comando[iterador] == 2 or controle_comando[iterador] == 1):
        pilha.append(atual)
        controle_comando[iterador] = 3

    # Encerrando o comando 'leia' da producao P(79), <leia_declaracao>
    elif atual[0] == ';' and controle_comando[iterador] == 3:
        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

        comandos(atual, prox)

    else:
        print('error')


# Funcao da producao P(76), <identificador_imp_arm_deriva>
def identificador_imp_arm_deriva(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    if atual[0] == '.' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 1

    elif atual[0] == '[' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 2

    elif atual[0].isdigit() and controle_comando[iterador] == 2:
        pilha.append(atual)
        controle_comando[iterador] = 3

    # Ao final do '.token_identificador' encerra <identificador_imp_arm_deriva> e volta para <escreva_declaracao> ou <leia_declaracao>
    elif atual[1] == 1 and controle_comando[iterador] == 1:
        pilha.append(atual)

        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

    # Ao final do '[token_inteiro]'' encerra <identificador_imp_arm_deriva> e volta para <escreva_declaracao> ou <leia_declaracao>
    elif atual[0] == ']' and controle_comando[iterador] == 3:
        pilha.append(atual)

        # Tratamento para caso seja <matriz>
        if prox[0] == '[':
            controle_comando[iterador] = 0

        else:
            iterador -= 1
            controle_comando.pop()
            tipo_producao[0] = pilha_comandos.pop()

    else:
        print('error')


# Funcao da producao P(96), <exp_aritmetica>
def exp_aritmetica(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    if atual[0] == '=' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 1

    # Chamando a producao P(97), <exp_simples>, por vir depois de '='
    elif (atual[0] == '+' or atual[0] == '-' or atual[1] == 1 or atual[0].isdigit() or atual[0] == '(') and controle_comando[iterador] == 1:
        controle_comando[iterador] = 2

        pilha_comandos.append('exp_aritmetica')
        tipo_producao[0] = 'exp_simples'

        iterador += 1
        controle_comando.append(0)
        exp_simples(atual, prox)

    elif atual[0] == ';' and controle_comando[iterador] == 2:
        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

        comandos(atual, prox)

    else:
        print('error')


# Funcao da producao P(97) <exp_simples>
def exp_simples(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    # <exp_simples> que comeca com P(106), <op_ss>
    if (atual[0] == '+' or atual[0] == '-') and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 1

    # Condicao dupla para caso seja escolhida a producao alternativa P(98) ou vinda depois de <op_ss>
    # com a producao P(110), <termo>, que inicia com P(115), <fator>
    if(atual[1] == '1' or atual[0].isdigit() or atual[0] == '(') and (controle_comando[iterador] == 0 or controle_comando[iterador] == 1):
        controle_comando[iterador] = 2  # MUDAR para 2?

        pilha_comandos.append('exp_simples')
        tipo_producao[0] = 'fator'

        iterador += 1
        controle_comando.append(0)
        fator(atual, prox)

    #  Tratamento para producao P(111), <fator_deriva>
    elif (atual[0] == '*' or atual[0] == '/') and controle_comando[iterador] == 2:
        pilha.append(atual)
        controle_comando[iterador] = 1

        '''pilha_comandos.append('exp_simples')
        tipo_producao[0] = 'fator'

        iterador += 1
        controle_comando.append(0)'''

    # A condicao 'controle_comando[iterador] == 1' tambem eh para caso <fator_deriva> seja vazio
    # Tratando para producao P(99), <termo_deriva>
    elif (atual[0] == '+' or atual[0] == '-') and (controle_comando[iterador] == 1 or controle_comando[iterador] == 2):
        pilha.append(atual)
        # Tratamento para P(102), <op_soma_deriva>
        if atual[0] == '+' and prox[0] == '+':
            controle_comando[iterador] = 3
        # Tratamento para P(102), <op_sub_deriva>
        elif atual[0] == '-' and prox[0] == '-':
            controle_comando[iterador] = 4
        # Tratamento para <op_soma_deriva> ou <op_sub_deriva> que chama <termo>
        elif prox[1] == '1' or prox[0].isdigit() or prox[0] == '(':
            controle_comando[iterador] = 1
        else:
            print('error')

    # Tratamento para P(102), <op_soma_deriva>, quando chama o segundo simbolo
    elif atual[0] == '+' and controle_comando[iterador] == 3:
        pilha.append(atual)
        controle_comando[iterador] = 5
        # Se o proximo for um <op_relacional>, encerra <exp_simples>
        if prox[0] in op_relacional and (controle_comando[iterador-1] == 2 or controle_comando[iterador-1] == 5):
            controle = 7

            iterador -= 1
            controle_comando.pop()
            tipo_producao[0] = pilha_comandos.pop()

        # Ou se o proximo for um <op_booleano>, encerra <exp_simples>
        elif prox[0] in op_booleano and controle_comando[iterador-1] == 4:
            controle = 7

            iterador -= 1
            controle_comando.pop()
            tipo_producao[0] = pilha_comandos.pop()

    # Tratamento para P(102), <op_sub_deriva>, quando chama o segundo simbolo
    elif atual[0] == '-' and controle_comando[iterador] == 4:
        pilha.append(atual)
        controle_comando[iterador] = 6
        # Se o proximo for um <op_relacional>, encerra <exp_simples>
        if prox[0] in op_relacional and (controle_comando[iterador-1] == 2 or controle_comando[iterador-1] == 5):
            controle = 7

            iterador -= 1
            controle_comando.pop()
            tipo_producao[0] = pilha_comandos.pop()

        # Ou se o proximo for um <op_booleano>, encerra <exp_simples>
        elif prox[0] in op_booleano and controle_comando[iterador-1] == 4:
            controle = 7

            iterador -= 1
            controle_comando.pop()
            tipo_producao[0] = pilha_comandos.pop()

    # Encerrando caso <fator_deriva> e/ou <termo_deriva> sejam vazis
    elif controle_comando[iterador] == 1 or controle_comando[iterador] == 2:
        # Se o proximo for um <op_relacional>, encerra <exp_simples>
        if prox[0] in op_relacional and (controle_comando[iterador-1] == 2 or controle_comando[iterador-1] == 5):
            controle = 7

            iterador -= 1
            controle_comando.pop()
            tipo_producao[0] = pilha_comandos.pop()

        # Ou se o proximo for um <op_booleano>, encerra <exp_simples>
        elif prox[0] in op_booleano and controle_comando[iterador-1] == 4:
            controle = 7

            iterador -= 1
            controle_comando.pop()
            tipo_producao[0] = pilha_comandos.pop()

        else:
            print('error')

    # Tratamento de erro
    else:
        print('error')


# Funcao da producao P(115), <fator>
def fator(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global controle_comando
    global pilha_comandos
    global iterador

    if atual[1] == '1' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 1

    elif atual[0].isdigit() and controle_comando[iterador] == 0:
        pilha.append(atual)

        # Somente pega o 'token_numero' e encerra <fator>
        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

    elif atual[0] == '(' and controle_comando[iterador] == 0:
        pilha.append(atual)
        controle_comando[iterador] = 3

        iterador += 1
        controle_comando.append(0)
        pilha_comandos.append('fator')
        tipo_producao[0] = 'exp_simples'

    # Os proximos 3 'if's' sao tratamento para P(76), <identificador_imp_arm_deriva> com suas producoes alternativas
    elif atual[0] == '.' and controle_comando[iterador] == 1:
        pilha.append(atual)
        controle_comando[iterador] = 2

    elif atual[0] == '[' and controle_comando[iterador] == 1:
        controle_comando[iterador] = 4

        pilha_comandos.append('fator')
        # Prepara e chama <matriz>
        controle = 4
        matriz(atual, prox)

    elif atual[1] == 1 and controle_comando[iterador] == 2:
        pilha.append(atual)
        controle_comando[iterador] = 5

        # Depois de pegar o '.token_identificador' encerra <fator>
        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

    # Encerrando para P(117)
    elif atual[0] == ')' and controle_comando[iterador] == 3:
        controle = 7
        # Depois de passar pelas possiveis producoes encerra <fator>
        iterador -= 1
        controle_comando.pop()
        tipo_producao[0] = pilha_comandos.pop()

    else:
        print('error')


# DICA: <algoritmo> eh igual a uma funcao sem parametros e sem retorno
# Funcao da producao P(52), <algoritmo_declaracao>
def algoritmo(atual, prox):
    global pilha
    global tipo_producao
    global controle

    global pilha_comandos

    if atual[0] == '{' and controle == 0:
        pilha.append(atual)
        controle = 1

    # A producao <deriva_cont_principal> P(53) comeca aqui
    elif atual[0] in tipo_primitivo and controle == 1:
        controle = 1
        tipo_producao[0] = 'declaracao_var'
        tipo_producao[3] = 'algoritmo'

        declaracao_var(atual, prox)

    # Acrescentando 'controle == 1' como condicao permito a possibilidade de P(22) <declaracao_var> seja vazia
    # e seguir para a producao alternativa P(54)
    # Verifica se o token atual eh um comando
    elif (atual[0] in comandos_lista or atual[1] == 1) and (controle == 2 or controle == 1):
        tipo_producao[3] = 'algoritmo'
        pilha_comandos.append('algoritmo')
        controle = 2

        tipo_producao[0] = 'comandos'
        # Chama a funcao da producao P(56), <comandos>
        comandos(atual,prox)

    # Encontrando a ultima chave, finaliza <algoritmo>
    elif atual[0] == '}' and controle == 2:
        pilha.append(atual)
        # Como algoritmo eh o ULTIMO bloco do programa, apos deve vir nada
        tipo_producao[0] = '$'
        controle = 0

    else:
        print('error')






# A mensagem de ERRO será, por exemplo, 'Erro. Uma '(' era esperado, linha 10'

j = 0

# Codigo que vai ler cada token da lista
# Fazendo a varredura de cada token da lista
for t in tokens:
    # Este verifica se o token lido eh o ultimo de todo a lista
    if j < tamanho-2:               # Aqui vou ate o ante-penultimo

        if tipo_producao[0] == 'start':                            # # Tratamento para producao 1, a inicial da analise sintatica, <start>
            start(t, tokens[j+1])                                   # Passando o atual e o proximo para a funcao 'start'

        elif tipo_producao[0] == 'registro':                   # Tratamento para producao 2, <registro_declaracao>
            registro_declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'declaracao_reg':       # Tratamento para producao 4, <declaracao_reg>
            declaracao_reg(t, tokens[j+1])

        elif tipo_producao[0] == 'declaracao':              # Tratamento para producao 6, <declaracao>
            declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'constantes':              # Tratamento para producao 12, <constantes_declaracao>
            constantes_declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'declaracao_const':   # Tratamento para producao 13, <declaracao_const>
            declaracao_const(t, tokens[j+1])

        elif tipo_producao[0] == 'variaveis':                  # Tratamento para producao 21, <variaveis_declaracao>
            variaveis_declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'declaracao_var':          # Tratamento para producao 22, <declaracao_var>
            declaracao_var(t, tokens[j+1])

        elif tipo_producao[0] == 'matriz':                         # Tratamento para producao 28, <matriz>
            matriz(t, tokens[j+1])

        elif tipo_producao[0] == 'valor_primitivo':
            if isvalorprimitivo(t):
            # Tratamento para producao 30, <inicializacao>
                if tipo_producao[1] == 'identificador_deriva':      # Verificar depois se isso aqui sera realmente necessario
                    pilha.append(t)
                    tipo_producao[0] = 'declaracao_var'
                    controle = 8

            else:
                print('error')

        elif tipo_producao[0] == 'funcao':                          # Tratamento para producao 32, <funcao_declaracao>
            funcao_declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'decl_param':                  # Tratamento para producao 34, <decl_param>
            decl_param(t, tokens[j+1])

        elif tipo_producao[0] == 'identificador_param_deriva':      # Tratamento das producoes 38 e 40, <identificador_param_deriva> e <matriz_param>, respectivamente
            identificador_param_deriva(t, tokens[j+1])

        elif tipo_producao[0] == 'comandos':                                    # Tratamento das producoes P(44) e P(56), <decl_comandos> e <comandos>, respectivamente
            comandos(t, tokens[j+1])                                                   # Feita juntas para nao haver redundancias desnecessarias no codigo

        elif tipo_producao[0] == 'se_declaracao':                              # Tratamento para producao P(62), <se_declaracao>
            se_declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'senao_declaracao':                        # Tratamento para producao P(63), <senao_declaracao>
            senao_declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'enquanto_declaracao':                  # Tratamento para producao P(65), <enquanto_declaracao>
            enquanto_declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'para_declaracao':                          # Tratamento para producao P(66), <para_declaracao>
            para_declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'escreva_declaracao':                    # Tratamento para producao P(67), <escreva_declaracao>
            escreva_declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'leia_declaracao':                           # Tratamento para producao P(79), <leia_declaracao>
            leia_declaracao(t, tokens[j+1])

        elif tipo_producao[0] == 'exp_aritmetica':                            # Tratamento para producao P(96), <exp_aritmetica>
            exp_aritmetica(t, tokens[j+1])

        elif tipo_producao[0] == 'exp_simples':                                 # Tratamento para producao P(97), <exp_simples>
            exp_simples(t, tokens[j+1])

        elif tipo_producao[0] == 'fator':                                               # Tratamento para producao P(115), <fator>
            fator(t, tokens[j+1])

        elif tipo_producao[0] == 'identificador_imp_arm_deriva':      # Tratamento para producao P(76), <identificador_imp_arm_deriva>
            identificador_imp_arm_deriva(t, tokens[j+1])

        elif tipo_producao[0] == 'algoritmo':                                       # Tratamento para producao P(52), <algoritmo_declaracao>
            algoritmo(t, tokens[j+1])


    # Se for o penultimo token eh lido, eh feito um tratamento diferente,
    # pois o ultimo token lido eh o '$' que significa final de arquivo
    # alem de que para nao exceder o tamanho da lista e dar erro
    else:        # Pegando o penultimo e o ultimo token do arquivo, posso verificar se foi finalizado corretamente
                    # ou se ocorreu um 'final inesperado do arquivo'

        if t[0] == '}' and tokens[j+1][0] == '$':             # Essa eh a condicao correta, se entrar nela CHAMA TUDO corretamente

            print("entrou")
            algoritmo(t, tokens[j+1])                        # O final do programa deve ser sempre o final da producao P(52), <algoritmo_declaracao>

        else:                                                             # Essa eh a condicao errada, pode CHAMAR TUDO mas havera erros,

            print('error: Final inesperado do arquivo.')    # entrando nela imprimir mensagem de erro

        tokens.pop()                                                # Depois retira o '$' do final da lista de tokens
        j += 1                                                          # Da esta incrementada para nao entrar nesta condicao novamente,
                                                                            # sem que haja arquivos para ler

    j += 1