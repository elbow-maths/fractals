import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

def line_length(x1,y1,x2,y2):
    width = x2-x1
    height = y2-y1
    return np.sqrt(width**2 + height**2)

def angle_to_horizonal(x1,y1,x2,y2):
    dot_product = 1*(x2-x1)
    magntiude_product = 1 * line_length(x1,y1,x2,y2)
    return np.arccos(dot_product/magntiude_product)

def scale_line(line_points,desired_length):
    x1,y1 = line_points[0]
    x2,y2 = line_points[-1]
    
    current_length = line_length(x1,y1,x2,y2)
    scaling_factor = desired_length/current_length
    
    return [tuple(i*scaling_factor for i in j) for j in line_points]

def rotate_line(flat_line_points,x1,y1,x2,y2):
    if y2-y1 < 0:
        angle = 2*np.pi - angle_to_horizonal(x1,y1,x2,y2)
    else:
        angle = angle_to_horizonal(x1,y1,x2,y2)
    new_points = []
    for x,y in flat_line_points:
        new_points.append((x*np.cos(angle)-y*np.sin(angle),x*np.sin(angle)+y*np.cos(angle)))
    
    return new_points
    
def translate_line(line_points,new_start):
    return [tuple(point[i]+new_start[i] for i in [0,1]) for point in line_points]


def koch_line(start,end,order):
    current_line = [start,end]
    koch_template = [(0,0),(1,0),(1.5,np.sqrt(3)/2),(2,0),(3,0)]
    
    for i in range(order):
        output=[]
        for j in range(len(current_line)-1):
            x1,y1 = current_line[j]
            x2,y2 = current_line[j+1]
            desired_length = line_length(x1,y1,x2,y2)
            new_line = scale_line(koch_template,desired_length)
            new_line = rotate_line(new_line,x1,y1,x2,y2)
            new_line = translate_line(new_line,current_line[j])
            output = output + new_line
        current_line = deepcopy(output)
    return current_line

def koch_snowflake(order=4):
    lines = [[(1,1),(2,1+np.sqrt(3))],[(2,1+np.sqrt(3)),(3,1)],[(3,1),(1,1)]]
    
    lines_flaked = [koch_line(i[0],i[1],order) for i in lines]
            
    
    plt.figure(figsize=(10,10))
    ax = plt.gca()
    ax.set_xlim([-0, 4])
    ax.set_ylim([-0.5, 3.5])
    for j in [0,1,2]:
        plt.plot([p[0] for p in lines_flaked[j]],[p[1] for p in lines_flaked[j]],linewidth=3,color="k")
    plt.axis("off")
    plt.show()
    plt.savefig("koch_snowflake_"+str(order)+".png",bbox_inches='tight')
    plt.close()