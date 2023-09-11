## Linux development
1. 
```
python -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install cmake numpy moderngl pyrr scipy openmesh PyQt5 PyOpenGL PyOpenGL_accelerate open3d
```

2. Choose one of the following:
```
python main.py

PYOPENGL_PLATFORM=x11 python opengl_open3d.py

python vis-gui.py
```

## Qt 3DViewer
### Qt 3DViewer is a compact tool for viewing 3D models in a user-friendly way. 

<br>This project is a compact and user-friendly application designed to showcase 
<br>3D models in a visually appealing manner. With support for a wide range of 
<br>file formats including .obj, .stl, .ply, .off, and .om.

Powered by Python the PyQt framework, the app use OpenGL, in combination 
<br>with ModernGL to render the 3D models and scenes in an interactive experience.
<br>Designed and developed by Alon Rubin.


### Movement:
- Rotate:  click and drag the <b>left mouse</b> button.
- Pan: click and drag the <b>right mouse</b> button.
- Zoom: use the <b>mouse wheel</b> to zoom in or out.

### Watch a video demo:

<a href="https://www.youtube.com/watch?v=ZwK2B9AODtw&ab_channel=ALONZUBINA" target="_blank">
<img src="https://i.ytimg.com/an_webp/ZwK2B9AODtw/mqdefault_6s.webp?du=3000&sqp=CNTB6Z4G&rs=AOn4CLCHnn6Hr9zfh7cAxOX0AsEJMwo2Yg" alt="Watch the series" width="340" height="180" border="10" />
</a>

### App preview:
![Alt text](https://github.com/alonrubintec/3DViewer/blob/master/resource/app_preview.PNG?raw=true "app_preview.png")

### How to install:

1. Install Python 3.9
2. Install requirements
3. run "main.py" file

## Like this project?

Check out other stuff that i make:
<br>https://github.com/alonrubintec
<br>https://www.artstation.com/alonzu
