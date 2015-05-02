import numpy as np
import json

from bokeh.plotting import figure, output_file, show, VBox, ColumnDataSource
from bokeh.models import HoverTool
from collections import OrderedDict

#Tools to be used in plotting the figure
TOOLS="wheel_zoom,box_zoom,hover"

#Import json file
with open("crime.json") as json_file:
    data = json.load(json_file)

#pull out the data relevant to us
data = { d["name"]: d["crime"] for d in data["data"] if d["crime"]["Total"] > 0}

#Sort the data into decreasing order of Total no. of crimes
States = sorted(data.keys(), key=lambda x: data[x]["Total"], reverse=True)

#Create a numpy array for different crimes
revenge_scores = np.array([data[name]["Revenge /Settling scores"] for name in States], dtype=np.float)
greed = np.array([data[name]["Greed/ Money"] for name in States], dtype=np.float)
extortion = np.array([data[name]["Extortion"] for name in States], dtype=np.float)
disrepute = np.array([data[name]["Cause Disrepute"] for name in States], dtype=np.float)
prank = np.array([data[name]["Prank/Satisfaction of Gaining Control "] for name in States], dtype=np.float)
fraud = np.array([data[name]["Fraud/Illegal Gain"] for name in States], dtype=np.float)
eveteasing = np.array([data[name]["Eve teasing/Harassment"] for name in States], dtype=np.float)
others = np.array([data[name]["Others"] for name in States], dtype=np.float)

# Output static HTML File
output_file('CrimeTest.html')


#There are a lot of things to for each element we might want a hover tool to
#be able to display, so put them all in a ColumnDataSource
source1 = ColumnDataSource(data = dict(re = revenge_scores)) 
source2 = ColumnDataSource(data = dict(gr = greed))
source3 = ColumnDataSource(data= dict(ex = extortion))
source4 = ColumnDataSource(data = dict(di = disrepute))
source5 = ColumnDataSource(data = dict(pr = prank))
source6 = ColumnDataSource(data = dict(fr = fraud))
source7 = ColumnDataSource(data = dict(ev = eveteasing))
source8 = ColumnDataSource(data = dict(ot = others))



# create a figure()
p1 = figure(title="Cyber Crime Statistics-2013", tools=TOOLS,
            x_range=States, y_range=[0, max([revenge_scores.max(), greed.max(), extortion.max(), disrepute.max(), prank.max(), fraud.max(), eveteasing.max(), others.max()])],
            background_fill='white', plot_width=1375, plot_height=700,x_axis_label="States/U.T.", y_axis_label="No. of Crimes"
    )

# Catagorical percentage coordinates can be used for positioning/grouping
States_revenge_scores = [c+":.2" for c in States]
States_greed = [c+":.3" for c in States]
States_extortion = [c+":.4" for c in States]
States_disrepute = [c+":.5" for c in States]
States_prank = [c+":.6" for c in States]
States_fraud = [c+":.7" for c in States]
States_eveteasing = [c+":.8" for c in States]
States_others = [c+":.9" for c in States]

#Make individual bars of each crime for each state
#Take the source from the above ColumnDataSource for each of them
p1.rect(x=States_revenge_scores, y=revenge_scores/2, width=0.1, source=source1, legend="Revenge/Settling Scores", height=revenge_scores, color="#CD7F32", alpha=0.6)
p1.rect(x=States_greed, y=greed/2, width=0.1, height=greed, source=source2, legend="Greed/Money", color="silver", alpha=0.6)
p1.rect(x=States_extortion, y=extortion/2, width=0.1, source=source3, legend="Extortion", height=extortion, color="blue", alpha=0.6)
p1.rect(x=States_disrepute, y=disrepute/2, width=0.1, source=source4, legend="Cause Disrepute", height=disrepute, color="red", alpha=0.6)
p1.rect(x=States_prank, y=prank/2, width=0.1, source=source5, legend="Prank/Satisfaction of Gaining Control", height=prank, color="gold", alpha=0.6)
p1.rect(x=States_fraud, y=fraud/2, width=0.1, source=source6, legend="Fraud/Illegal Gain", height=fraud, color="#FFFF00", alpha=0.6)
p1.rect(x=States_eveteasing, y=eveteasing/2, width=0.1, source=source7, legend="Eveteasing/Harrasment", height=eveteasing, color="#008000", alpha=0.6)
p1.rect(x=States_others, y=others/2, width=0.1, source=source8, legend="Others", height=others, color="#A52A2A", alpha=0.6)


#Set up a hovertool to display properties of each bar
hover = p1.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([("revenge", '@re'), 
		("greed", '@gr'), 
		('extortion', '@ex'), 
		('disrepute', '@di'), 
		('prank', '@pr'), 
		('fraud', '@fr'), 
		('eveteasing', '@ev'), 
		('others', '@ot')]
		)

#use grid and axis methods to style the plot
p1.xgrid.grid_line_color = None
p1.axis.major_label_text_font_size = "8pt"
p1.axis.major_label_standoff = 0
p1.xaxis.major_label_orientation = np.pi/3
p1.xaxis.major_label_standoff = 6
p1.xaxis.major_tick_out = 0


# Create a second plot in which for individual states, all the crime data are stacked on each other.

p2 = figure(title="Cyber Crime Statistics-2013(Stacked)", tools=TOOLS, 
	x_range=States, y_range=[0,400],
	background_fill='white', plot_width=800, x_axis_label="States/U.T.", y_axis_label="No. of Crimes")

p2.rect(x=States, y=revenge_scores/2, width=0.8, height=revenge_scores, legend="Revenge/Settling Scores", color="#CD7F32", alpha=0.6)
p2.rect(x=States, y=greed/2, width=0.8, height=greed, legend="Greed/Money", color="silver", alpha=0.6)
p2.rect(x=States, y=extortion/2, width=0.8, height=extortion, legend='Extortion', color="gold", alpha=0.6)
p2.rect(x=States, y=disrepute/2, width=0.8, height=disrepute, legend='Cause Disrepute', color='blue', alpha=0.6)
p2.rect(x=States, y=prank/2, width=0.8, height=prank, legend='Prank/Satisfaction of Gaining Control', color='#A52A2A', alpha=0.6)
p2.rect(x=States, y=fraud/2, width=0.8, height=fraud, legend='Fraud/Illegal Gain', color='red', alpha=0.6)
p2.rect(x=States, y=eveteasing/2, width=0.8, height=eveteasing, legend='Eveteasing/Harrasment', color='#FFFF00', alpha=0.6)
p2.rect(x=States, y=others/2, width=0.8, height=others, legend='Others', color="#008000", alpha=0.6)

p2.xgrid.grid_line_color = None
p2.axis.major_label_text_font_size = "8pt"
p2.axis.major_label_standoff = 0
p2.xaxis.major_label_orientation = np.pi/2
p2.xaxis.major_label_standoff = 6
p2.xaxis.major_tick_out = 0

show(VBox(p1,p2))
