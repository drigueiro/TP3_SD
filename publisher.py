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

global qtCircle
qtCircle= 0

NUMBER_CIRCLES = 3
myport = 6969
myport2 = 7070
topic ="200.239.138.236"
topic2 = "200.239.138.122"


def createList():
    circle_list = []
    for i in range(NUMBER_CIRCLES):
        circle_list.append(CreateCircle(i+qtCircle))

    return circle_list;



for j in range(20):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (topic, int(myport))
    dest2 = (topic2, int(myport2))
    try:
    
        tcp.connect(dest)
        circle_list = createList()
        qtCircle = qtCircle + NUMBER_CIRCLES
        data = cPickle.dumps([Mensagem04, circle_list])
        tcp.send(data)
        tcp.close();
        time.sleep(5);
    except:
        try:
            tcp.connect(dest2)
            circle_list = createList()
            qtCircle = qtCircle + NUMBER_CIRCLES
            data = cPickle.dumps([Mensagem04, circle_list])
            tcp.send(data)
            tcp.close();
            time.sleep(5);
            
        except Exception as e:
            raise
        