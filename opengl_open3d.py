from PyQt5 import QtCore      # core Qt functionality
from PyQt5 import QtGui       # extends QtCore with GUI functionality
from PyQt5 import QtOpenGL    # provides QGLWidget, a special OpenGL QWidget
from PyQt5 import QtWidgets

import OpenGL.GL as gl        # python wrapping of OpenGL
from OpenGL import GLU        # OpenGL Utility Library, extends OpenGL functionality
from OpenGL.arrays import vbo
import numpy as np
import open3d as o3d
import ctypes 
import sys                    # we'll need this later to run our Qt application

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    # call the init for the parent class

        self.resize(300, 300)
        self.setWindowTitle('Hello OpenGL App')
        
        self.glWidget = GLWidget(self)
        self.initGUI()
        
        timer = QtCore.QTimer(self)
        timer.setInterval(20)   # period, in milliseconds
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()
        
    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)

        gui_layout.addWidget(self.glWidget)

        sliderX = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))

        sliderY = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))

        sliderZ = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))

        gui_layout.addWidget(sliderX)
        gui_layout.addWidget(sliderY)
        gui_layout.addWidget(sliderZ)
        
class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(100, 100, 100))     # initialize the screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST)                       # enable depth testing

        self.initGeometry()

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0

    def setRotX(self, val):
        self.rotX = val

    def setRotY(self, val):
        self.rotY = val

    def setRotZ(self, val):
        self.rotZ = val
        
    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        
    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix()    # push the current matrix to the current stack

        gl.glTranslate(0.0, 0.0, -150.0)    # third, translate cube to specified depth
        # gl.glScale(20.0, 20.0, 20.0)       # second, scale cube
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        gl.glTranslate(-50, -50, -50)   # first, translate cube center to origin

        # Point size
        gl.glPointSize(3)
        
        ### NEW ###
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        stride = 6*4 # (24 bates) : [x, y, z, r, g, b] * sizeof(float)

        # PYOPENGL_PLATFORM=x11 python opengl_open3d.py
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glVertexPointer(3, gl.GL_FLOAT, stride, None)

        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        offset = 3*4 # (12 bytes) : the rgb color starts after the 3 coordinates x, y, z 
        gl.glColorPointer(3, gl.GL_FLOAT, stride, ctypes.c_void_p(offset))
        
        noOfVertices = self.noPoints
        gl.glDrawArrays(gl.GL_POINTS, 0, noOfVertices)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        ### NEW ###

        gl.glPopMatrix()    # restore the previous modelview matrix
        

    def initGeometry(self):
    
        vArray = self.LoadVertices()
        self.noPoints  = len(vArray) // 6
        print("No. of Points: %s" % self.noPoints)
        
        self.vbo = self.CreateBuffer(vArray)

        
    ### NEW ###

    def LoadVertices(self):
        
        pcd = o3d.io.read_point_cloud("test_files/heart.ply")
        print(pcd)
        print("Pointcloud Center: " + str(pcd.get_center()))
    
        points = np.asarray(pcd.points).astype('float32')
        colors = np.asarray(pcd.colors).astype('float32')
        
        attributes = np.concatenate((points, colors),axis=1)
        print("Attributes shape: " + str(attributes.shape))
        
        return attributes.flatten()

    def CreateBuffer(self, attributes):
        bufferdata = (ctypes.c_float*len(attributes))(*attributes) # float buffer
        buffersize = len(attributes)*4                             # buffer size in bytes 

        # vbo = gl.glGenBuffers(1)
        # gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        # gl.glBufferData(gl.GL_ARRAY_BUFFER, buffersize, bufferdata, gl.GL_STATIC_DRAW) 
        # gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        my_vbo = vbo.VBO(np.array(bufferdata, dtype=np.float32))
        my_vbo.bind()
        return my_vbo
        
    ### NEW ###


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())