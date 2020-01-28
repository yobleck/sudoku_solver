#sudoku solver        worst case senario it takes 6.2350029e+60 (6 Novemdecillion) years
#python solver.py 4 0:2 1:1 5:3 6:2 11:4 12:1
#https://www.websudoku.com/?level=1&set_id=1818407932  python solver.py 9 6:2 8:1 10:6 14:3 17:7 18:7 20:8 21:4 24:5 27:2 29:3 30:6 32:9 33:1 34:7 37:7 38:6 40:1 42:3 43:4 46:8 47:1 48:3 50:2 51:9 53:6 56:4 59:6 60:7 62:5 63:5 66:1 70:9 72:6 74:2
#http://www.sudoku-download.net/sudoku_4x4.php
import sys;
import math;
userIsStupid = False; #input error handling
#input prefilled cells in standard format position:value
print("input: ");
print(sys.argv);

if (math.sqrt(int(sys.argv[1])))%1 != 0 or int(sys.argv[1]) < 1:
    userIsStupid = True;
    print("input size is invalid. i.e. not square or less than one");

#sudoku grid size i.e. 4x4 9x9 16x16 etc.
size = int(sys.argv[1]);
sqrt_size = int(math.sqrt(size));
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
#similar to function above but calculates row column and square from input and remove value from those things
for i in range(2,len(sys.argv)):
    pos = int(sys.argv[i].split(":")[0]);
    value = int(sys.argv[i].split(":")[1]);
    row = pos//size;
    col = pos%size;
    for j in range(0,size):
        if len(master_array[row*size+j]) > 1:
            try:
                master_array[row*size+j].remove(value); #removes value from row
            except:
                pass;
        if len(master_array[col+size*j]) > 1:
            try:
                master_array[col+size*j].remove(value); #removes value from column
            except:
                pass;
    
    sqr_row = row//sqrt_size;
    sqr_col = col//sqrt_size;
    sqr_thing = int(sqr_col*sqrt_size + sqr_row*math.pow(sqrt_size,3));
    for k in range(0,sqrt_size):
        for m in range(0,sqrt_size):
            if len(master_array[(k*size+m)+sqr_thing]) > 1:
                try:
                    master_array[(k*size+m)+sqr_thing].remove(value); #removes value from square
                except:
                    pass;

print(master_array);

############################################################################
wcs = 1; #calculates worst case senario number of iterations/combination the programs will have to search for a potential solution
for x in range(0,len(master_array)):
   wcs *= len(master_array[x]);
print("worst case senario:");
print(wcs);

#############################################################################
#array that temporarily hold possible solution to be checked
testarray = [];
for i in range(0,size**2):
    testarray.append(master_array[i][0]);
#print(testarray);

#############################################################################
temp_solution = [3,2,4,1,1,4,3,2,2,3,1,4,4,1,2,3];
#TODO:check for duplicates
def checker(checkerarray): #function to check if col row and square are valid
    isvalid = True;
    if checkerarray == temp_solution:
        print("solution here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");

    for i in range(0,size):
        if sum(checkerarray[i*size:i*size+size]) != size_sum or len(checkerarray[i*size:i*size+size]) != len(set(checkerarray[i*size:i*size+size])): #check if row has valid sum and no dups
            isvalid = False;
            break;

        col_list = [];
        for j in range(0,size):
          col_list.append(testarray[i+j*size]);
        if sum(col_list) != size_sum or len(col_list) != len(set(col_list)): #check if column has valid sum and no dups
            isvalid = False;
            break;
        
        #this code is just modified from above, which violates DRY
        sqr_list = [];
        row = i//sqrt_size;
        col = i%sqrt_size;
        thing = int(col*sqrt_size + row*math.pow(sqrt_size,3));
        for k in range(0,sqrt_size):
            for m in range(0,sqrt_size):
                sqr_list.append(checkerarray[(k*size+m)+thing]);
        if sum(sqr_list) != size_sum or len(sqr_list) != len(set(sqr_list)): #check if square has valid sum
            isvalid = False;
            break;

    return isvalid;

################################################################################
#recursive function that goes through evey possible combination of solutions
def func(tier):
    if tier >= size**2:
        #print(testarray); #test function will go here
        if checker(testarray) == True:
            print("potential solution:");
            for x in range(0,size):
                for y in range(0,size):
                    print(testarray[x*size + y], end=" ");
                print("");
        return;
    else:
        for i in range(0,len(master_array[tier])):
            #print(tier);
            testarray[tier] = master_array[tier][i];
        
            passthru = tier+1;
            func(passthru);
            
if userIsStupid == False:
    func(0);
print("end");
