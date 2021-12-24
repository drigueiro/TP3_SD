from circle import *
from multiprocessing import Process,Manager, Value
#!pip install pickle
import _pickle as cPickle
#import multiprocessing
import socket
import time


Mensagem01 = "Desejo Ingressar na rede"
Mensagem02 = "Desejo Sair da Rede"
Mensagem03 = "Atualizacao Dados"
Mensagem04 = "Requisicao de Escrita"
Mensagem05 = "OK"
Mensagem06 = "Lista de subscribers"
Mensagem07 = "Request"
Mensagem08 = "Reply"
Mensagem09 = "Voltando a funcionar"


topic = "200.239.138.236"
myport = 7070
port = 6969
portsubs = 7171


#atualizado = False
circles = None
circlesReq = None




def sendRequestTopic(subsTopic2, subscribers):

        while(bool(envia.value)==True):
            a=0;
        print("não estou esperando mais o enviar")
        try:
            envia.value = True
            time.sleep(2)
            SocketTopic = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            dest = (topic, int(port))
            SocketTopic.connect(dest)
            ReqW = cPickle.dumps([Mensagem07,"Qualquer"])
            SocketTopic.send(ReqW)
            #recebe a resposta
            print("Vai receber a Mensagem")
            aux = SocketTopic.recv(100000)
            if len(aux)>0:
                data = cPickle.loads(aux)

            if (data==Mensagem08):
                token.value = True;

            SocketTopic.close();
            envia.value= False
        except:

            token.value = True;
            print("Outro Topic caiu avisar subscribers");
            #atribui os novos subscribers a ele
            for s in subsTopic2:
                subscribers.append(s);


def sendCirclesTopic(Circles, subsTopic2, subscribers, token, envia, caiu):

    while(bool(envia.value)==True):
        a=0;
    print("não estou esperando mais o enviar")
    try:
        envia.value = True
        SocketTopic = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Enviando circles")
        dest = (topic, int(port))
        SocketTopic.connect(dest)
        ReqW = cPickle.dumps([Mensagem03,list(Circles)])
        SocketTopic.send(ReqW);
        SocketTopic.close();
        envia.value= False
    except:

        token.value = True;
        print("Outro Topic caiu avisar subscribers");
        #atribui os novos subscribers a ele
        for s in subsTopic2:
            subscribers.append(s);

        caiu.value=True

def atualizaSubscribers(Circles, subscribers):
    atualiza = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("SUBSCRIBERS", subscribers)
    for subscriber in subscribers:
        try:
            dest = (subscriber, int(portsubs))
            atualiza.connect(dest)
            circulos = cPickle.dumps(list(Circles))
            atualiza.send(circulos)
            atualiza.close();
            atualizado = False;
            circles = None;
        except:
            print("Perdeu a conexao com o Subscriber:", subscriber )


def listening(circlesAtual, subscribers, subsTopic2, RequestQ, caiu, token, envia):
    print("listening")
    numAtualiza= 0
    while(True):
        while (len(RequestQ)!=0):
            aux = RequestQ[0]
            conexao, ipConexao= aux[0]
            data = aux[1];
            print(ipConexao)
            #print("DATA:", data)
            if(data == Mensagem01): #se for subscriber cadastrando na rede
                subscribers.append(ipConexao[0])
                conexao.send( cPickle.dumps(list(circlesAtual)))
                if len(topic)!=0:
                    SocketTopic = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    dest = (topic, int(port))
                    SocketTopic.connect(dest)
                    topicsubs = cPickle.dumps([Mensagem06,list(subscribers)])
                    SocketTopic.send(topicsubs)
                    SocketTopic.close();

            if(data == Mensagem02): #se for subscriber saindo da rede
                subscribers.remove(ipConexao[0])


            if(data[0] == Mensagem03): #Se estiver recebendo atualizacao
                circles = data[1];
                atualizado = True;
                atualiza = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                print("Atualização numero", numAtualiza)
                numAtualiza= numAtualiza +1;
                #escrita dos dados no próprio topic
                for c in circles:
                    circlesAtual.append(c)

                atualizaSubscribers(circles, subscribers);


            if (data[0] == Mensagem04):
                circlesReq = data[1]; #circulos na qual os publisher querem escrever

                numAtualiza= numAtualiza +1;
                print("Atualização numero", numAtualiza)

                if(bool(token.value) ==True):
                    using.value = True
                    #conexao.send( cPickle.dumps("Escrita Realizada"))

                    for c in circlesReq:
                        circlesAtual.append(c)

                    atualizaSubscribers(circlesReq, subscribers);
                    if len(topic)!=0 and bool(token.value)==True:
                        sendCirclesTopic(circlesReq,subsTopic2, subscribers, token, envia, caiu)

                else:
                    if len(topic)!=0 :  #manda requisicao para receber o token
                        sendRequestTopic(subsTopic2, subscribers)


                    if bool(token.value)==True:
                        using.value = True
                        #conexao.send( cPickle.dumps("Escrita Realizada"))
                        numAtualiza= numAtualiza +1;
                        print("Atualização numero", numAtualiza)
                        for c in circlesReq:
                            circlesAtual.append(c)

                        atualizaSubscribers(circlesReq, subscribers);

                        if len(topic)!=0 and bool(token.value)==True:
                            sendCirclesTopic(circlesReq,subsTopic2, subscribers,token, envia, caiu)

                using.value= False

            if(data[0]==Mensagem06):
                for sb in data[1]:
                    subsTopic2.append(sb)

            RequestQ.pop(0)
            conexao.close()





def sincronize(circlesAtual, subscribers, RequestQ,token,caiu, envia):
    print("sincronize")
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = ("0.0.0.0", int(myport))
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind(orig)
    tcp.listen(50)

    while(True):
        conexao, ipConexao = tcp.accept()



        msg = conexao.recv(100000)


        if(len(msg)>0):

            data = cPickle.loads(msg)

            print(data)
            if(data[0]==Mensagem07): #Requisicao de token
                if(bool(using.value)==False):
                    envia.value = True
                    conexao.send(cPickle.dumps(Mensagem08))
                    token.value =False
                    envia.value = False
                else:
                    time.sleep(5)
                    print("Token sendo usado - espera um pouco")
                    if(bool(using.value)==False):
                        envia.value = True
                        conexao.send(cPickle.dumps(Mensagem08))
                        envia.value = False
                        token.value =False

            elif(data== Mensagem05):
                print("DATA:", Mensagem05)
                envia.value = True
                conexao.send(cPickle.dumps(Mensagem05))
                envia.value = False

            elif(data[0]== Mensagem09):
                for s in data[2]:
                    subscribers.append(s)
                for c in data[1]:
                    circlesAtual.append(c)
                caiu.value = False
            else:
                print("DATA2:", data)

                RequestQ.append([(conexao, ipConexao), data])

    tcp.close()

def sincronizeTopic(subsTopic2, subscribers, token, caiu):
    print("sincronizeTopic")
    caiu.value = False
    dest = (topic, int(port))
    while True:
        time.sleep(4)

        try:
            if (bool(envia.value)== False):
                if bool(caiu.value)==False:

                    SocketTopic = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    SocketTopic.connect(dest)
                    ReqW = cPickle.dumps(Mensagem05)
                    SocketTopic.send(ReqW);
                    SocketTopic.close();


            else:
                try:
                    print("topic caiu tentando reerguer")
                    SocketTopic = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    SocketTopic.connect(dest)
                    print("mandando lista circles")
                    ReqW = cPickle.dumps([Mensagem09,list(circlesAtual), list(subsTopic2)])
                    SocketTopic.send(ReqW);
                    SocketTopic.close();
                    time.sleep(4)

                    caiu.value = False

                    for s in subsTopic2:
                        subscribers.remove(s)

                except:
                    print("Outro topic ainda não voltou")
                    caiu.value = True

        except:
            if(bool(caiu.value)==False):
                token.value = True;
                print("Outro Topic caiu avisar subscribers");
                #atribui os novos subscribers a ele
                for s in subsTopic2:
                    subscribers.append(s);
                caiu.value=True
                print("Caiu",caiu.value)



if __name__ == '__main__':

    circlesAtual = Manager().list([])
    subscribers = Manager().list([])
    subsTopic2 = Manager().list([])
    RequestQ = Manager().list([])

    token = Value('b',True)
    using = Value('b', False)
    envia = Value('b',False)
    caiu = Value('b',False)

    sincronize = Process(target=sincronize,args=(circlesAtual, subscribers, RequestQ,token, caiu, envia))
    sincronize2 = Process(target=sincronizeTopic,args=(subsTopic2, subscribers, token , caiu))
    listen = Process(target=listening, args=(circlesAtual, subscribers, subsTopic2, RequestQ, caiu, token, envia,))
    sincronize.start()
    sincronize2.start()
    listen.start()
    sincronize.join()

    sincronize2.join()
    listen.join()
