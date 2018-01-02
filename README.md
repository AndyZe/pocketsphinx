# Modified ROS wrapper for pocketsphinx  

The following repositories were used in our wrapper, but are not required for installation:

* Original repository: https://github.com/mikeferguson/pocketsphinx  
  
* Also used repo: https://github.com/gorinars/ros_voice_control  

It uses up-to-date pocketsphinx features and is independent of most external dependencies.  
  
Current repository is a ROS wrapper which incorporates those features. 
  
## Installation 
1)   
    ```
    sudo apt-get install -y python python-dev python-pip build-essential swig libpulse-dev git
    sudo apt-get install python-pyaudio
    ```

2) pocketsphinx: You will need to have pip preinstalled for this to work
    ```
    sudo pip install pocketsphinx
    ```
3) Download and copy the hub4wsj_sc_8k language model  to /usr/share/pocketsphinx/model/hmm/en_US/. It can be found [here](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/Archive/US%20English%20HUB4WSJ%20Acoustic%20Model/)

4) Git clone our repository into the your catkin workspace's src folder:
  ```
  cd ~/catkin_ws/src
  git clone https://github.com/UTNuclearRoboticsPublic/pocketsphinx.git  
  ```
## Usage

### If you want to decode from a microphone stream:
1. From pocketsphinx.launch set stream to true
2. 
```
roslaunch pocketsphinx pocketsphinx.launch
```

### If you want to decode from a wav file:
1. Fron pocketsphinx.launch set stream to false 
2. set wavpath to the desired wav file path 
3.
``` 
roslaunch pocketsphinx pocketsphinx.launch
```

## Using your own keywords

You can run this with any set of words. To do that, you need lexicon and keyword list files (check voice_cmd.dic and voice_cmd.kwlist for details).

Word pronunciations for English can be found in CMUdict

You can also download pocketsphinx acoustic models for several other languages here

Read more about pocketsphinx on the official website: http://cmusphinx.sourceforge.net
