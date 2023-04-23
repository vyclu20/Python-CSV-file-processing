def main(csvfile, SubjIDs):
    #Type checking for validity
    try:
        if type(csvfile) != str or type (SubjIDs) != list or len(SubjIDs) != 2:
            print("The input data is invalid")
            return None
        file = open(csvfile)
        #Splitting list into two inputs
        subj1, subj2 = SubjIDs[0].upper(), SubjIDs[1].upper()
        OP1 = [face_symm(csvfile,subj1), face_symm1(csvfile,subj2)]
        OP2 = [fac_dist(csvfile,subj1),fac_dist1(csvfile,subj2)]
        OP3 = op3function(csvfile)  
        OP4 = cosine_similarity(fac_dist(csvfile,subj1),fac_dist1(csvfile,subj2))
    except Exception as e:
        print(e)
        return
    return OP1, OP2, OP3, OP4

def read_with_ID(csvfile,adultID):
    file = open(csvfile)
    #This header is used to make sure everything is in order (SubjID, Landmark and both X, Y, Z 's) and to also make sure all 8 columns exist
    try:
        header = next(file)
        first, second, third, fourth, fifth, sixth, seventh, eighth = header[:-1].split(',')
        header_list = [first.upper(), second.upper(), third.upper(), fourth.upper(), fifth.upper(), sixth.upper(), seventh.upper(), eighth.strip('\n').upper()]
    except:
        return None
    #Set for no duplicates
    corrupted = set()
    newlist = {}
    for line in file:
        row = line.split(',')
        #Getting index of each column in header, returning none if at least one column is missing/mispelled
        try:
            id_ind = header_list.index('SUBJID')
            mark_ind = header_list.index('LANDMARK')
            ox_ind = header_list.index('OX')
            oy_ind = header_list.index('OY')
            oz_ind = header_list.index('OZ')
            mx_ind = header_list.index('MX')
            my_ind = header_list.index('MY')
            mz_ind = header_list.index('MZ')
        except:
            return None
        
        #Checking to see if subject ID is valid
        try:
            if(row[id_ind] in newlist):
                newlist[row[id_ind]][row[mark_ind].upper()] = [float(row[ox_ind]), float(row[oy_ind]), float(row[oz_ind]), float(row[mx_ind]), float(row[my_ind]), float(row[mz_ind])]
            else:
                newlist[row[id_ind]] = {row[mark_ind].upper(): [float(row[ox_ind]), float(row[oy_ind]), float(row[oz_ind]), float(row[mx_ind]), float(row[my_ind]), float(row[mz_ind])]}
        except:
            corrupted.add(row[id_ind])
            
    #List comprehension to remove anything invalid from final dictionary       
    #Try statement to see if all 7 landmarks (Ft, En, Ex, etc) exist. Returning none if at least one value is missing
    try:
        [newlist.pop(subject)for subject in corrupted]
    except:
        return None
    
    #Try statement to see if all values in columns exist (returns final dictionary of subjectID), return none otherwise
    #[adultID] to get values of adultID
    try:
        if adultID == 'op4input':
            return newlist.keys()
        else:
            final_dict= newlist[adultID]
            for k in final_dict:
                for x in final_dict[k]:
                    if (-200.0 > x)  or (x > 200.0):
                        return None
                else:
                    return final_dict
    except:
        return None
        
#Comments are numbered throughout each function for OP1 (OP2 functions are very similar to OP1 functions, so less comments)    
#1. Both functions are for OP1, one face each. The ind/test = face.get('landmark') is just to get the values for each landmark
#2. Since after it outputs a list, we put it in a list of lists and loop through it using the index into the facial asymmetry formula
#3. Then it is made into a dictionary by zipping. We then check if PRN is equal to 0.0, remove it from the dictionary if it is otherwise return false
#4. Try statements in both functions. It is to check if anything is invalid, return None for EACH subjectID if so.
def face_symm(csvfile, subj1):
    try:
        #1.
        face1 = read_with_ID(csvfile, subj1)
        ind1 = face1.get('FT')
        ind2 = face1.get('EX')
        ind3 = face1.get('EN')
        ind4 = face1.get('AL')
        ind5 = face1.get('SBAL')
        ind6 = face1.get('CH')
        ind7 = face1.get('PRN')
        
        #2.
        lst = []
        indexxlist = [ind1,ind2,ind3,ind4,ind5,ind6,ind7]
        i = 0
        while i < len(indexxlist):
            addedind = round((((indexxlist[i][3]-indexxlist[i][0]) ** 2) + ((indexxlist[i][4]-indexxlist[i][1]) ** 2) + ((indexxlist[i][5]-indexxlist[i][2]) ** 2) )** (1/2),4)
            i += 1
            lst.append(addedind)
            
            #3. 
            lndmrk_dict = ['FT', 'EX', 'EN', 'AL', 'SBAL', 'CH', 'PRN']
            dict1=zip(lndmrk_dict,lst)
            face1dict = dict(dict1)
        if face1dict.get('PRN') == 0.0:
            face1dict.pop('PRN')
        else:
            return None          
    except:
        return None
    return face1dict

def face_symm1(csvfile, subj2):
    try:
        #1.
        face2 = read_with_ID(csvfile, subj2)
        test11 = face2.get('FT')
        test22 = face2.get('EX')
        test33 = face2.get('EN')
        test44 = face2.get('AL')
        test55 = face2.get('SBAL')
        test66 = face2.get('CH')
        test77 = face2.get('PRN')
        
        #2.
        lst1 = []
        testlst1 = [test11,test22,test33,test44,test55,test66,test77]
        i = 0
        while i < len(testlst1):
            test = round((((testlst1[i][3]-testlst1[i][0]) ** 2) + ((testlst1[i][4]-testlst1[i][1]) ** 2) + ((testlst1[i][5]-testlst1[i][2]) ** 2) )** (1/2),4)
            i += 1
            lst1.append(test)
            
            #3.
            lndmrk_dict1 = ['FT', 'EX', 'EN', 'AL', 'SBAL', 'CH', 'PRN']
            dict2=zip(lndmrk_dict1,lst1)
            face2dict = dict(dict2)
        if face2dict.get('PRN') == 0.0:
            face2dict.pop('PRN')
        else:
            return None
    except:
        return None            
    return face2dict

#These are functions for OP2
#Very similar process to OP1 functions above, just different inputs for the formula
def fac_dist(csvfile, subj1):
    try:
        face1 = read_with_ID(csvfile, subj1)
        ftindex = face1.get('FT')
        exindex = face1.get('EX')
        enindex = face1.get('EN')
        alindex = face1.get('AL')
        sbalindex = face1.get('SBAL')
        chindex = face1.get('CH')
        
        exen1 = round((((exindex[0]-enindex[0]) ** 2) + ((exindex[1]-enindex[1]) ** 2) + ((exindex[2]-enindex[2]) ** 2) )** (1/2),4)
        enal1 = round((((enindex[0]-alindex[0]) ** 2) + ((enindex[1]-alindex[1]) ** 2) + ((enindex[2]-alindex[2]) ** 2) )** (1/2),4)
        alex1 = round((((alindex[0]-exindex[0]) ** 2) + ((alindex[1]-exindex[1]) ** 2) + ((alindex[2]-exindex[2]) ** 2) )** (1/2),4)
        ftsbal1 = round((((ftindex[0]-sbalindex[0]) ** 2) + ((ftindex[1]-sbalindex[1]) ** 2) + ((ftindex[2]-sbalindex[2]) ** 2) )** (1/2),4)
        sbalch1 = round((((sbalindex[0]-chindex[0]) ** 2) + ((sbalindex[1]-chindex[1]) ** 2) + ((sbalindex[2]-chindex[2]) ** 2) )** (1/2),4)
        chft1 = round((((chindex[0]-ftindex[0]) ** 2) + ((chindex[1]-ftindex[1]) ** 2) + ((chindex[2]-ftindex[2]) ** 2) )** (1/2),4)
        
        joined_lndmrk = ['EXEN','ENAL','ALEX','FTSBAL','SBALCH','CHFT']
        lndmrk_values = [exen1,enal1,alex1,ftsbal1,sbalch1,chft1]
        joinedict=zip(joined_lndmrk, lndmrk_values)
        face1op2 = dict(joinedict)
    except:
        return None
    return face1op2

def fac_dist1(csvfile, subj2):
    try:
        face2= read_with_ID(csvfile, subj2)
        ftindex1 = face2.get('FT')
        exindex1 = face2.get('EX')
        enindex1 = face2.get('EN')
        alindex1 = face2.get('AL')
        sbalindex11 = face2.get('SBAL')
        chindex1 = face2.get('CH')
          
        exen2 = round((((exindex1[0]-enindex1[0]) ** 2) + ((exindex1[1]-enindex1[1]) ** 2) + ((exindex1[2]-enindex1[2]) ** 2) )** (1/2),4)
        enal2 = round((((enindex1[0]-alindex1[0]) ** 2) + ((enindex1[1]-alindex1[1]) ** 2) + ((enindex1[2]-alindex1[2]) ** 2) )** (1/2),4)
        alex2 = round((((alindex1[0]-exindex1[0]) ** 2) + ((alindex1[1]-exindex1[1]) ** 2) + ((alindex1[2]-exindex1[2]) ** 2) )** (1/2),4)
        ftsbal2 = round((((ftindex1[0]-sbalindex11[0]) ** 2) + ((ftindex1[1]-sbalindex11[1]) ** 2) + ((ftindex1[2]-sbalindex11[2]) ** 2) )** (1/2),4)
        sbalch2 = round((((sbalindex11[0]-chindex1[0]) ** 2) + ((sbalindex11[1]-chindex1[1]) ** 2) + ((sbalindex11[2]-chindex1[2]) ** 2) )** (1/2),4)
        chft2 = round((((chindex1[0]-ftindex1[0]) ** 2) + ((chindex1[1]-ftindex1[1]) ** 2) + ((chindex1[2]-ftindex1[2]) ** 2) )** (1/2),4)
        
        joined_lndmrk1 = ['EXEN','ENAL','ALEX','FTSBAL','SBALCH','CHFT']
        lndmrk_values1 = [exen2,enal2,alex2,ftsbal2,sbalch2,chft2]
        joinedict1=zip(joined_lndmrk1, lndmrk_values1)
        face2op2 = dict(joinedict1)
    except:
        return None
    return face2op2

#These are the functions for OP3
#The function below is just an unrounded version of face_symm
def unrounded(csvfile, subj1):
    try:
        #1.
        faceop3 = read_with_ID(csvfile, subj1)
        test1 = faceop3.get('FT')
        test2 = faceop3.get('EX')
        test3 = faceop3.get('EN')
        test4 = faceop3.get('AL')
        test5 = faceop3.get('SBAL')
        test6 = faceop3.get('CH')
        test7 = faceop3.get('PRN')
        
        #2.
        lst = []
        testlst = [test1,test2,test3,test4,test5,test6,test7]
        i = 0
        while i < len(testlst):
            test = (((testlst[i][3]-testlst[i][0]) ** 2) + ((testlst[i][4]-testlst[i][1]) ** 2) + ((testlst[i][5]-testlst[i][2]) ** 2) )** (1/2)
            i += 1
            lst.append(test)
            
            #3. 
            lndmrk_dict = ['FT', 'EX', 'EN', 'AL', 'SBAL', 'CH', 'PRN']
            dict1=zip(lndmrk_dict,lst)
            faceop3dict = dict(dict1)
        if faceop3dict.get('PRN') == 0.0:
            faceop3dict.pop('PRN')
        else:
            return None          
    except:
        return None
    return faceop3dict

def op3function(csvfile):
    try:
        allIDs = read_with_ID(csvfile,'op4input')
        allIDlist = list(allIDs)
        
        newarray = [] #new empty array
        #looping through the index elements of list
        i = 0
        while i < len(allIDlist):
            eachdict = unrounded(csvfile, allIDlist[i])
            i += 1
            newarray.append(eachdict)
        #Checking for indexes that are None to remove in adultID as well
        l=[i for i in range(len(newarray)) if newarray[i] == None]
        for z in sorted(l, reverse=True):
            del allIDlist[z]
            
        #Here we remove none values from the numbered list so it can loop
        noNone = []
        for val in newarray:
            if val != None:
                noNone.append(val)
        #List of the total facial asymmetries for each valid subjID
            onlynumbers = []
            x = 0
            while x < len(noNone):
                adding = round(sum(noNone[x].values()),4)
                x += 1
                onlynumbers.append(adding)
                
        #Using lambda to get tuples and first 5 from minimum sorted list
        min_list = sorted(zip(allIDlist, onlynumbers), key=lambda t: t[1])[:5]
    except:
        return None
    return min_list


#This is the function for OP4
def cosine_similarity(op2lst1, op2lst2):
    try:
        #initializing, then we match the landmarks and use the index for the formula
        numerator, denom1, denom2 = 0, 0, 0
        both_dist = ['EXEN','ENAL','ALEX','FTSBAL','SBALCH','CHFT']

        for i in both_dist:
            numerator += op2lst1[i] * op2lst2[i]
            denom1 += op2lst1[i] * op2lst1[i] 
            denom2 += op2lst2[i] * op2lst2[i]
    except:
        return None
    return round(numerator / ((denom1 ** 0.5) * (denom2 ** 0.5)),4)
print(main('TestData4.csv',('D8328','E4996')))