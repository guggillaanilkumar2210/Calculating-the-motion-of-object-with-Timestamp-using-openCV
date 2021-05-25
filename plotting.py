from motion import df
from bokeh.plotting import figure, show, output_file, Figure
from bokeh.models import HoverTool, ColumnDataSource
#Converting time to string format
df["Start_string"]= df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")
cds = ColumnDataSource(df)
#The dataframe of time values is plotted on the browser using Bokeh plots.
p=figure(x_axis_type = 'datetime',height=100,width=500,title="Motion Graph")
p.yaxis.minor_tick_line_color = None
p.ygrid[0].ticker.desired_num_ticks = 1
hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])
p.add_tools(hover)
q=p.quad(left="Start",right="End",bottom=0,top=1,color="red",source=cds)
output_file("Graph.html")
show(p)