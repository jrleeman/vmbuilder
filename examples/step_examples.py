# This is an example of how to build a basic velocity model for use
# with the rate and state friction tool or the control file builder
# tool.  All modes of making velocity steps and slide-hold-slide 
# tests are shown.

# Import the velocity tool
import rsffs

# Create an instance of the velocity model class
vm = rsffs.VelocityModel()

#
# Let's make a velocity step thats sliding at 1 um/s for a total
# of 5 seconds. 
#
 
# Instance of the step class
step1 = vm.step()    

# When setting velocity duration must be set first do that we can
# automatically calculate the displacement  
step1.duration = 5.    

# Use the set_velocity function so displacment is calculated automatically
step1.set_velocity(1.) 

# Set the sampling rate of the data for the step, this can be done at any time
# before the step is added to the model
step1.Fs = 100.


#
# Using a similar technique lets make a step by specifying a velocity and 
# a total displacement, automatically calculate the duration.
#

# Instance of the step class
step2 = vm.step()

# Set the velocity of sliding, here we just set it as a property of the object
# not using the set_velocity function since we will be calculating duration.
step2.velocity=10.

# Set the desired displacement and automatically calculate the duration of 
# the step
step2.set_displacement(150)

# Set the sampling rate of the data for the step, this can be done at any time
# before the step is added to the model
step2.Fs = 100.

#
# Now make some hold steps using the hold function.  You could do this all
# manually, but this wraps it all to be quicker.
#

# Instance of the step class
step3 = vm.step()

# Make step 3 a hold, calling with the duration of the hold
step3.hold(10)

# Set the sampling rate of the data for the step, this can be done at any time
# before the step is added to the model
step3.Fs = 10.


#
# Now we add the steps to the model in the order we want, remember you can add
# the same step multiple times.  You could wait until right before this to set
# all step sampling rates if desired.  Also the steps with the same velocity,
# but different sampling rates could be used to account to changing sampling
# rates in the middle of a step.
#
# You can also call the steps anything you want such as "10shold" or 
# "v30d100" to designate their properties.
#

vm.add_step(step1)
vm.add_step(step2)
vm.add_step(step3)
vm.add_step(step2)
vm.add_step(step1)

# Make a plot so we can inspect our model
vm.plot()