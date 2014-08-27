Velocity Model Builder: vmbuilder
=========

This is a tool to build velocity models of slide-hold-slide tests and velocity
step tests commonly conducted in friction experiments.  Many things are rather crudely accomplished, but this fills a hole in our toolset by allowing editing of profiles.  Maintained by [John R. Leeman](http://www.johnrleeman.com/) of the [Penn State Rock and Sediment Mechanics Laboratory](http://rockmechanics.psu.edu/).  

## Use Instructions

1. Start the program as you would any other python script *python vmbuilder.py*
2. Enter the output file name.  Good practice is to include the type of tests (velocity steps or slide-hold-slides), transducer, gain setting, and the update rate of the file.
3. Enter the calibration for the DCDT that you will use in the experiment.
4. Enter the update rate.  This is how many times per second the target voltage.
5. At the command prompt build your velocity profile with the following commands:

**v [velocity] d [displacement]** -  Create a velocity step that continues to a fixed displacement.  v 10 d 50 produces a 10 $\mu$m/s step for 50 $\mu$m.

**v [velocity] t [time]** - Create a velocity step that lasts for the specified time.  v 10 d 5 produces a 10 $\mu$m/s step for 5 seconds.

**h [seconds]** - Create a hold for the specified number of seconds.  *h 100* generates a 100 second hold.

**d [step]** - Delete a step.  Enter the step number, so *d 5* would delete the 5th velocity step.

**i [step]** - Insert a step before the given step number. This puts a 1 second hold in that should then be edited to your desired step.  

**s** - Print a summary of the current velocity model.

**e [step]** - Edit a step.  Enter *e 6* to edit step 6.  The prompt will reappear and whatever you enter will replace that step.

**p** - Produce a plot of the current velocity model.

**run [command file name]** - Load and run commands stored from a previous session.  This is useful to make the same sequence of velocities for different transducers, calibrations, or for new sequences that only require editing a previous sequence.  

**q** - Write out all model files and quit the program.

## Outputs

*Control File* - This file is called whatever you entered as the output name.  It is a text file with voltages in it that are to put clocked out of the DAC at the specified rate.

*Command File* - Contains the command history of that session.  This can be used to recreate the profile with different calibrations or rate settings.  Named as *your output name_commands.txt*

*Summary File* - This is a plain text file written in a multi-markdown format.  The summary contains a table of the step number, experiment time at which the step starts, velocity, displacement, and duration.  At the bottom of the file the total time, voltage change, and displacement are computed.  This can be viewed and is easily readable as plain text, or the file can be nicely rendered with any markdown viewer such as [Marked](http://marked2app.com/).


## Example

Say we want an experiment that begins with a 20 second hold, then steps from 1 to 10 $mu$m/s with a displacement of 50 $\mu$m each 3 times, then does a series of slide-hold-slides and view the summary.  I'll demonstrate both time and displacement commands in the example. The command sequence would be:

<pre>
h 20
v 1 d 50
v 10 d 50
v 1 t 50
v 10 t 5
v 1 d 50
v 10 d 50
h 1
v 10 d 50
h 10
v 10 d 50
h 100
h 1000
v 10 d 50
s

-------------------------------------------------------------------
| Step Number | Start Time | Velocity | Displacement |  Duration  |
|             |    hh:mm:ss|      um/s|            um|           s|
------------------------------------------------------------------|
|            1|    00:00:00|      0.00|          0.00|       20.00|
|            2|    00:00:20|      1.00|         50.00|       50.00|
|            3|    00:01:10|     10.00|         50.00|        5.00|
|            4|    00:01:15|      1.00|         50.00|       50.00|
|            5|    00:02:05|     10.00|         50.00|        5.00|
|            6|    00:02:10|      1.00|         50.00|       50.00|
|            7|    00:03:00|     10.00|         50.00|        5.00|
|            8|    00:03:05|      0.00|          0.00|        1.00|
|            9|    00:03:06|     10.00|         50.00|        5.00|
|           10|    00:03:11|      0.00|          0.00|       10.00|
|           11|    00:03:21|     10.00|         50.00|        5.00|
|           12|    00:03:26|      0.00|          0.00|      100.00|
|           13|    00:05:06|      0.00|          0.00|     1000.00|
|           14|    00:21:46|     10.00|         50.00|        5.00|
-------------------------------------------------------------------
Total Time [hh:mm:ss]: 00:21:51
Total Delta V: -0.4500
Total Displacement [mm]: 0.4500
</pre>

Oops! We forgot to shear between the 100 and 1000 second holds! No problem, we'll insert a step and edit it to be a re-shear: 

<pre>
i 13
e 13
v 10 d 50
s

-------------------------------------------------------------------
| Step Number | Start Time | Velocity | Displacement |  Duration  |
|             |    hh:mm:ss|      um/s|            um|           s|
------------------------------------------------------------------|
|            1|    00:00:00|      0.00|          0.00|       20.00|
|            2|    00:00:20|      1.00|         50.00|       50.00|
|            3|    00:01:10|     10.00|         50.00|        5.00|
|            4|    00:01:15|      1.00|         50.00|       50.00|
|            5|    00:02:05|     10.00|         50.00|        5.00|
|            6|    00:02:10|      1.00|         50.00|       50.00|
|            7|    00:03:00|     10.00|         50.00|        5.00|
|            8|    00:03:05|      0.00|          0.00|        1.00|
|            9|    00:03:06|     10.00|         50.00|        5.00|
|           10|    00:03:11|      0.00|          0.00|       10.00|
|           11|    00:03:21|     10.00|         50.00|        5.00|
|           12|    00:03:26|      0.00|          0.00|      100.00|
|           13|    00:05:06|     10.00|         50.00|        5.00|
|           14|    00:05:11|      0.00|          0.00|     1000.00|
|           15|    00:21:51|     10.00|         50.00|        5.00|
-------------------------------------------------------------------
Total Time [hh:mm:ss]: 00:21:56
Total Delta V: -0.5000
Total Displacement [mm]: 0.5000
</pre>
