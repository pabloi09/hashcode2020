def get_lib_total_score(lib_idx):
    global scoreMap,libraries
    lib_total_score = 0
    lib_book_list = libraries[lib_idx]['books_list']
    for book_id in lib_book_list:
        lib_total_score += scoreMap[book_id]

    return lib_total_score


#gets(integer): library ID
# returns(list): library grade
# lib_grade = lib_total_score/(Ndays + (Nbooks/days_rate))
def get_lib_grade(lib_id):
    global scoreMap,libraries
    lib_grade = 0

    lib_total_score = get_lib_total_score(lib_id)
    Ndays = libraries[lib_id]['Ndays_lib']
    Nbooks = libraries[lib_id]['Nbooks']
    days_rate = libraries[lib_id]['books_rate']

    lib_grade = lib_total_score/(Ndays + (Nbooks/days_rate))

    return lib_grade


def get_provisional_list_graded_libs():
    global scoreMap,libraries
    list_graded_libs = []

    for lib_idx in range(len(libraries)):
            list_graded_libs.append(get_lib_grade(lib_idx))

    return list_graded_libs

def get_list_graded_libs(provisional_list_graded_libs):
    global scoreMap,libraries
    result = provisional_list_graded_libs

    for i in range(len(provisional_list_graded_libs)):
        if libraries[i]['Ndays_lib'] >= Ndays:
            result[i] = None
    return result

def update_libraries_grade_cabe():
    global scoreMap,libraries
    list_grades = []
    list_grades = get_list_graded_libs(get_provisional_list_graded_libs())

    for i in range(len(libraries)):

        libraries[i]['grade'] = list_grades[i]
        if list_grades[i] == None:
            libraries[i]['cabe'] = False

def getScannedBooks(fileName):
  global scoreMap,libraries
  # Imput data parsing
  fin = open(fileName+".txt","r")
  global Nbooks, Nlibraries, Ndays
  Nbooks, Nlibraries, Ndays = map(int,fin.readline().split())
  scores = list(map(int,fin.readline().split()))
  sortedScores = sorted(scores, reverse = True)
  for i in range(Nbooks):
    scoreMap[i] = scores[i]

  for i in range(Nlibraries):
    library = {}
    n, days, rate = map(int, fin.readline().split())
    library["id"] = i
    library["Nbooks"] = n
    library["Ndays_lib"] = days
    library["books_rate"] = rate
    library["books_list"] = list(map(int,fin.readline().split()))
    library["books_scanned"] = ""
    library["counter"] = 0
    library["grade"] = 0
    library["cabe"] = True
    libraries.append(library)

  
  update_libraries_grade_cabe()
 
  libraries = sorted(libraries, key=lambda library: library["grade"], reverse = True)
  
  signed_up = []
  library_signing = 0
  days_of_signing = 0
  scanned = []
  for d in range(Ndays):
    if library_signing < len(libraries) and days_of_signing == libraries[library_signing]["Ndays_lib"] : 
      signed_up.append(library_signing)
      days_of_signing = 0
      library_signing += 1
      if library_signing < len(libraries):
        while library_signing < len(libraries) and (libraries[library_signing]["Ndays_lib"] >= (Ndays - d)) :
          library_signing += 1
      if library_signing < len(libraries):
        libraries[library_signing]["books_list"] = sorted(libraries[library_signing]["books_list"], key=lambda book_id: scoreMap[book_id], reverse = True)
    days_of_signing += 1
    for idx, n in enumerate(signed_up):
      library = libraries[n]

      
      
      for i in range(library["books_rate"]):
        maximumIndex = 0
        if len(library["books_list"]) == 0:
          break
        
        if library["books_list"][maximumIndex] in scanned:
            for j in range(1,len(library["books_list"])):
                if not (library["books_list"][j] in scanned):
                  maximumIndex = j
                  break
            
        library["books_scanned"] = library["books_scanned"] +str(library["books_list"][maximumIndex]) +" " 
        library["counter"] += 1
        if not (library["books_list"][maximumIndex] in scanned):
          scanned.append(library["books_list"][maximumIndex])
        library["books_list"].pop(maximumIndex)
      libraries[n] = library

  f = open("./outputs/" + fileName + "_out.txt", "w")
  f.write(str(len(signed_up)) + "\n")
  for idx, n in enumerate(signed_up):
    if libraries[n]["counter"] != 0:
      f.write(str(libraries[n]["id"]) + " " + str(libraries[n]["counter"]) + "\n")
      f.write(libraries[n]["books_scanned"] + "\n")

  f.close()




fileNames = ["a_example","b_read_on","c_incunabula","d_tough_choices","e_so_many_books","f_libraries_of_the_world"]
for fileName in fileNames:
  scoreMap = {}
  libraries = []
  print("Scanning input with name "+fileName)
  getScannedBooks(fileName)