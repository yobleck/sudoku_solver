#sudoku solver        worst case senario it takes 6.2350029e+60 (6 Novemdecillion) years
#python solver.py 4 0:2 1:1 5:3 6:2 11:4 12:1
#easy https://www.websudoku.com/?level=1&set_id=1818407932  python solver.py 9 6:2 8:1 10:6 14:3 17:7 18:7 20:8 21:4 24:5 27:2 29:3 30:6 32:9 33:1 34:7 37:7 38:6 40:1 42:3 43:4 46:8 47:1 48:3 50:2 51:9 53:6 56:4 59:6 60:7 62:5 63:5 66:1 70:9 72:6 74:2
#medium https://www.websudoku.com/?level=2&set_id=2942337575 python solver.py 9 1:1 3:3 8:7 11:8 13:2 15:5 19:9 20:7 21:6 22:8 23:4 26:1 29:6 30:8 37:4 43:3 50:2 51:1 54:3 57:4 58:7 59:8 60:9 61:1 65:2 67:5 69:7 72:7 77:3 79:5
#evil https://www.websudoku.com/?level=4&set_id=2698854159  python solver.py 9 1:7 2:8 4:5 11:5 13:8 15:2 18:6 19:2 23:9 25:1 30:7 34:4 38:7 42:3 46:1 50:2 55:9 57:6 61:3 62:1 65:1 67:2 69:4 76:9 78:5 79:8
#http://www.sudoku-download.net/sudoku_4x4.php
#TODO: hidden singles aka values with 2 possibilities that can be quickly eliminated
#TODO: used naked pair to eliminate those 2 possibilities from the rest of the row/col/sqr
#TODO: add log to file
import sys;
import math;
userIsStupid = False; #input error handling
verbosePrinting = False;
#input prefilled cells in standard format position:value
if len(sys.argv) > 2:
    given_array = sys.argv[2:]; #TODO: check given array to make sure it is even valid (has no typos)
else:
    userIsStupid = True;
print("Input:", given_array); #TODO: fix bug where program crashes if no givens are provided

if (math.sqrt(int(sys.argv[1])))%1 != 0 or int(sys.argv[1]) < 1:
    userIsStupid = True;
    print("Input size is invalid. i.e. not square or less than one");
if int(sys.argv[1]) == 4 and len(sys.argv) < 6:
    print("Number of givens is below minimum value to guarentee one solution. Multiple solutions will be outputted.");
if int(sys.argv[1]) == 9 and len(sys.argv) < 19:
    print("Number of givens is below minimum value to guarentee one solution. Multiple solutions will be outputted.");
#add more for 16x16 etc...

#sudoku grid size i.e. 4x4 9x9 16x16 etc.
size = int(sys.argv[1]); sqrt_size = int(math.sqrt(size)); size_sqrd = size**2; size_sum = int(((size_sqrd)+size)/2);

#############################################################################
#create master array length=size^2 with each item being its own array length 0 to size
#array reads left to right top to bottom 
#this array shows possible values for each cell and values should only be removed if absolutely sure
master_array=[];
for i in range(size_sqrd): #81=number of cells in 9x9 sudoku
    sub = [];
    for j in range(1,size+1): #populate with possible values 1-9
        sub.append(j);
    master_array.append(sub);
if verbosePrinting == True:
    print("initial creation of master array:",master_array);

#############################################################################
#remove all but input value from appropriate cell in master array
def elim_all_but_given():
    for i in given_array:
        pos = int(i.split(":")[0]);
        value = int(i.split(":")[1]);
        if verbosePrinting == True:
            print(str(pos) +":"+ str(value)); #TODO: print in grid format maybe
        master_array[pos] = list(filter(lambda x: x==value, master_array[pos]));
#elim_all_but_given();
#############################################################################
#similar to function above but calculates row column and square from input and remove value from those things
def elim_given_from_other():
    for i in given_array:
        pos = int(i.split(":")[0]);
        value = int(i.split(":")[1]);
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
#elim_given_from_other();
#############################################################################
def naked_elim():
    for subset in range(2,3): #naked pairs/triples/quads TODO:range(2,5)
        for i in range(0,size): #copying checker function violate dry but the outputs are different enought that i dont want to jut make one function to handle every case like this atleast for now
            nak_row = [];
            nak_row.append(master_array[i*size : i*size+size]);
            #print(nak_row);
            for j in range(0,size):
                #print(nak_row[0][j]);
                if len(nak_row[0][j]) == subset:
                    #print("almost");
                    if nak_row[0].count(nak_row[0][j]) > 1:
                        print("succ");
                        
                
#naked_elim();
#############################################################################
def initial_clearing(): #this function recursively calls the elim functions until the value of given_array stops changing
    #print("given");
    global given_array;
    #print(given_array);
    elim_all_but_given();
    elim_given_from_other();
    temp_given_array = [];
    for x in range(0,size_sqrd):
        if len(master_array[x]) == 1:
           temp_given_array.append(str(x)+":"+str(master_array[x][0]));
    if verbosePrinting == True:
        print("temp:", temp_given_array);
    if temp_given_array == given_array:
        return;
    else:
        given_array = temp_given_array;
        initial_clearing();

#############################################################################
def worst_case_senario ():
    wcs = 1; #calculates worst case senario number of iterations/combination the programs will have to search for a potential solution
    amount = 0; unit = 0; unit_array = ["year(s)","day(s)","hour(s)","minute(s)","second(s)","millisecond(s)"];
    for x in range(0,len(master_array)):
        wcs *= len(master_array[x]);
    print("worst case senario number of possibilities to check:", wcs);
                    #year                       day                hour              min         sec      ms
    time_array = [wcs/500000/60/60/24/356,wcs/500000/60/60/24,wcs/500000/60/60,wcs/500000/60,wcs/500000,wcs/500]; #500000 is based on single thread ryzen 3700x
    for t in range(0,len(time_array)):
        if time_array[t] > 1:
           amount = time_array[t];
           unit = t;
           break;
    print("estimated time to completion:", amount, unit_array[unit]);

#############################################################################
#array that temporarily hold possible solution to be checked
testarray = [];
for i in range(0,size_sqrd):
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
        if sum(checkerarray[i*size:i*size+size]) != size_sum or len(set(checkerarray[i*size:i*size+size])) != size: #check if row has valid sum and no dups
            isvalid = False;
            break;

        col_list = [];
        for j in range(0,size):
          col_list.append(testarray[i+j*size]);
        if sum(col_list) != size_sum or len(set(col_list)) != size: #check if column has valid sum and no dups
            isvalid = False;
            break;
        
        #this code is just modified from elim_given_from_other, which violates DRY
        sqr_list = [];
        row = i//sqrt_size;
        col = i%sqrt_size;
        thing = int(col*sqrt_size + row*math.pow(sqrt_size,3));
        for k in range(0,sqrt_size):
            for m in range(0,sqrt_size):
                sqr_list.append(checkerarray[(k*size+m)+thing]);
        if sum(sqr_list) != size_sum or len(set(sqr_list)) != size: #check if square has valid sum and no dups
            isvalid = False;
            break;

    return isvalid;

#############################################################################
#recursive function that goes through evey possible combination of solutions
solution_counter = 0;
def brute_force(tier):
    if tier >= size_sqrd:
        if checker(testarray) == True:
            print("potential solution:");
            for x in range(0,size):
                for y in range(0,size):
                    print(testarray[x*size + y], end=" ");
                print("");
            global solution_counter;
            solution_counter+=1;
        return;
    else:
        for i in range(0,len(master_array[tier])):
            #print(tier);
            testarray[tier] = master_array[tier][i];
        
            passthru = tier+1;
            brute_force(passthru);
            
if userIsStupid == False:
    initial_clearing();
    #naked_elim();
    print("possibilities:");
    for x in range(0,size):
        print(master_array[x*size:x*size+size]);
    #print(master_array);
    worst_case_senario();
    brute_force(0);
    print("");
    print(solution_counter, "solution(s) found");
print("end");
