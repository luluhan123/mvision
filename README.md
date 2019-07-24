Automatic Tracking of Guidewire Tip From Fluoroscopic Videos Using RuSio Framework
====
 This code implemented the method of RuSio framework.
 
RuSio framework Overview
----
![Flowchar of RuSio framework](https://github.com/wangtseng/mvision/blob/master/doc/gtt/manuscript/figures/flowchart.png)
Prerequisites
----
Test on:
* Windows 10, 64 bits
* Linux Ubuntu 18 LTS, 64 bits
* MacOS

 Development Tool:
* PyCharm

 Development Language:
* Python (3.6)

 Require evironment to excute the python code:
* Anaconda
* Opencv

Environment Installation
----
You can simply follow with intruction on
http://www.cs.cmu.edu/~galeotti/methods_course/assignment-itkinstall.html for installing Python and SimpleITK for Python
 or

If you already had 64-bit Anaconda installed, use the command line to enter these commands one at a time (they may prompt you with questions) to update python and install python versions of both VTK and SimpleITK:
```Python
conda update conda
conda update matplotlib
conda update scipy
conda install vtk 
conda install -c simpleitk simpleitk=1.2.0
```
 Install opencv
```Python
pip install opencv-python
pip install opencv-contrib-python
```

Test Demo
----
After run msa_main.py, you will get this window:
![Window](https://github.com/wangtseng/mvision/blob/master/doc/gtt/Draft/figures/window.png)

 Simply check the box for Tracking or Guidewire tip Evaluation or both
![Check boxes](https://github.com/wangtseng/mvision/blob/master/doc/gtt/manuscript/figures/boxes.png) 

 Drag target video sequence into correct position to run RuSio framework
![Software window](https://github.com/wangtseng/mvision/blob/master/doc/gtt/Draft/figures/software%20.png)

Test Showcase
----
The segmentation collection of guidewire tip from RuSio framework in 8 consecutive frames from 128 to 135.
![Showcase](https://github.com/wangtseng/mvision/blob/master/doc/gtt/manuscript/figures/showcase.png)
