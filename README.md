<h1>User-Designed-Connective-Structures</h1>
Our idea is to have a software such that takes in user input and output a curve for marble track

<h1>Instructions</h1>
https://www.edrawingsviewer.com/download-edrawings for viewing DFX on local computer <br>
https://www.onshape.com/en/ for viewing and editing DFX online<br>

The folder we mainly use will be "Turn2D3D" and other folders will not be directly related to the project itself but research oriented.<br>
The user can run Sketch.py in Turn2D3D, and use right clicks to create curves (every four right clicks will create 4 control points for a Bezier curve), the points of Bezier curve will be output in a text file named curveCoordinates.txt, which is used automatically to generate curves in dxf format and the file so far is named "test.dxf". <br>

<h1>Libraries</h1>
os <br>
wxpython <br>
math <br>
random <br>
numpy <br>
PIL <br>
dxfwrite(I include this in the repository so user can place it into their library folder) <br>
