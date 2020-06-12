# 多机器人地图覆盖仿真
## 开发环境及依赖项
- python 3.8.2
  - pygame
  - PySide2
  - pyqtgraph (pypi版本暂不支持PySide2，使用`pip install git+https://github.com/pyqtgraph/pyqtgraph`命令进行安装
  - numpy

## 关于发布的打包程序

下载整个relese文件夹，运行menu.exe。

1. map文件夹中为地图文件，在程序中创建的地图会自动保存在该文件夹下。
2. main.ui为界面配置文件，需放在.exe文件同一文件夹下。