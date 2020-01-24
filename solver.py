#sudoku solver        worst case senario it takes 6.2350029e+60 (6 Novemdecillion) years
#python solver.py 4 0:2 1:1 5:3 6:2 11:4 12:1
#http://www.sudoku-download.net/sudoku_4x4.php
import sys;
import math;
userIsStupid = False; #input error handling
#input prefilled cells in standard format position:value
print("input: ");
print(sys.argv);

if (math.sqrt(int(sys.argv[1])))%1 != 0:
    userIsStupid = True;
    print("input size is not a square number");

#sudoku grid size i.e. 4x4 9x9 16x16 etc.
size = int(sys.argv[1]);
size_sum = int(((size**2)+size)/2);

#############################################################################
#create master array length=size^2 with each item being its own array 0-size
#array reads left to right top to bottom 
#this array shows possible values for each cell and values should only be removed if absolutely sure
master_array=[];
solution_array=[];
for i in range(size**2): #81=number of cells in sudoku
    sub = [];
    for j in range(1,size+1): #populate with possible values 1-9
        sub.append(j);
    master_array.append(sub);
#print(master_array);

#############################################################################
#remove all but input value from appropriate cell in master array
for i in range(2,len(sys.argv)):
    pos = int(sys.argv[i].split(":")[0]);
    value = int(sys.argv[i].split(":")[1]);
    print(str(pos) +" : "+ str(value));
    master_array[pos] = list(filter(lambda x: x==value, master_array[pos]));

#print(master_array);

#############################################################################
#TODO:remove input value from other cells based on square
#similar to function above but calculates row column and square from input and remove value from those things
for i in range(2,len(sys.argv)):
    pos = int(sys.argv[i].split(":")[0]);
    value = int(sys.argv[i].split(":")[1]);
    row = math.floor(pos/size);
    col = pos%size;
    for j in range(0,size):
        if len(master_array[row*size+j]) > 1:
            try:
                master_array[row*size+j].remove(value);
            except:
                pass;
        if len(master_array[col+size*j]) > 1:
            try:
                master_array[col+size*j].remove(value);
            except:
                pass;

print(master_array);

#############################################################################
#array that temporarily hold possible solution to be checked
testarray = [];
for i in range(0,size**2):
    testarray.append(master_array[i][0]);
#print(testarray);

#############################################################################
#temp_solution = [2,1,4,3,4,3,2,1,3,2,1,4,1,4,3,2];
#TODO:checker function check columns and square
def checker(checkerarray): #input test array as local variable?
    isvalid = True;
    #if checkerarray == temp_solution:
        #solution_array.extend(checkerarray);

    for i in range(0,size):
        if sum(checkerarray[i*size:i*size+size]) != size_sum: #check if rows are valid
            isvalid = False;
            #print("solution failed");
            break;
        #else:
            #print("row solution succeeded!");
        colsum = 0;
        for j in range(0,size):
          colsum += testarray[i+j*size];
        if colsum != size_sum:
            isvalid = False;
            break;
    #TODO:check squares
    return isvalid;

################################################################################
#recursive function that goes through evey possible combination of solutions
def func(tier):
    if tier >=size**2:
        #print(testarray); #test function will go here
        if checker(testarray) == True:
            print("potential solution:");
            print(testarray);
        return;
    else:
        for i in range(0,len(master_array[tier])):
            #print(tier);
            testarray[tier] = master_array[tier][i];
        
            passthru =  tier+1;
            func(passthru);
            
if userIsStupid == False:
    func(0);
#print("solution:");
#print(solution_array);
print("end");
