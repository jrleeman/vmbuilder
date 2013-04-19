#!/usr/bin/env python

"""
vmbuilder.py : Tool to allow the building of a velocity model
that could be used for a variety of modeling and control tools.
"""

__author__ = "John Leeman"
__copyright__ = "Copyright 2013, John R. Leeman"
__credits__ = ""
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "John Leeman"
__email__ = "kd5wxb@gmail.com"
__status__ = "Development"


import numpy as np
import matplotlib.pylab as plt
from math import log,exp


class VelocityModel:
    """
    Class that makes the velocity model that can ultimately be used
    in the rate and state model.  
    """
    def __init__(self):
        """
        Make the initial arrays to hold velocity model steps.
        """
        self.time         = np.empty(0)
        self.displacement = np.empty(0)
        self.velocity     = np.empty(0)
        self.sampling     = np.empty(0)
        self.steps        = []
        self.FirstStep    = True
    
    class step:
        """
        Make a velocity step 
        """
        def __init__(self):
            """
            Parameters of the velocity step
            """
            self.velocity     = None
            self.duration     = None
            self.displacement = None
            self.Fs           = None
            
        def set_velocity(self, velocity):
            """
            Set the velocity of the step and calculate the displacement based
            on the duration of sliding.  
            """
            if self.duration == None:
                print """Warning! You must set a duration of sliding before
                       setting the velocity for displacement to be
                       calculated properly!"""
             
            self.velocity = velocity
            self.displacement = self.velocity * self.duration
        
        def set_displacement(self, displacement):
            """
            Set the displacement of the step and calculate the velocity based
            on the accumulated displacement when sliding.  
            """
            if self.velocity == None:
                print """Warning! You must set a velocity of sliding before
                       setting the displacement for duration to be
                       calculated properly!"""
             
            self.displacement = displacement
            self.duration = self.displacement/self.velocity
            
        def hold(self,duration):
            """
            Create a hold step during an experiment.  This just automates what
            could be done manually, but makes it nicer.
            """
            self.velocity = 0.0
            self.duration = duration
            self.displacement = 0.0
        
    def add_step(self,step):
        """
        Add a velocity step to the velocity model.
        Takes a step instance and adds it into the model.
        """
        # TODO: 
        #       add sampling array
   
        # Check if it is the fist step
        if len(self.steps) != 0:
            self.FirstStep = False
            
        # Add step to list of steps
        self.steps.append(step)
        
        # If this is the first step we must treat it special since 
        # time 0 is included
        if self.FirstStep == True:
            time_array = np.arange(1./step.Fs,step.duration+1./step.Fs,1./step.Fs)
        
        else:
            time_array = self.time[-1] + np.arange(1./step.Fs,step.duration+1./step.Fs,1./step.Fs)
        
        number_of_points = len(time_array)
        vel_array  = step.velocity * np.ones(number_of_points)
        disp_array = np.arange(1./step.Fs,step.duration+1./step.Fs,1./step.Fs) * step.velocity
        
        if self.FirstStep == False:
            disp_array = disp_array + self.displacement[-1]

        samp_array = step.Fs * np.ones(number_of_points)
        
        ##
        #print time_array
        print len(time_array)
        
        self.velocity     = np.concatenate((self.velocity,vel_array))
        self.time         = np.concatenate((self.time,time_array))
        self.displacement = np.concatenate((self.displacement,disp_array))
        self.sampling     = np.concatenate((self.sampling,samp_array))
        
    def plot(self):
        """
        Make a plot of the current velocity model.  Plot the following plots:
        1) Time, Velocity
        2) Time, Fs
        3) Time, Displacement
        4) Displacement, Velocity
        """   
        # Make figure and four subplots
        fig = plt.figure(0)
        ax1 = plt.subplot(411)
        ax2 = plt.subplot(412)
        ax3 = plt.subplot(413)
        ax4 = plt.subplot(414)
        
        # Set x-labels
        ax1.set_xlabel('Time')
        ax2.set_xlabel('Time')
        ax3.set_xlabel('Time')
        ax4.set_xlabel('Displacement')
        
        # Set y-labels
        ax1.set_ylabel('Velocity')
        ax2.set_ylabel('Fs')
        ax3.set_ylabel('Displacement')
        ax4.set_ylabel('Velocity')
        
        # Plot the data on the subplots
        ax1.plot(self.time,self.velocity,color='k')
        ax2.plot(self.time,self.sampling,color='k')
        ax3.plot(self.time,self.displacement,color='k')
        ax4.plot(self.displacement,self.velocity,color='k')
        
        # Set the plot limits
        # pad is the percent to be padded
        pad = 1.2
        # x-limits 
        ax1.set_xlim(0,max(self.time))
        ax2.set_xlim(0,max(self.time))
        ax3.set_xlim(0,max(self.time))
        ax4.set_xlim(0,max(self.displacement))
        
        # y-limits 
        ax1.set_ylim(0,max(self.velocity)*pad)
        ax2.set_ylim(0,max(self.sampling)*pad)
        ax3.set_ylim(0,max(self.displacement)*pad)
        ax4.set_ylim(0,max(self.velocity)*pad)
        
        # Show the plot
        plt.show()
