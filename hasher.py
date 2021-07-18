import hashlib
import csv

def CousinValue(n_registros):
    if(n_registros %2) == 0:
        n_registros +=1
    for cousin_verifier in range(3,n_registros,2):
        if(n_registros % cousin_verifier) == 0:
            n_registros +=2
            return CousinValue(n_registros)
    return n_registros
    
def MakeTable():
    #Table Hash -> Dicionario da forma hash_table = {'h_index':('cod_hash', 'user_login','user_pswd','user_type')}
    hash_table = {}
    n_registros = n_users + (n_users //2)
    n_registros = CousinValue(n_registros)
    print('\nNumero de registros na tabela é: {}\n'.format(n_registros))
    for index in range(n_registros):
        hash_table[index] = (None, None, None, None)
    return hash_table

def HashIt(user_login, user_pswd):
    cod_hash = hashlib.md5((user_login + user_pswd).encode())
    cod_hash = cod_hash.hexdigest()
    cod_hash = int(cod_hash, 16)
    return cod_hash

def InsertReg(user_login, user_pswd, user_type):
    global hash_table
    global jump_count
    cod_hash = HashIt(user_login, user_pswd)

    if CheckReg(cod_hash, user_login, user_pswd):
        return ('Já existe um registro com essas informações na tabela') 

    jump_count =0
    index = cod_hash % n_users
    jumper = (cod_hash // n_users) % n_users
    if jumper == 0:
        jumper =1
    print('O indice gerado foi - {} - \nO jump para colisao - {} -'.format(index,jumper))
    index = SearchIndex(len(hash_table), index, jumper, index, 'inserção')
    

    #if  CheckIndex(index,'inserção'):
    if  CheckIndex(index,'inserção'):
        hash_table[index] = (cod_hash, user_login, len(user_pswd) *'*', user_type)
        #Debugging
        #return (True, user_login, index, jumper)
        return ('Registro inserido')
    
    else:
        return ('Não existem mais registros vazios na tabela')
    #Debugging
    #return (False, user_login, index, jumper)

def SetReg():
    user_login = input('Informe nome do usuario: ')
    user_pswd = input('Informe senha do usuario: ')
    user_type = input('Informe função do usuario: ')
    ClScreen()
    return InsertReg(user_login, user_pswd, user_type)

def RemoveReg():
    #Remoção de registros através da alteração dos seus campos para nulo
    #Se presupõe que tenham havidos saltos para o indice do registro removido
    if WeightTable() == '0%':
        return 'A tabela está vazia'

    opcao = input('\nremoção por indice ou por registro?\n: ')
    opcao = opcao.lower()

    #remoção de Registro Atraves do indice
    if opcao == "indice":
        JumpCounter()
        index = int(input('\nIndice do registro a ser deletado é: '))
        return DelIndex(index)
    
    #remoção de Registro Atraves de busca dos dados
    else:
        user_login = input('Informe login do usuario: ')
        user_pswd = input('Informe senha do usuario: ')
        return DelReg(user_login, user_pswd)

    return None

def DelReg(user_login, user_pswd):
    global hash_table
    cod_hash = HashIt(user_login, user_pswd)
    index = cod_hash % n_users
    jumper = (cod_hash // n_users) % n_users
    index = SearchIndex(len(hash_table), index, jumper, index, cod_hash)

    if cod_hash and user_login in hash_table[index][:2]:
        hash_table[index] = ('Some','None','None','None')
        return True

    return False

def DelIndex(index):
    global hash_table
    if not CheckIndex(index,'inserção'):
        hash_table[index] = ('Some','None','None','None')
        return True

    return False

def CheckIndex(index, arg):
    #A função recebe o indice a ser conferido e um argumento que indica o que deve ser buscado neste indice
    #caso o argumento seja 'inserção' então se busca por um indice vazio para inserção
    #caso contrario se busca pelo proprio argumento como valor contido no indice informado
    global hash_table
    if arg == 'inserção':
        return bool(hash_table[index][0] in [None, 'Some'])
    else:
        return bool(hash_table[index][0] == arg)

def CheckReg(cod_hash, user_login, user_pswd):
    #Verifica se os dados inseridos estão contidos na tabela, realizando os saltos necessarios
    global hash_table
    cod_hash = HashIt(user_login, user_pswd)
    index = cod_hash % n_users
    jumper = (cod_hash // n_users) % n_users
    index = SearchIndex(len(hash_table), index, jumper, index, cod_hash)

    if cod_hash and user_login in hash_table[index][:2]:
        return True
    return False

def SearchIndex(len_table, index, jumper, new_index, arg):
    #print("ACCESS", new_index)
    JumpCounter()
    if CheckIndex(new_index, arg):
        return new_index

    new_index += jumper
    if new_index >= len_table:
        new_index -= len_table
    
    if new_index == index:
        return new_index
    
    return SearchIndex(len_table, index, jumper, new_index, arg)

def UserAuthenticate():
    user_login = input('Digite seu login: ')
    user_pswd = input('Digite sua senha:')
    return Authentication(user_login, user_pswd)

def Authentication(user_login, user_pswd):
    cod_hash = HashIt(user_login, user_pswd)

    if CheckReg(cod_hash, user_login, user_pswd):
        print('Autenticação realizada com sucesso')
        return True

    print('Dados não encontrados')
    return False

def CatchReg():
    #Leitura de registros através do seu indice ou dados contidos

    opcao = input('captura por indice ou por registro?\n: ')
    opcao = opcao.lower()

    #leitura de Registro Atraves do indice
    if opcao == 'indice':
        JumpCounter()
        index = int(input('\nIndice do registro a ser capturado é: '))
        return GetByIndex(index)
    
    #Leitura de Registro Atraves de busca dos dados
    else:
        user_login = input('Informe login do usuario: ')
        user_pswd = input('Informe senha do usuario: ')
        return GetByReg(user_login, user_pswd)

    return None

def GetByIndex(index):
    global hash_table
    if not CheckIndex(index,'inserção'):
            return hash_table[index]

    return 'Indice de Registro Inexistente'

def GetByReg(user_login, user_pswd):
    global hash_table
    cod_hash = HashIt(user_login, user_pswd)
    index = cod_hash % n_users
    jumper = (cod_hash // n_users) % n_users
    index = SearchIndex(len(hash_table), index, jumper, index, cod_hash)

    if cod_hash and user_login in hash_table[index][:2]:
        return hash_table[index]

    return 'Dados de Registro Inexistente'

#inforamções sobre quantidade de acessos e registros na tabela
def WeightTable():
    #Cálculo do fator de ocupação da tabela hash - n_reg preenchidos / n_reg totais
    global hash_table
    weight = 0.0
    for counter in range(len(hash_table)):
        if hash_table[counter][0] not in ['Some',None]:
            weight += 1
    return ("{:.0%}".format(weight / len(hash_table)))

jump_count =0
def JumpCounter():
    #Contador de acessos a indices da lista numa operação de inserção, remoção ou captura de registros
    global jump_count
    jump_count = jump_count +1

def WriteLog(tabela):
    with open("TabelaHash.csv",'w+', newline ='') as logfile:
        gravar_dados = csv.writer(logfile, delimiter ='\n')
        gravar_dados.writerow([(index,campo) for index,campo in zip(tabela.keys(),tabela.values())])

def ClScreen():
    import os
    pause = input('\nPressione uma tecla para continuar')
    os.system('cls' if os.name == 'nt' else 'clear')
      
#Menu de operações para segundo trabalho da disciplina Estrutura de Dados II - Tabelas Hash
def Menu(funcoes):
    global jump_count
    ClScreen()
    print('Digite:')
    print('Insert - para inserir um novo registro a tabela')
    print('Remove - para remover um dos registros da tabela')
    print('Catch - Para ler um dos registros da tabela')
    print('Authenticate - Para logar com um dos registros da tabela')
    print('Weight - Para imprimir fator de ocupação da tabela')
    print('Exit - Para interromper execução do programa')
    
    option = input('\nA operação é: ')
    option = option.lower()
    if option == 'exit':
        return 'Sair'
    jump_count =0
    ClScreen()
    print(funcoes[option]())
    print("Numero de acessos a tabela foi:", jump_count)

    

#Gerenciamento e autenticação de usuarios utilizando tabela hash
funcoes = {'insert':SetReg, 'remove':RemoveReg, 'catch':CatchReg, 'authenticate':UserAuthenticate, 'weight':WeightTable}
n_users = int(input('O numero de usuarios esperados para o sistema é: '))
hash_table = MakeTable()
while Menu(funcoes) != 'Sair':
    WriteLog(hash_table)
