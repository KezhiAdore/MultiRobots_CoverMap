import pygame
import yaml
from sys import exit

class Makemap:
    def __init__(self,xlen,ylen,filename):
        self.xlen=xlen
        self.ylen=ylen
        self.filename=filename
        self.weight=1000
        self.height=1000
        self.edge=50
        self.rect_size=((self.weight-2*self.edge)//self.xlen,(self.height-2*self.edge)//self.ylen)
        self.fps=60
        self.line_color=(0,0,0)

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
        choose=[]
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
                                if [i,j] not in choose:
                                    choose.append([i,j])
                    if event.button==3:
                        for i in range(Start[0],End[0]+1):
                            for j in range(Start[1],End[1]+1):
                                if [i,j] in choose:
                                    choose.remove([i,j])
                    start=(-1,-1)
            if start[0]>0:
                self.show_selected(self.trans(start),self.trans(tmp),(255,255,0))
            for point in choose:
                self.draw_rect(point,(255,0,0))
            self.draw_line()
            pygame.display.flip()
        data={'Map':{'xlen':self.xlen,'ylen':self.ylen},'Obstacles':choose}
        yaml_file=self.filename+'.yaml'
        file = open(yaml_file, 'w', encoding='utf-8')
        yaml.dump(data, file)
        file.close()
        pygame.quit()
