# EGR598-Intro-To-Python---Facial-Tracking-Robot-
EGR598 Intro To Python - "Facial Tracking Robot"

![IMG_0891](https://github.com/user-attachments/assets/0f376cfd-ca5e-4bbc-a6ae-e029342b3933)


User beaware, this code brings forth a robot that knocks stuff over on your desk.

### Idea/Exigency
I wanted to make this funny robot that knocks over things on my desk if i am not looking at it. My python code detects if you are looking away from the robot, and if you are it sends a trigger command to my ESP32 robot over UART. When this command is recieved by the robot, the robot first checks if there are any objects on the table to knock off with its servo. It can do this by sensing if an object is placed on it's pressure plate that connects two wires and pulls a digital pin low. If there isn't an object the robot does not move because that would ruin its inconspicuous nature.

###### Disclaimer:
This robot will detect in real time if you are looking at the robot. It does this by processing images coming from your webcam and detecting your gaze direction. Right now the code is set up for a robot placed to the left of the users webcam. 

### Code Explanation
It processes facial landmarks deciphered by Dlib, so it can create a black and white mask image of your eyeballs. It then counts the white space of your eyes and compares the left and right halves of each eye. Then comparing those ratios, I calculated the ratios of each eye (left eye and right). This is because one eye can give misguiding information if you are focused on something near to your face. For example, if your left eye is looking at your webcam the ratio of the left half will be bigger than your right half of the eye. So I applied my function to both eyeballs and creates a ratio of each eye. Additionally, to even process this image, I had to remove the eyelids around the detected eyes because that renders as white pixels when converting to a black and white image.

So with these ratios, I set the thresholds to determine if I am looking at the robot. If I am looking away from my robot, my python sends a UART command to my ESP32 to trigger.

For detecting if the user is blinking, I drew 3 horizontal lines. The main horizontal line across landmarks 36 and 39 for the left eye with 42 and 45 for the right eye. This is the main length of the eyeball. Then for the other two horizontal lines, I drew a line for the upper eyelid and lower eyelid (left eye upper [37-38], left eye lower[41-40]). I took the midpoint of these lines as a way to draw a verticle line to measure the height of the eyeball. Then the ratio for one eyeball was calculated with this eye length and height. If this ratio calculated for both eyes is within a set threshold. Then the code determines that the user is blinking. 


If you want a more generalized idea of how this code works consult the link below 
### my youtube video:
https://youtu.be/6CTSYtoE3rc?si=Kf9moJ3v6Br-dWex

### Implementation
To get this code running download the cameraTracking.py file for facial recognition.

Then download the arduino code and upload it to any arduino capable microcontroller.
###### (Change the baud rates in both pyhton and arduino files according to your microcontroller)
If you want a refrence image for what landmarks to use if you are adapting this code later on, that is also listed in the repository.
Lastly you need the facial landmarks.dat file for Dlib to process the face. (see bottom of readme file)

##### Dependencies
In order to run this code you must have all necessary libraries and their dependencies.
- OpenCV2
- Math
- Numpy
- Serial
- Time
- Dlib
Dlib proved to be the hardest to implement because of its dependencies like CMake.
If you chose to run this on a Mac I would recommend installing CMake with homebrew, by following this tutorial:


Additionally you will need the facial landmarks file for Dlib to recognize specific parts on the face.
I scraped the facial landmarks from someone else's github repo, so you can do the same in your implementation.

#### shape_predictor_68_face_landmarks.dat Link:
https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat

