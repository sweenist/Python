import bpy
from math import sqrt
FB_THICKNESS = 0.1875

def add_fret_board(fret_count, scale_length, min_width, max_width, curve_radius = None, overhang = True):

    verts = []    
    faces = []
    frets = []

    #get y values of fret medians
    for i in range(fret_count + 1):
        frets.append(fret_spacer(scale_length, i))
        
    #Add bottom vertices at the last fret or overhang. Negligible but...
    if overhang:
        frets.append(fret_spacer(scale_length, fret_count + 1))

    #Add fretboard vertices
    if curve_radius:
        for fret_y in frets:        
            cur_width = get_fret_width(min_width, max_width,frets[-1],fret_y)
            print("current width:", cur_width)
            print("Current Fret:", fret_y)
            z1, z2, x1, x2 = fretboard_curve_face(curve_radius, cur_width)
            
            verts.append((-cur_width / 2.0, fret_y, 0.00))          #0
            verts.append((-cur_width / 2.0, fret_y, FB_THICKNESS))  #1
            verts.append((-x1, fret_y, z1))                         #2
            verts.append((-x2, fret_y, z2))                         #3
            verts.append(( x2, fret_y, z2))                         #4
            verts.append(( x1, fret_y, z1))                         #5
            verts.append(( cur_width / 2.0, fret_y, FB_THICKNESS))  #6
            verts.append(( cur_width / 2.0, fret_y, 0.00))          #7

        #build the end face on the fretboard
        z1, z2, x1, x2 = fretboard_curve_face(curve_radius, min_width)
        verts.append(( x1, frets[-1], 0.00))
        verts.append(( x2, frets[-1], 0.00)) 
        verts.append((-x2, frets[-1], 0.00)) 
        verts.append((-x1, frets[-1], 0.00)) 

    else:
        for item in frets:
            cur_width = get_fret_width(min_width, max_width,frets[-1],fret_y)
            verts.append((-cur_width / 2.0, fret_y, 0.00))
            verts.append((-cur_width / 2.0, fret_y, FB_THICKNESS))
            verts.append(( cur_width / 2.0, fret_y, FB_THICKNESS))
            verts.append(( cur_width / 2.0, fret_y, 0.00))            
        
    #append faces
    if curve_radius:
        frets.pop()
        for i in range(len(frets)):
            offset = i * 8
            for j in range(7):
                faces.append(( 1 + offset, 0 + offset, 8 + offset, 9 + offset))
                print ( 1 + offset, 0 + offset, 8 + offset, 9 + offset)
                offset += 1
            print ("set %d complete" % i)
        #fille bottom faces
        offset = len(frets) * 8
        faces.extend([(offset, 11 + offset, 2 + offset, 1 + offset),
                      (11 + offset, 10 + offset, 3 + offset, 2 + offset),
                      (10 + offset, 9 + offset, 4 + offset, 3 + offset),
                      (9 + offset, 8 + offset, 5 + offset, 4 + offset),
                      (8 + offset, 7 + offset, 6 + offset, 5 + offset)
                    ]
                )
        
    #flat fretboard
    else:
        faces.extend([
            ( 0, 2, 3, 1),
            ( 7, 5, 4, 6),
            ( 1, 3, 7, 5),
            ( 3, 7, 6, 2),
            ( 2, 6, 4, 0)
            ]
        )

    return verts, faces

def fret_spacer(scale_length, fret_number):
    return -(scale_length - (scale_length/(2**(fret_number / 12.0))))

def fretboard_curve_face(radius, width, z_offset=FB_THICKNESS):
    #determine the offset
    x0 = width / 2.0    #Outer Edge
    z0 = sqrt((radius**2) - (x0**2))
    offset = z0 - z_offset
    
    x1 = width * 0.30
    x2 = width * 0.10
        
    z1 = (sqrt((radius**2) - (x1**2))) - offset
    z2 = (sqrt((radius**2) - (x2**2))) - offset
    
    return z1, z2, x1, x2

def get_fret_width(min_width, max_width, max_length, current_length):
    #return the width of the fretboard at the specified fret
    variance = max_width - min_width
    current_width = min_width + (variance * (current_length/max_length))
    return current_width

#main for testing
fret_count = 22
scale_length= 24.75
nut_midth = 1.75
bottom_width = 2.25
curve_radius = 12

v, f = add_fret_board(fret_count, scale_length, nut_midth, bottom_width, curve_radius)

mesh = bpy.data.meshes.new("frettest")
mesh.from_pydata(v, [], f)
mesh.update()
obj = bpy.data.objects.new("Fretboard", mesh)

bpy.context.scene.objects.link(obj)

