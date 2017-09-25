#!/usr/bin/env python

import argparse
import rospy

from geometry_msgs.msg import Twist

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pyaudio

from std_msgs.msg import String
from std_srvs.srv import *
import os
import commands

class recognizer(object):

    def __init__(self):

        # initialize ROS
        self.speed = 0.2
        self.msg = Twist()

        # Start node
        rospy.init_node("recognizer")
        rospy.on_shutdown(self.shutdown)

        self._lm_param = "~lm"
        self._dict_param = "~dict"
        self._kws_param = "~kws"

        # you may need to change publisher destination depending on what you run
        self.pub_ = rospy.Publisher('~output', String, queue_size=1)

        if rospy.has_param(self._lm_param):
            self.lm = rospy.get_param(self._lm_param)
        else:
            rospy.loginfo("Loading the default acoustic model")
            self.lm = "/usr/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k"
            rospy.loginfo("Done loading the default acoustic model")

        if rospy.has_param(self._dict_param):
            self.lexicon = rospy.get_param(self._dict_param)
        else:
            rospy.logerr('No dictionary found. Please add an appropriate dictionary argument.')
            return

        if rospy.has_param(self._kws_param):
            self.kw_list = rospy.get_param(self._kws_param)
        else:
            rospy.logerr('kws cant run. Please add an appropriate keyword list file.')
            return
        self.start_recognizer()

    def start_recognizer(self):
        # initialize pocketsphinx. As mentioned in python wrapper
        rospy.loginfo("Initializing pocketsphinx")
        config = Decoder.default_config()
        rospy.loginfo("Done initializing pocketsphinx")

        # Hidden Markov model: The model which has been used
        config.set_string('-hmm', self.lm)
        #Pronunciation dictionary used
        config.set_string('-dict', self.lexicon)
        #Keyword list file for keyword searching
        config.set_string('-kws', self.kw_list)

        rospy.loginfo("Opening the audio channel")

	# Pocketsphinx requires 16kHz, mono, 16-bit little-Endian audio.
	# See http://cmusphinx.sourceforge.net/wiki/tutorialtuning
        stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1,
                        rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()
        rospy.loginfo("Done opening the audio channel")

        #decoder streaming data
        rospy.loginfo("Starting the decoder")
        self.decoder = Decoder(config)
        self.decoder.start_utt()
        rospy.loginfo("Done starting the decoder")

        # Main loop
        while not rospy.is_shutdown():
            # taken as is from python wrapper
            buf = stream.read(1024)
            if buf:
                self.decoder.process_raw(buf, False, False)
            else:
                break
            self.publish_result()

    def publish_result(self):
        """
        Publish the words
        """
        if self.decoder.hyp() != None:
            print ([(seg.word)
                for seg in self.decoder.seg()])
            seg.word = seg.word.lower()
            self.decoder.end_utt()
            self.decoder.start_utt()
            self.pub_.publish(seg.word)

    def shutdown(self):
        """
        command executed after Ctrl+C is pressed
        """
        rospy.loginfo("Stopping PocketSphinx")


if __name__ == "__main__":
    if len(sys.argv) > 0:
        start = recognizer()

