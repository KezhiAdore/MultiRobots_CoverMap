import pygame
import random
import math
import time
from sys import exit

def load_map(path):
    try:
        with open('./map/'+path,'r') as f:
            x=f.readlines()
            global map_size,start_pos
            x[0]=x[0].split()
            map_size=[int(i) for i in x[0]]
            x[1]=x[1].split()
            start_pos=[int(i) for i in x[1]]
            for i in range(map_size[0]):
                for j in range(map_size[1]):
                    block[i][j]=-int(x[i+2][j])
    except:
        start_pos=(-1,-1)
        print('Cannot load file {0}'.format(path))
        return False
    else:
        print('Successfully load file {0}'.format(path))
        return True


def check(x,y):
    return x>=0 and x<map_size[0] and y>=0 and y<map_size[1] and block[x][y]>=0

def roulette(lst):
    length=len(lst)
    psum=0
    for i in range(length):
        psum=psum+lst[i]
    p=random.random()*psum
    for i in range(length):
        if (p>psum-lst[i]):
            return i
        psum=psum-lst[i]
    return length-1




##在窗口中画出网格
def draw_line():
    start,end=[edge,edge],[edge+rect_size[0]*map_size[0],edge+rect_size[1]*map_size[1]]
    for i in range(0,map_size[0]+1):
        pygame.draw.line(window,line_color,(edge+i*rect_size[0],start[1]),(edge+i*rect_size[0],end[1]))
    for i in range(0,map_size[1]+1):
        pygame.draw.line(window,line_color,(start[0],edge+i*rect_size[1]),(end[0],edge+i*rect_size[1]))

def draw_rect(point,color):
    global rect_size
    left=point[1]*(rect_size[0])+edge
    top=point[0]*(rect_size[1])+edge
    rect_color_size=(rect_size[0]-1,rect_size[1]-1)
    pygame.draw.rect(window,color,((left+1,top+1),rect_color_size))



def init():
    global width,height,textwidth,fps,clock,info,block,visit,window,direction,visitcell,edge,map_size,rect_size,totalcell,turn,disp
    if (disp):
        pygame.init()
        pygame.display.set_caption("机器人仿真")
        width,height,textwidth=800,800,300   #窗口宽高
        fps=60  #窗口帧率
        clock=pygame.time.Clock()   #时间控制
        window=pygame.display.set_mode((width+textwidth,height))
        edge=50 #网格旁边留白宽度
        ##窗口控制变量
        line_color=(0,0,0)
        pygame.font.init()
        pygame.draw.rect(window,(255,255,255),(0,0,width+textwidth,height))
    direction=[[0,1],[0,-1],[-1,0],[1,0],[0,0]]
    turn=0
    visitcell=0
    totalcell=0
    info=[[0] * 100 for _ in range(100)]
    block=[[0] * 100 for _ in range(100)]
    visit=[[0] * 100 for _ in range(100)]

def getcolor(x,y):
    global c
    if (block[x][y]>=1):
        return (125,255,125)
    if (block[x][y]<0):
        return (0,0,0)
    i=info[x][y]
    if (i==0):
        return (255,255,255)
    if (i>10):
        i=10
    d=int(55+(1000/(i+5)))
    return (d,d,d)

def checkquit():
    event=pygame.event.get()
    for e in event:
        #设定窗口在点击关闭后结束运行
        if e.type==pygame.QUIT:
            return False
    return True

class Robot:
    x=0
    y=0
    p=0
    m=0


    def setpara(self,lst):
        self.para=lst

    def setposition(self,x,y):
        if (x==-1 and y==-1):
            while True:
                self.x=random.randint(0,map_size[0]-1)
                self.y=random.randint(0,map_size[1]-1)
                if (block[self.x][self.y]>=0):
                    break
            block[self.x][self.y]+=1
            return 1

        if (not check(x,y)):
            return 0
        self.x=x
        self.y=y
        return 1


    def update(self):
        global disp
        if (disp):
            draw_rect((self.x,self.y),getcolor(self.x,self.y))

    def output(self):
        print(self.x,self.y)

    def move(self):
        global visitcell,visit
        if (visit[self.x][self.y]==0):
            visitcell=visitcell+1
            visit[self.x][self.y]=1
        #self.output()
        if (self.p!=len(direction)-1):
            info[self.x][self.y]+=self.m
        block[self.x][self.y]-=1
        self.update()
        self.x+=direction[self.p][0]
        self.y+=direction[self.p][1]
        #self.output()
        block[self.x][self.y]+=1
        self.update()

    def clear(self):
        draw_rect((self.x,self.y),(255,255,255))


    def work(self):
        lst=[]
        for i in range(len(direction)-1):
            if check(self.x+direction[i][0],self.y+direction[i][1]):
                #print(self.x+direction[i][0],self.y+direction[i][1],info[self.x+direction[i][0]][self.y+direction[i][1]])
                lst.append(1/(info[self.x+direction[i][0]][self.y+direction[i][1]]+0.01)**2)
            else:
                lst.append(0)

        self.p=roulette(lst)
        self.m=1


class Robot_swarm(Robot):
    para=[]

    def work(self):
        lst=[]
        for i in range(len(direction)-1):
            if check(self.x+direction[i][0],self.y+direction[i][1]):
                lst.append(self.para[0]**(2*info[self.x+direction[i][0]][self.y+direction[i][1]]))
            else:
                lst.append(0)
        lst.append(self.para[1]**2)

        self.p=roulette(lst)
        if (self.p==len(direction)-1):
            self.m=0
        else:
            self.m=1



class Robot_swarm1(Robot):
    para=[]

    def work(self):
        lst=[]
        blank=0
        for i in range(len(direction)-1):
            if check(self.x+direction[i][0],self.y+direction[i][1]):
                lst.append(self.para[0]**(2*info[self.x+direction[i][0]][self.y+direction[i][1]]))
                if (visit[self.x+direction[i][0]][self.y+direction[i][1]]==0):
                    blank+=1
            else:
                lst.append(0)
        lst.append(self.para[1]**2)

        self.p=roulette(lst)
        if (self.p==len(direction)-1):
            self.m=0
        else:
            self.m=1+(4-blank)/4


class Robot_dfs1(Robot):
    stack=0

    def __init__(self):
        self.stack=[]

    def work(self):
        lst=[]
        #print(len(self.stack))
        for i in range(len(direction)-1):
            if (check(self.x+direction[i][0],self.y+direction[i][1]) and info[self.x+direction[i][0]][self.y+direction[i][1]]==0):
                lst.append(1)
            else:
                lst.append(0)
        self.m=1
        if (sum(lst)==0):
            if (len(self.stack)==0):
                lst=[]
                for i in range(len(direction)-1):
                    if (check(self.x+direction[i][0],self.y+direction[i][1])):
                        lst.append(self.para[0]**(2*info[self.x+direction[i][0]][self.y+direction[i][1]]))
                    else:
                        lst.append(0)
                    self.p=roulette(lst)
            else:
                self.p=self.stack.pop()
        else:
            self.p=roulette(lst)
            self.stack.append(self.p^1)


class Robot_dfs2(Robot):
    stack=0

    def __init__(self):
        self.stack=[]

    def work(self):
        lst=[]
        #print(len(self.stack))
        for i in range(len(direction)-1):
            if (check(self.x+direction[i][0],self.y+direction[i][1]) and info[self.x+direction[i][0]][self.y+direction[i][1]]==0):
                lst.append(1)
            else:
                lst.append(0)
        self.m=1
        if (sum(lst)==0):
            if (len(self.stack)==0):
                lst=[]
                for i in range(len(direction)-1):
                    if (check(self.x+direction[i][0],self.y+direction[i][1])):
                        lst.append(self.para[0]**(2*info[self.x+direction[i][0]][self.y+direction[i][1]]))
                    else:
                        lst.append(0)
                    self.p=roulette(lst)
            else:
                self.p=self.stack.pop()
        else:
            self.p=roulette(lst)
            self.stack.append(self.p^1)
        if len(self.stack)>self.para[1]:
            self.stack.pop(0)


class Robot_dfs3(Robot):
    stack=0

    def __init__(self):
        self.stack=[]

    def work(self):
        lst=[]
        #print(len(self.stack))
        for i in range(len(direction)-1):
            if (check(self.x+direction[i][0],self.y+direction[i][1]) and info[self.x+direction[i][0]][self.y+direction[i][1]]==0):
                lst.append(1)
            else:
                lst.append(0)
        self.m=1
        if (len(self.stack)>self.para[1] or sum(lst)==0):
            if (len(self.stack)==0):
                lst=[]
                for i in range(len(direction)-1):
                    if (check(self.x+direction[i][0],self.y+direction[i][1])):
                        lst.append(self.para[0]**(2*info[self.x+direction[i][0]][self.y+direction[i][1]]))
                    else:
                        lst.append(0)
                    self.p=roulette(lst)
            else:
                self.p=self.stack.pop()
        else:
            self.p=roulette(lst)
            self.stack.append(self.p^1)


def strdisplay(s,x,y,z):
    global width
    myfont = pygame.font.SysFont('Comic Sans MS', z)
    textsurface = myfont.render(s, False, (0, 0, 0))
    window.blit(textsurface,(width+x,y))


def strclear(s,x,y,z):
    global width
    myfont = pygame.font.SysFont('Comic Sans MS', z)
    textsurface = myfont.render(s, False, (255, 255, 255))
    window.blit(textsurface,(width+x,y))



def display_init():
    global totalcell
    strdisplay('Time:',20,100,20)
    strdisplay('Cells Covered:',20,200,20)
    strdisplay('Cells Total:',20,300,20)
    strdisplay(str(totalcell),20,350,20)
    #strdisplay('Cover Percentage:',20,300,20)

def textdisplay():
    global visitcell,totalcell,turn
    strdisplay(str(turn),20,150,20)
    strdisplay(str(visitcell),20,250,20)
    #strdisplay(str(int(visitcell/totalcell*100)/100.0)+'%',20,350,20)

def textclear():
    global visitcell,totalcell,turn
    strclear(str(turn),20,150,20)
    strclear(str(visitcell),20,250,20)
    #strclear(str(int(visitcell/totalcell*10000)/100.0)+'%',20,350,20)


def map_init():
    global totalcell,disp
    if (disp):
        global rect_size,width,height
        rect_size=((width-2*edge)//map_size[0],(height-2*edge)//map_size[1])   #方格大小
    for i in range(map_size[0]):
        for j in range(map_size[1]):
            if (block[i][j]==-1):
                if disp:
                    draw_rect((i,j),(0,0,0))
            else:
                totalcell+=1
    if (disp):
        display_init()


def main(robot_num=100,algorithm_id=0,parameter=[],_map_size=(100,100),path='',cover_ratio=0.99,fps=60):
    global visitcell,rect_size,totalcell,turn,disp,map_size,start_pos
    map_size=_map_size
    if (fps==0):
        disp=0
    else:
        disp=1
    init()
    algorithm_list=[Robot,Robot_swarm,Robot_swarm1,Robot_dfs1,Robot_dfs2,Robot_dfs3]
    load_map(path)
    #print(totalcell)
    map_init()

    robot=[]
    for i in range(robot_num):
        robot.append(algorithm_list[algorithm_id]())
        robot[i].setposition(start_pos[0],start_pos[1])
        robot[i].setpara(parameter)
        #robot[i].output()
    running=1
    while running:
        turn+=1
        for i in range(robot_num):
            robot[i].work()
        for i in range(robot_num):
            robot[i].move()
        if disp:
            running=checkquit()
            clock.tick(fps)
            textdisplay()
            pygame.display.flip()
        if (visitcell>=totalcell*cover_ratio):
            if (disp):
                strdisplay('Coverage Complete',20,400,20)
                pygame.display.flip()
                while running:
                    running=checkquit()
                    time.sleep(0.01)
            break
        if (disp):
            textclear()
    print(turn)
    pygame.quit()
    return turn


def trial(num,robot_num=50,algorithm_id=1,parameter=[],_map_size=(100,100),path='',cover_ratio=0.99):
    t=[]
    for i in range(num):
        t.append(main(robot_num,algorithm_id,parameter,_map_size,path,cover_ratio,0))
    print(sum(t)/len(t))
    return sum(t)/len(t)

#0.轮盘赌
#1.黄蜂群 [alpha,beta]
#2.启发式黄蜂群 [alpha]
#3.深度优先搜索 [alpha]
#4.栈限长dfs [alpha,len]
#5.队列限长dfs [alpha,len]
if __name__ == "__main__":
    main(10,1,[0.1,0],(10,10),'',fps=1.5)