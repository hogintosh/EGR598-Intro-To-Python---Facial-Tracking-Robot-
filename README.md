# EGR598-Intro-To-Python---Facial-Tracking-Robot-
EGR598 Intro To Python - "Facial Tracking Robot"

User, beaware this code brings forth laplaces demon in the form of a robot that knocks stuff over on your desk.




This robot will detect in real time if you are looking at the robot. It does this by processing images coming from your webcame and detecting your gaze direction. Right now the code is set up for a robot placed to the left of the users webcam. 

### Code Explanation
It processes facial landmarks deciphered by Dlib, so it can create a black and white mask image of your eyeballs. It then counts the white space of your eyes and compares the left and right halves of each eye. Then comparing those ratios, I calculated the ratios of each eye (left eye and right). This is because one eye can give misguiding information if you are focused on something near to your face. For example, if your left eye is looking at your webcam the ratio of the left half will be bigger than your right half of the eye. So I applied my function to both eyeballs and creates a ratio of each eye.

So with these ratios, I set the thresholds to determine if I am looking at the robot. If I am looking away from my robot, my python sends a UART command to my ESP32 to trigger.

For detecting if the user is blinking, I drew 3 horizontal lines. The main horizontal line across landmarks 36 and 39 for the left eye with 42 and 45 for the right eye. This is the main length of the eyeball. Then for the other two horizontal lines, I drew a line for the upper eyelid and lower eyelid (left eye upper [37-38], left eye lower[41-40]). I took the midpoint of these lines as a way to draw a verticle line to measure the height of the eyeball. Then the ratio for one eyeball was calculated with this eye length and height. If this ratio calculated for both eyes is within a set threshold. Then the code determines that the user is blinking. 

If you want a more generalized idea of how this code works consult my youtube video:
https://youtu.be/6CTSYtoE3rc?si=Kf9moJ3v6Br-dWex

In order to run this code you must have all necessary libraries and their dependencies.
- OpenCV2
- Math
- Numpy
- Serial
- Time
- Dlib
  Dlib proved to be the hardest to implement because of its dependencies like CMake.
If you chose to run this on a Mac I would recommend installing CMake with homebrew, by following this tutorial: 

