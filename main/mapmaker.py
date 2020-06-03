import pygame
from sys import exit

class Makemap:
    def __init__(self,xlen,ylen,filename):
        self.xlen=xlen
        self.ylen=ylen
        self.filename=filename
        self.weight=900
        self.height=900
        self.edge=50
        self.rect_size=((self.weight-2*self.edge)//self.xlen,(self.height-2*self.edge)//self.ylen)
        self.fps=60
        self.line_color=(100,100,100)

    def load_map(self,path):
        try:
            with open('./map/'+path+'.txt','r') as f:
                x=f.readlines()
                x[0]=x[0].split()
                map_size=[int(i) for i in x[0]]
                x[1]=x[1].split()
                start_pos=[int(i) for i in x[1]]
                self.choose=[]
                for i in range(map_size[0]):
                    for j in range(map_size[1]):
                        if int(x[i+2][j]):
                            self.choose.append([i,j])
        except:
            start_pos=(-1,-1)
            print('Cannot load file {0}'.format(path+'.txt'))
            return False
        else:
            print('Successfully load file {0}'.format(path+'.txt'))
            return True

    def draw_line(self):
        start,end=[self.edge,self.edge],[self.weight-self.edge,self.height-self.edge]
        for i in range(start[0],end[0]+1,self.rect_size[1]):
            pygame.draw.line(self.window,self.line_color,(i,start[1]),(i,end[1]))
        for i in range(start[1],end[1]+1,self.rect_size[0]):
            pygame.draw.line(self.window,self.line_color,(start[0],i),(end[0],i))

    def draw_rect(self,point,color):
        left=point[0]*(self.rect_size[0])+self.edge
        top=point[1]*(self.rect_size[1])+self.edge
        rect_color_size=(self.rect_size[0]-1,self.rect_size[1]-1)
        pygame.draw.rect(self.window,color,((left+1,top+1),rect_color_size))

    def trans(self,pos):
        return [(pos[0]-self.edge)//self.rect_size[0],(pos[1]-self.edge)//self.rect_size[1]]

    def show_selected(self,start,end,color):
        for i in range(start[0],end[0]+1):
            for j in range(start[1],end[1]+1):
                self.draw_rect((i,j),color)

    def run(self):
        pygame.init()
        self.window=pygame.display.set_mode((self.weight,self.height))
        pygame.display.set_caption("地图制作")
        self.clock=pygame.time.Clock()   #时间控制
        running=True
        start=(-1,-1)
        self.choose=[]
        self.load_map(self.filename)
        while running:
            #设定窗口帧率
            self.clock.tick(self.fps)
            #处理窗口事件
            pygame.draw.rect(self.window,(255,255,255),(0,0,self.weight,self.height))
            for event in pygame.event.get():
                #设定窗口在点击关闭后结束运行
                if event.type==pygame.QUIT:
                    running=False
                if event.type==pygame.MOUSEBUTTONDOWN:
                    start=event.pos
                if event.type==pygame.MOUSEMOTION:
                    tmp=event.pos
                if event.type==pygame.MOUSEBUTTONUP:
                    end=event.pos
                    Start,End=self.trans(start),self.trans(end)
                    if event.button==1:
                        for i in range(Start[0],End[0]+1):
                            for j in range(Start[1],End[1]+1):
                                if [i,j] not in self.choose:
                                    self.choose.append([i,j])
                    if event.button==3:
                        for i in range(Start[0],End[0]+1):
                            for j in range(Start[1],End[1]+1):
                                if [i,j] in self.choose:
                                    self.choose.remove([i,j])
                    start=(-1,-1)
            if start[0]>0:
                self.show_selected(self.trans(start),self.trans(tmp),(255,255,0))
            for point in self.choose:
                self.draw_rect(point,(255,0,0))
            self.draw_line()
            pygame.display.flip()
        data={'Map':{'xlen':self.xlen,'ylen':self.ylen},'Obstacles':self.choose}
        map_file='map/'+self.filename+'.txt'
        file = open(map_file, 'w', encoding='utf-8')
        file.write(str(self.xlen)+' '+str(self.ylen)+'\n')
        file.write('-1 -1\n')
        for i in range(self.xlen):
            for j in range(self.ylen):
                if [i,j] in self.choose:
                    file.write('1')
                else:
                    file.write('0')
            file.write('\n')
        file.close()
        pygame.quit()
