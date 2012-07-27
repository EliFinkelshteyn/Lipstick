# Lipstick (LilBro Graphing Framework)

##IMPORTANT NOTE:

This is currently a work in progress in terms of open sourcing. I built this originally at an awesome company I used to work for called Shutterstock, who let me open source it. I'm working on doing that right now, but until I finish, this will not work for you out of the box. I'd recommend waiting for me to push a few more commits before trying to use this.

## Why the name?

1. Lipstick makes things pretty, if you use it right.
2. You can put Lipstick on Apache Pig, but it's still Apache Pig.

## Installation

To install Lipstick, you'll first need to have Hadoop and Pig properly installed. There are instructions for this all over the internet. Once this is finished:

1. Simply git clone the project 
2. Add *path/to/Lipstick/resources/jython-standalone-2.5.2.jar* to your PIG_CLASSPATH. Go ahead and do this in your .bashrc so you never need to worry about it again. That's it. 
3. If you want to be able to use scripts referencing the framework from anywhere, just add the framework's src folder to your JYTHONPATH environment variable.

That's it. You're ready to go. Go ahead and try out one of the scripts in the scripts folder to make sure things work.

## Use Cases

There are two main use cases as of this writing. Both involve generating a two dimensional graph with an arbitrary number of lines:

1. Where the things you want graphed are defined before a pig script is run. For example: graph the numbers of searches, downloads, and the average temperature in Siberia on one graph. You know you always wants to graph just these three things.

2. Where the things you want graphed are defined *dynamically during the run of the pig script itself*. For example: I want to graph how often each browser is used every day, but I don't know exactly which browsers were used at all before the script is run.

##Use

To generate a graph, simply run **pig name_of_generating_script.py**. That would have generated a graph on Shutterstock's graphing site. Since I no longer have access to that, I'll built my own, and allow graphs to be generated through matplotlib. Stay tuned.

##Brief Howto

To properly use the framework, you'll need to design a short Python (really, Jython) script that will pass some pig code along with some parameters to the framework. There are lots of examples of this in the bin folder, and **the best way of learning is probably just using one of these as a template. They're very self-explanatory.**

That said, the specific parameters you'll need to pass will look like:

<code>
params = {'script':pig, 
          'date_range':date_range, 
          'output_name': output_name,
          'columns': columns}
</code>

<code>pig_runner = PigRunner.PigRunner(params)</code>

1. **'script'**: A string. Just the variable that holds your bit of pig code.

2. **'date_range'**: A list of two python datetime objects. these provide the timeframe you'd like to graph for. These are inclusive on both sides.

3. **'output_name'**: A string. This will be the output_name  used on HDFS and the name used in Grapht for your graph.

4. **'columns'**: a list of whatever names you used for the columns you want graphed. All but the last of these will provide y values for individual lines. The last will provide the x values used for all lines. 

5. **'rotation'** (optional): A string: 'rotated' or 'normal'. If you're graphing dynamic columns determined by your script, this can be useful. Its use is explained in the conventions section of this readme.


### Conventions
In addition to this, some conventions are expected of you in your Pig script portion. 

1. You need not load LilBro data manually. This is done for you. You can just assume that it's been loaded for a single day of your date range into a set called *loaded_set*. The framework will extrapolate out from your code to get data for all days in your date range.

2. The final set that provides the numbers you'd like graphed should simply be a single row of numbers where the first n-1 of these provide y values for individual lines, and the last provides an x value for all lines for a single set of data points.

3. Call that last set **pre_final**.

4. If you're graphing time series data per day, just provide **'$date' AS date** as the last part of your **pre_final** data set, and **date** as the last column in your list of columns.

5. In the case that you want your data rotated so that the columns become the rows and the rows become the columns (this is common when you're graphing a dynamic set of columns determined by your script's results), you should provide the **'rotation': 'rotated'** parameter to **params**. In addition, and unlike the normal case, you should make sure your pig script returns any number of *rows*, but just three columns titled **colname**, **total**, and whatever your x value is (usually **date**).

##Issues and Helping Out

Notice any issues or missing information in this Readme? Notice anything you think could be done better in the framework? Feel free to come bug me (Eli Finkelshteyn), or contribute! 