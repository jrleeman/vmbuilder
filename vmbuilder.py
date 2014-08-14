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
from math import log,exp, floor

end_voltage = 0.

def SecondsToHMS(seconds):
    hours = floor(seconds/3600.)
    minutes = floor((seconds - hours * 3600)/60.)
    seconds = seconds - hours * 3600 - minutes * 60
    return '%02d:%02d:%02d' %(hours,minutes,seconds)

class VelocityModel:
    """
    Class that makes the velocity model that can ultimately be used
    in the rate and state model.  
    """
    def __init__(self):
        """
        Make the initial arrays to hold velocity model steps.
        """
        self.time         = np.zeros(1)
        self.displacement = np.zeros(1)
        self.voltage = np.zeros(1)
        self.velocity     = np.zeros(1)
        self.sampling     = np.zeros(1)
        self.steps        = []
        self.FirstStep    = True
        self.final_voltage = None
        self.final_displacement = None
        self.final_time = None
    
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
            self.start_time   = None
            self.number       = None
       
        def hold(self,duration):
            """
            Create a hold step during an experiment.  This just automates what
            could be done manually, but makes it nicer.
            """
            self.velocity = 0.0
            self.duration = duration
            self.displacement = 0.0

    def write_file(self,fname):
        #mm/V
        f = open(fname,'w')
        for v in self.voltage:
            f.write('%f\n' %v)
        f.close()
        
    def add_step(self,step,edit=False):
        """
        Add a velocity step to the velocity model.
        Takes a step instance and adds it into the model.
        """

        if step.velocity == None:
            print "Error: No step velocity set."
            return

        if step.displacement == None:
            step.displacement = step.velocity * step.duration

        if step.duration == None:
            step.duration = step.displacement/step.velocity

        if self.FirstStep == True:
            step.number = 1
            self.FirstStep = False
        
        if step.number == None:
            step.number = self.steps[-1].number + 1
       
        if edit:
            self.steps[step.number-1] = step
        else:
            # Add step to list of steps
            self.steps.append(step)
        

    def build_model(self):
        self.time         = np.zeros(1)
        self.displacement = np.zeros(1)
        self.voltage = np.zeros(1)
        self.velocity     = np.zeros(1)
        self.sampling     = np.zeros(1)
        
        i = 1
        for step in self.steps:
            step.number = i
            i += 1

        for step in self.steps:
            # If this is the first step we must treat it special since 
            # the time zero velocity needs to be set as does Fs
            if step.number == 1:
                self.velocity[0] = step.velocity
                self.sampling[0] = step.Fs
            
            time_array = self.time[-1] + np.arange(1./step.Fs,step.duration+1./step.Fs,1./step.Fs)
            
            step.start_time = time_array[0]

            number_of_points = len(time_array)
            vel_array  = step.velocity * np.ones(number_of_points)
            disp_array = np.arange(1./step.Fs,step.duration+1./step.Fs,1./step.Fs) * step.velocity
            
            if self.FirstStep == False:
                disp_array = disp_array + self.displacement[-1]

            samp_array = step.Fs * np.ones(number_of_points)
            
            self.velocity     = np.concatenate((self.velocity,vel_array))
            self.time         = np.concatenate((self.time,time_array))
            self.displacement = np.concatenate((self.displacement,disp_array))
            self.sampling     = np.concatenate((self.sampling,samp_array))

        self.voltage = self.displacement/self.calibration/1000.
        self.final_displacement = self.displacement[-1]
        self.final_time = self.time[-1]
        self.final_voltage = self.voltage[-1]

    def print_summary(self):

        end_time_str = SecondsToHMS(self.final_time)

        print '\n'
        print '-------------------------------------------------------------------'
        print '| Step Number | Start Time | Velocity | Displacement |  Duration  |'
        print '|             |    hh:mm:ss|      um/s|            um|           s|'
        print '------------------------------------------------------------------|'
        for step in self.steps:
            start_str = SecondsToHMS(step.start_time)
            print '|%13d|%12s|%10.2f|%14.2f|%12.2f|' %(step.number,start_str,step.velocity,step.displacement,step.duration)
        
        print '-------------------------------------------------------------------'
        print 'Total Time [hh:mm:ss]: %s' %end_time_str
        print 'Total Delta V: %.4f' %model.final_voltage
        print 'Total Displacement [mm]: %.4f' %(model.final_displacement/1000.)

    def write_mdsummary(self,fname):
        f = open(fname,'w')

        end_time_str = SecondsToHMS(self.time[-1])

        f.write('# Control File Summary\n')
        f.write('### %s\n\n' %fname)
        f.write('| Step Number | Start Time | Velocity | Displacement |  Duration  |\n')
        f.write('|             |    hh:mm:ss|      um/s|            um|           s|\n')
        f.write('--------------|------------|----------|--------------|------------|\n')
        for step in self.steps:
            start_str = SecondsToHMS(step.start_time)
            f.write('|%13d|%12s|%10.2f|%14.2f|%12.2f|\n' %(step.number,start_str,step.velocity,step.displacement,step.duration))
        
        f.write('\n###Total Time [hh:mm:ss]: %s\n' %end_time_str)
        f.write('###Total Delta V: %.4f\n' %model.final_voltage)
        f.write('###Total Displacement [mm]: %.4f\n' %(model.final_displacement/1000.))

        #f.write('\n### Total Time [hh:mm:ss]: %s\n' %end_time_str)
        #f.write('### Total Delta V: %.4f\n' %end_voltage)
        f.close()


    def plot(self):
        """
        Make a plot of the current velocity model.  Plot the following plots:
        1) Time, Velocity
        2) Time, Fs
        3) Time, Displacement
        4) Displacement, Velocity
        """   
        # Make figure and four subplots
        fig = plt.figure(figsize=(12,8))
        ax1 = plt.subplot(411)
        ax2 = plt.subplot(412)
        ax3 = plt.subplot(413)
        ax4 = plt.subplot(414)
        plt.subplots_adjust(hspace=0.4)

        # Set x-labels
        ax1.set_xlabel('Time [s]')
        ax2.set_xlabel('Time [s]')
        ax3.set_xlabel('Time [s]')
        ax4.set_xlabel('Displacement [um]')
        
        # Set y-labels
        ax1.set_ylabel('Velocity [um/s]')
        ax2.set_ylabel('Fs [Hz]')
        ax3.set_ylabel('Displacement [um]')
        ax4.set_ylabel('Velocity [um/s]')
        
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
        ax4.set_xlim(min(self.displacement),max(self.displacement))
        
        # y-limits 
        ax1.set_ylim(0,max(self.velocity)*pad)
        ax2.set_ylim(0,max(self.sampling)*pad)
        ax3.set_ylim(0,max(self.displacement)*pad)
        ax4.set_ylim(0,max(self.velocity)*pad)
        
        # Show the plot
        plt.show()

if __name__ == "__main__":

    class Modes:
        def __init__(self):
            self.edit_mode = False
            self.insert_mode = False
            self.step = None

    def ProcessCommand(cmd,modes):
        write_cmd = True

        arg = cmd.split(' ')
        if arg[0] == 'd':
            model.steps.pop(int(arg[1])-1)

        elif arg[0] == 'i':
            modes.insert_mode = True
            insert_loc = int(arg[1]) - 1
            step = model.step()
            step.Fs = Fs
            step.hold(1)
            model.steps.insert(insert_loc,step)

        elif arg[0] == 's':
            write_cmd = False
            model.build_model()
            model.print_summary()
        
        elif arg[0] == 'e':
            step = model.steps[int(arg[1])-1]
            modes.step = step
            print 'Edit step %d' %(int(arg[1]))
            modes.edit_mode = True

        elif arg[0] == 'h':
            if modes.edit_mode == False:
                step = model.step()
                step.Fs = Fs
            else:
                step = modes.step
                step.duration = None
                step.displacement = None
                step.velocity = None
            step.hold(float(arg[1]))
            #try:
            model.add_step(step,modes.edit_mode)
            print 'Added hold of %f seconds' %float(arg[1])
            modes.edit_mode = False
            #except:
            #    print 'Error adding hold'
                
        elif arg[0] == 'p':
            write_cmd = False
            model.build_model()
            model.plot()

        elif arg[0] == 'v':
            if modes.edit_mode == False:
                step = model.step()
                step.Fs = Fs
            else:
                step = modes.step
                step.duration = None
                step.displacement = None
                step.velocity = None
            
            step.velocity = float(arg[1])

            if arg[2] == 't':
                step.duration = float(arg[3])
            elif arg[2] == 'd':
                step.displacement = float(arg[3])
            #try:
            model.add_step(step,modes.edit_mode)
            print 'Added velocity of %f um/s for %f um and %f s' %(step.velocity,step.displacement,step.duration)
            modes.edit_mode = False
            modes.insert_mode = False
            #except:
            #print 'Error adding velocity'
        else:
            write_cmd = False
            print 'Invalid command'
        if write_cmd:
            f_cmds.write('%s \n' %cmd) 

    model = VelocityModel()
    do_commands = True

    fname = raw_input('Output name: ')
    calibration = input('Calibration [mm/V]: ')
    model.calibration = -1*calibration
    Fs = input('Update Rate [Hz]: ')

    # Make the command storage file
    f_cmds = open('%s_commands.txt'%fname,'w')
    #f_cmds.write('%s\n' %fname)
    #f_cmds.write('%f\n' %calibration)
    #f_cmds.write('%f\n' %Fs)
     
    modes = Modes()
    modes.edit_mode = False
    modes.insert_mode = False  

    while do_commands:
        
        cmd = raw_input('>')
        arg = cmd.split(' ')

        if arg[0] == 'q':
            do_commands = False
            f_cmds.close()
            model.build_model()
            model.write_file(fname)
            model.write_mdsummary('%s_summary.md' %fname)
            model.print_summary()

        elif arg[0] == 'run':
            f = open(arg[1],'r')
            for cmd in f.readlines():
                cmd = cmd.strip('\n')
                print 'Running: ', cmd
                ProcessCommand(cmd,modes)
            f.close()

        else:
            ProcessCommand(cmd,modes)


        