#!/usr/env/python

#TODO: use the new replacement for PIL, 'Pillow'
#TODO: convert from 8-space indent to 4-space indent


'''Motion Model Simulation
Eric Cawi

Based on notes from a talk by Stephen Anderson.
Impedance tables possibly based on work by Ferguson, Doherty, & Doke.

'''
import numpy as np
#import arcpy as arc #need to convert rasters to np arrays
#from arcpy.sa import * #spatial analyst for the thing
import matplotlib.pyplot as plt                      
import matplotlib.image as img
from PIL import Image
from PIL import PngImagePlugin
from scipy.stats import rv_discrete
from scipy import misc

#base_dir = 'C:/Users/Eric Cawi/Documents/SAR/motion_model_test/'
base_dir = './'
NUM_SIMS = 100
IMAGE_SIZE = (501,501) # pixels

def tag_image(filename, p_out):#for saving and adding images
        im = Image.open(filename)
        meta = PngImagePlugin.PngInfo()
        meta.add_text("prob outside", str(p_out))
        im.save(filename,"png",pnginfo = meta)

def rectify(sweep_angle):
        '''Rectifies sweep_angle to lie within [0, 2*pi].'''
        if sweep_angle < 0:
                return sweep_angle +2*np.pi
        elif sweep_angle > 2*np.pi: 
                return sweep_angle -2*np.pi
        else:
                return sweep_angle
        
def attract(current_r, current_theta, current_cell, sweep, rast, rast_res,dr):
        '''Rate attractiveness for 10 directions based on current position.

        @param r, theta, cell: Current position info. cell = (y,x)
        @param sweep: ???
        @param rast: current input raster; attractiveness???
        @param rast_res: raster resolution, i.e. pixel width in meters (???)
        @param dr: radial distance (???)
        
        Need to use current theta to figure out which cells of slope to access

        TODO: why is sweep_cell and array instead of just sweep_x and sweep_y?

        @return vector of relative attractiveness, each scaled from 0..1, sum=1.0
        
        '''  
        attract_data= np.zeros(12)
        rel_attract = np.zeros(12)
        oldy,oldx = current_cell
        for i in range(12):
                sweep_angle = rectify(current_theta + sweep[i])
                #this should work for all quadrants with the right positive negative additions
                dx = dr*np.cos(sweep_angle)
                dy = dr*np.sin(sweep_angle) #x and y components of sweep angle
                sweep_y = np.floor(dy/rast_res)
                sweep_x = np.floor(dx/rast_res) #get the number of cells to move up/down to look
                attract_data[i] = rast[oldy + sweep_y][oldx + sweep_x]
        attract_sum = 1.*np.sum(attract_data)
        #to get relative attractiveness of slope take inverse of slope so that less change is bigger, than take each one over the sum over the whole thing
        rel_attract = attract_data/attract_sum
        return rel_attract #returns relative attractiveness scaled from 0 to 1
        
def avg_speed(current_cell_sl, new_theta,dr, walking_speeds, sl_res):
        '''Calculates average speed/distance.
        @param current_cell_sl: (y,x);  y is the rows,  is the columns 
        @param new_theta:
        @param dr: radial distance (meters)
        @param walking_speeds:
        @param: sl_res:
        
        For simplicity, take average of walking speed of current cell and new cell.
        This should work for small stepsizes.
        
        TODO: use the path integral along the radial.
        TODO: is it (x,y) or (y,x)?

        '''
        oldy,oldx = current_cell_sl
        dx = np.floor(dr*np.cos(new_theta)/sl_res)
        dy = np.floor(dr*np.sin(new_theta)/sl_res)
        newx, newy = oldx+dx, oldy+dy
        first_speed = walking_speeds[oldy][oldx]
        last_speed = walking_speeds[newy][newx]
        speed = (first_speed+last_speed)/2
        return speed
        
def main():

        #have land cover and slope, reclassify land cover for impedance
        #have elevation map, use arcpy to calculate slope for each cell might not need this
        #use raster to numpy array to get numpy arrays of each thing
        #use formula from tobler to calculate walking speed across each cell
        #arc.env.workspace = "C:\Users\Eric Cawi\Documents\SAR\Motion Model Test"
        
        sl = misc.imread(base_dir + "slope.tif")
        sl = np.add(sl,.1)#get rid of divide by 0 errors
        print 'shape(sl):', str(np.shape(sl))
        #have to resize image to make the arrays multiply correctly
        img = Image.open(base_dir + 'imp2.png')
        shp = np.shape(sl)
        shp = tuple(reversed(shp))#need to get in width x height instead of height x width for the resize
        img = img.resize(shp,Image.BILINEAR)
        img.save(base_dir + 'imp2.png')
        imp = misc.imread(base_dir + 'imp2.png')
        print 'imp:', imp
        impedance_weight = .5
        slope_weight = .5
        #before getting inverse of slope use array to make walking speed array
        # for simplicity right now using tobler's hiking function and multiplying with the impedance weight
        walking_speeds = 6*np.exp(-3.5*np.abs(np.add(np.tan(sl),.05)))*1000.0/60.0 # speed in kmph*1000 m/km *1hr/60min
        sl = np.divide(1,sl)
        imp_shape = imp.shape
        sl_shape = sl.shape
        imp.astype('float')
        
  
        #walking speed weighted with land cover here from doherty paper, which uses a classification as 25 = 25% slower than normal, 100 = 100% slower than normal walking speed
        vel_weight = np.divide(np.subtract(100.0,imp),100.0)
        walking_speeds = np.multiply(vel_weight, walking_speeds) #since 1 arcsecond is roughy 30 meters the dimensions will hopefully work out
        
        #lower impedance is higher here, will work for probabilities, have to convert to float to avoid divide by zero errors
        imp = np.divide(1.0,imp)
        		
        print 'imp:', imp
        print 'sl:', sl
        print 'vw:', vel_weight
        sl_res = 25000/sl_shape[0] #NED should be a square so this should work for both ways, should be integer division
        imp_res = 25000/imp_shape[0]#30 meter impedance resolution from the land cover dataset
        end_time = 240 #arbitrary 4 hours
        #establish initial conditions in polar coordinates, using polar coordinates because i think it's easier to deal with the angles
        #r is the radius from the last known point, theta is the angle from "west"/the positive x axis through the lkp
        r = np.zeros(NUM_SIMS)#simulates 1000 hikers starting at ipp
        theta = np.random.uniform(0,2*np.pi,NUM_SIMS) #another 1000x1 array of angles, uniformly distributing heading for simulation
        stay = .05
        rev = .05#arbitrary values right now, need to discuss
        sweep = [-45.0 , -35.0 , -25.0 , -15.0 , -5.0 , 5.0 , 15.0 , 25.0 , 35.0, 45.0 , 0.0 , 180.0] #0 represents staying put 180 is a change in heading
        for i in range(len(sweep)):
                sweep[i] = sweep[i]*np.pi/180.0 #convert sweep angles to radians
        dr = 120.0 #120 meters is four cells ahead in the land cover raster which gives 9 specific cells for the sweeping angles

        #for each lookahead, have ten angles between -45 and plus 45 degrees of the current heading
        #get average impedance around 100 meters ahead, average flatness, weight each one by half
        #then scale to 1 - (prob go back + prob stay put)  these guys are all free parameters I think

        current_cell_imp = [imp_shape[0]/2 - 1, imp_shape[1]/2 - 1] #-1 is to compensate for the indeces starting at 0, starting at middle of array should represent the ipp
        current_cell_sl = [sl_shape[0]/2 - 1, sl_shape[1]/2 - 1]
        
        for i in range(NUM_SIMS):
                t = 0.0
                current_r = r[i]
                current_theta = theta[i]
                while t < end_time:
                        #look in current direction, need to figure out how to do the sweep of slope
                        slope_sweep = attract(current_r, current_theta,current_cell_sl,sweep,sl, sl_res,dr)
                        impedance_sweep = attract(current_r,current_theta,current_cell_imp,sweep, imp, imp_res,dr)
                        #goal: have relative attractiveness of both slope and land cover by taking values
                        #for slope might have a function that takes the least average change in each direction
                        #then take reciprocal to make smaller numbers bigger and take each change/sum of total to get relative goodness
                        #land cover take average 1/impedance in each direction and get relative attractiveness
                        sl_w = np.multiply(slope_sweep,slope_weight)
                        imp_w = np.multiply(impedance_sweep, impedance_weight)
                        probabilities= np.add(sl_w, imp_w)

                        #create a random variable with each of the 12 choices assigned the appropopriate probability
                        dist = rv_discrete(values = (range(len(sweep)), probabilities))
                        ind = dist.rvs(size = 1)
                        dtheta = sweep[ind]
                        
                        #Note: cannot test floating point for equality!  Modified.  -crt
                        eps = 1e-4
                        if (-eps < dtheta < eps):
                                v = 0.0 #staying put, no change
                                dt = 10.0 #stay arbitrarily put for 10 minutes before making next decision
                                r_new = current_r
                                theta_new = current_theta + dtheta
                        elif (np.pi-eps < dtheta < np.pi + eps):#reversal case
                                v = avg_speed(current_cell_sl, dtheta,dr,walking_speeds, sl_res)
                                dt = 120.0/v
                                r_new = current_r-120
                                theta_new = -1*current_theta
                        else:
                                #update the current hiker's new radius                          
                                if -eps < r[i] < eps:
                                        r_new = 120.0
                                        theta_new = current_theta + dtheta 
                                else:
                                        r_new = np.sqrt(current_r**2 + 120.0**2 -2.0*current_r*120.0*np.cos(np.pi-dtheta))#law of cosines to find new r
                                #law of sines to find new theta relative to origin, walking speeds treats each original cell as origin to calculate walking velocity
                                asin = np.arcsin(120/r_new * np.sin(np.pi-dtheta))
                                theta_new = current_theta+asin
                                v = avg_speed(current_cell_sl,dtheta,dr,walking_speeds,sl_res)#some way to figure out either average speed or distance traveled along the line chosen
                                dt = 120.0/v
                        #update for current time step
                      
                        current_r= r_new
                        current_theta= theta_new
                        t=t+dt
                        #update current_cell for slope and impedance
                        x = current_r*np.cos(theta[i])
                        y = current_theta*np.sin(theta[i])
                        impx = np.floor(x/imp_res)
                        impy = np.floor(y/imp_res)
                        slx = np.floor(x/sl_res)
                        sly = np.floor(y/sl_res)
                        current_cell_imp = np.add(current_cell_imp , [impx,impy])
                        current_cell_sl = np.add(current_cell_sl, [slx,sly])
                        
                #update r and theta
                r[i] = current_r
                theta[i] = current_theta

        #now that we have final positions for 1000 hikers at endtime the goal is to display/plot
        #Note: streamlined to eliminated some loops etc. -crt
        Xs = r * np.cos(theta)/50.
        Ys = r * np.sin(theta)/50.
        coords = zip(Ys,Xs)

        #Count the outsiders using vector logic: "OR" these arrays together
        outsiders = (Xs < 0) | (Xs > 500) | (Ys < 0) | (Ys > 500)
        num_outside = sum(outsiders)
        prob_outside = 1. * num_outside / NUM_SIMS

        # Create nominal grid of N 50m cells. Will get resized later.
        # Avoid zeros by putting 10/NUM_SIMS observations in each cell.
        # TODO: let prior be the distance model, with weight of ~1/100 motion model.
        counts = 10. * np.ones((500,500)) / NUM_SIMS
        for y,x in coords:
                counts[250+y][250+x] += 1
        probs = 1.*counts/NUM_SIMS #adding 1, dividing by total number of counts to get probability, these numbers should have both positive and negative values
        print 'Probs\n', probs
        print '\nP_inside :', sum(probs)
        print '\nP_outside:', prob_outside
        case_name = 'test'
        #example plotting for testing:
        plt.title("Motion Model Test")
        plt.imshow(probs,cmap = 'gist_gray')
        plt.colorbar()
        name = '%s/motion_model_test/%s.png' % (base_dir, case_name)
        plt.imsave(name, probs, cmap = 'gist_gray')
        tag_image(name, prob_outside)
        #now want to resize the image to be 5001 x5001 as required by mapscore
        img = Image.open(name)
        img = img.resize(IMAGE_SIZE, Image.BILINEAR)
        img.save(name)
main()
