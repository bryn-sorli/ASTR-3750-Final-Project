import numpy as np
#from numpy.random import choice
import matplotlib.pyplot as plt
import sys
import matplotlib.cm as cm
import time
#import powerlaw
import matplotlib as mpl
np.set_printoptions(threshold=sys.maxsize)


def weighted_choice(objects, weights):
    #Funciton obtained through scikit forum as a variant of a python package for random selection
    #Works by normalizing the probabilites and outputing a random value from the given array
    """ returns randomly an element from the sequence of 'objects',
        the likelihood of the objects is weighted according
        to the sequence of 'weights', i.e. percentages."""

    weights = np.array(weights, dtype=np.float64)
    sum_of_weights = weights.sum()
    # standardization:
    np.multiply(weights, 1 / sum_of_weights, weights)
    weights = weights.cumsum()
    x = np.random.random()
    for i in range(len(weights)):
        if x < weights[i]:
            return objects[i]



print("Bryn Sorli's ASTR 3750 Final Project")
print("Impact simulator")
print("Please follow prompts below to run programs with desired inputs")
time.sleep(1)

# Base Variables used throughout the simulation
x = np.arange(0, 500)
y = np.arange(0, 500)
# Main array storing craters
arr = np.zeros((y.size, x.size))

# Lists and Dictionary to assist with saving values at saturation and the 25 - 75 percent saturations
arr25 = np.zeros((y.size, x.size))
arr50 = np.zeros((y.size, x.size))
arr75 = np.zeros((y.size, x.size))
points_dict = {}
test_sat = np.zeros((y.size, x.size))
notSat = True
impact_count = 50.
sat_count = 0

total = []
c10 = 0
c20 = 0
c30 = 0
c50 = 0

print("###Simulation Menu###")
print("Choose 0 to run until saturation")
print("Choose 1 to run for a desired amount of years")
print("Choose 2 to run simulation with varying crater sizes until saturation")
print("Choose 3 to run simulation with varying crater sizes and new assumption for saturation")
choice = input("###+++++++++++++++###\n")

if choice == '1' or choice == '0' or  choice == '2' or choice == '3':
    print("Would you like a plot of the number of craters vs time?")
    print("Note: This portion of the simulation takes much longer, average run time of around a minute")
    time_plot = input("Choose y for yes or n for no: \n")

#All the below choices are specified in the menu, choice takes user input as a string and enters correct statement
#Error occurs if any other value is entered
if choice == '1' or choice == "1":
    years = input("Enter years to run(In thousands of years): ")
    print("###Running Simulation###")
    for i in range(int(years)):
        print("%", end=' ')
        x_val = np.random.randint(0,500,1)
        y_val = np.random.randint(0,500,1)
        r = 10
        mask = (x[np.newaxis,:]-x_val)**2 + (y[:,np.newaxis]-y_val)**2 < r**2
        arr[mask] = impact_count
        impact_count += 3
        
    print('\nSimulation Finished')


elif choice == "0":
    temp_count = 0
    test_year_count = []
    while(notSat):
        #Randomly Gnerates x,y value for center of crater
        x_val = np.random.randint(0,500,1)
        y_val = np.random.randint(0,500,1)
        r = 10
        r=r/2
        points_dict[impact_count] = (x_val[0], y_val[0],r)
        if test_sat[x_val, y_val] == 1:
            temp_count+= 1
            if temp_count == 10:
                #print(x_val, "###", y_val)
                print("Time to saturation in thousands of years: ", sat_count)
                notSat = False
        #Create boolean mask which holds the circular crater
        mask = (x[np.newaxis,:]-x_val)**2 + (y[:,np.newaxis]-y_val)**2 < r**2
        #Assign unique value to arr where mask is true
        #This will not only allow for old craters to be erased but gives each crater a unique value
        arr[mask] = impact_count
        impact_count += 1
        test_sat[x_val, y_val] = 1
        sat_count += 1
        test_year_count.append(sat_count)
        
        
elif choice == "2":
    temp_count = 0
    test_year_count = []
    temp = 0
    while(notSat):
        #Randomly Gnerates x,y value for center of crater
        x_val = np.random.randint(0,500,1)
        y_val = np.random.randint(0,500,1)
        r_list = [10, 20, 30, 50]
        #r_prob = [.9, .1, .05, .0009]
        r_prob = [.9, .2, .1, .03]
        #use weighted choice funciton to find radius of new crater
        r = weighted_choice(r_list, r_prob)
        r=r/2
        #Store values of each crater
        #Allows 25, 50 and 75 to be determined after saturation occurs
        points_dict[impact_count] = (x_val[0], y_val[0], r)
        if r == 5:
            c10+=1
            
        elif r == 10:
            c20+=1
            
        elif r == 15:
            c30+=1
            
        else:
            c50+=1
        if test_sat[x_val, y_val] == 1:
            temp_count+= 1
            if temp_count == 10:
                print("Time to saturation in thousands of years: ", sat_count)
                notSat = False
        mask = (x[np.newaxis,:]-x_val)**2 + (y[:,np.newaxis]-y_val)**2 < r**2
        arr[mask] = impact_count
        impact_count += 1
        test_sat[x_val, y_val] = 1
        sat_count += 1
        done = False
        if time_plot == "y":
            for i in range(500):
                for j in range(500):
                    if test_sat[i][j] == 1 and mask[i][j]== True:
                        temp -=1
                        done = True
                        break
                if done:
                    break
            temp+=1
            test_year_count.append(temp)
        
        
elif choice == "3":
    temp_count = 0
    hold_sat= np.zeros((y.size, x.size))
    test_year_count=[]
    temp = 0
    while(notSat):
        x_val = np.random.randint(0,500,1)
        y_val = np.random.randint(0,500,1)
        r_list = [10, 20, 30, 50]
        
        r_prob = [.9, .1, .05, .0009]
        r = weighted_choice(r_list, r_prob)
        r=r/2
        points_dict[impact_count] = (x_val[0], y_val[0], r)
        if r == 5:
            c10+=1
            
        elif r == 10:
            c20+=1
            
        elif r == 15:
            c30+=1
            
        else:
            c50+=1
        if any(7 in x for x in hold_sat):
            notSat = False
            print("Time to saturation in thousands of years: ", sat_count)
        
        mask = (x[np.newaxis,:]-x_val)**2 + (y[:,np.newaxis]-y_val)**2 < r**2
        hold_sat[mask] += 1
        arr[mask] = impact_count
        impact_count += 1
        test_sat[x_val, y_val] = 1
        sat_count += 1
        done = False
        if time_plot == "y":
            for i in range(500):
                for j in range(500):
                    if test_sat[i][j] == 1 and mask[i][j]== True:
                        temp -=1
                        done = True
                        break
            temp+=1
            test_year_count.append(temp)
else:
    print("Non Valid entry, have a good day")
    sys.exit("Bad Entry")
    
lent = len(points_dict)
per_25 = lent*.25
per_50 = lent*.5
per_75 = lent*.75


count25, count50, count75 = 50,50,50
#print(c10, c20, c30, c50)
for k in points_dict:
    if k <= per_25:
        mask = (x[np.newaxis,:]-points_dict[k][0])**2 + (y[:,np.newaxis]-points_dict[k][1])**2 < points_dict[k][2]**2
        arr25[mask] = count25
        count25+=1
    if k <= per_50:
        mask = (x[np.newaxis,:]-points_dict[k][0])**2 + (y[:,np.newaxis]-points_dict[k][1])**2 < points_dict[k][2]**2
        arr50[mask] = count50
        count50+=1
        
    if k <= per_75:
        mask = (x[np.newaxis,:]-points_dict[k][0])**2 + (y[:,np.newaxis]-points_dict[k][1])**2 < points_dict[k][2]**2
        arr75[mask] = count75
        count75 += 1

pl = input("Would you like a plot(Y/N): ")
if pl == "Y" or pl == "y" or pl == "1":
    fig, axs = plt.subplots(2, 2)
    axs[1, 1].pcolormesh(x, y, arr, cmap= cm.gray)
    axs[1, 1].set_title('100%')
    axs[0, 0].pcolormesh(x, y, arr25, cmap= cm.gray)
    axs[0, 0].set_title('25%')
    axs[0, 1].pcolormesh(x, y, arr50, cmap= cm.gray)
    axs[0, 1].set_title('50%')
    axs[1, 0].pcolormesh(x, y, arr75, cmap= cm.gray)
    axs[1, 0].set_title('75%')

    for ax in axs.flat:
        ax.set(xlabel='Side Length(km)', ylabel='Side Length(km)')
        
    fig.suptitle('"Pictures" at 25%, 50%, 75%, and 100%')
    for ax in axs.flat:
        ax.label_outer()
    
    #impact_time = []
    time_elapsed = []
    for i in range(sat_count):
        time_elapsed.append(i)
        
    if time_plot == "y":
        time_run = sat_count*1000
        plt.figure(2)
        plt.title("Number of craters vs time")
        plt.xlabel("Time Elapsed(thousands of years)")
        plt.ylabel("Number of Craters")
        plt.text(time_elapsed[sat_count-1], test_year_count[sat_count-1], "Point of saturation after "+ str(time_run)+" years", horizontalalignment='right')
        #print(test_year_count)
        plt.plot(time_elapsed, test_year_count)
        plt.plot(time_elapsed[sat_count-1], test_year_count[sat_count-1], 'r*' )
    plt.show()
