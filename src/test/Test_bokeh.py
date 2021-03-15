#%%
from bokeh.plotting import figure, output_file, show, output_notebook

# prepare some data
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

# output to static HTML file
output_file("lines.html")
#output_notebook()

# create a new plot with a title and axis labels
p = figure(title="simple line example", x_axis_label='x', y_axis_label='y',plot_width=1200, plot_height=600)

# add a line renderer with legend and line thickness
p.line(x, y, legend_label="Temp.", line_width=2)

# remove the axis
p.xaxis.visible = False
p.yaxis.visible = False

# show the results
show(p)




# %%
from bokeh.plotting import figure, output_file, show

p = figure(title="My first interactive plot!")
x_coords = [0,1,2,3,4]
y_coords = [5,4,1,2,0]
p.circle(x=x_coords, y=y_coords, size=10, color="red")
show(p)



# %%
from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON, get_provider

output_file("tile.html")

tile_provider = get_provider(CARTODBPOSITRON)

# range bounds supplied in web mercator coordinates
p = figure(x_range=(12000000, 13000000), y_range=(2200000, 2800000),
           x_axis_type="mercator", y_axis_type="mercator")
p.add_tile(tile_provider)

show(p)

# %%
