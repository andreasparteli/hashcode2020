import copy


##### READ & WRITE ###

def read(filepath):
    def read_line(infile):
        line = infile.readline()
        return [int(val) for val in line.split(' ')]

    infile = open(filepath, 'r')

    n_books, n_libs, n_days = read_line(infile)  # LINE 1
    books = read_line(infile)  # LINE 2

    libs = []
    for id in range(0, n_libs):
        lnbooks, lsignup, lships = read_line(infile)  # LINE l1
        lbooks = read_line(infile)  # LINE l2: book ids
        assert lnbooks == len(lbooks), "book number must match"
        libs.append({'id': id, 'signup': lsignup, 'ships': lships, 'books': lbooks})

    infile.close()

    return n_books, n_libs, n_days, books, libs

def libscore(books, libts):
    score = 0
    for b in libts['books']:
        score += books[b]
    return score

def score(books, libs_to_scan):
    score = 0
    for libts in libs_to_scan:
        score += libscore(books, libts)
    return score

def write(libs_to_scan, outfilepath='output.txt'):
    outfile = open(outfilepath, 'w')
    outfile.writelines(f"{len(libs_to_scan)}\n") # how many libs
    for lib_to_scan in libs_to_scan:
        outfile.writelines(f"{lib_to_scan['id']} {len(lib_to_scan['books'])}\n") # lib_id, n_books
        outfile.writelines(" ".join([str(b) for b in lib_to_scan['books']]) + "\n") # list of books

    outfile.close()


### WORK
infilepath = 'in/a_example.txt'
infilepath = 'in/b_read_on.txt'
n_books, n_libs, n_days, books, libs = read(infilepath)


### prepare
libssorted = copy.deepcopy(libs)
# libssorted.sort(key=signup_desc, reverse=False)
for lib in libssorted:
    lib['score'] = libscore(books, lib)
    lib['books'].sort(key=lambda b: books[b], reverse=True)
# libssorted.sort(key=lambda l: l['score'], reverse=True)
libssorted.sort(key=lambda l: l['signup'], reverse=True)

### simulate
libsts = {}
next_signup = 0
for d in range(n_days):
    if d == next_signup and d < n_days - 1:
        pick = libssorted.pop()
        next_signup += pick['signup']
        books_to_pick = max(0, (n_days - d - pick['signup']) * pick['ships'])
        if books_to_pick > 0:
            pickedbooks = pick['books'][0:min(books_to_pick, len(pick['books']))]
            print(f"On day {d} picking lib {pick['id']} (signup: {pick['signup']}, ships: {pick['ships']}) where we scan {len(pickedbooks)} out of {len(pick['books'])} books")

            libsts[pick['id']] = {'signup': d, 'id': pick['id'], 'books': pickedbooks}


libtsinorder = [l for l in libsts.values()]
libtsinorder.sort(key=lambda lib: lib['signup'])
print(f"Score is {score(books, libtsinorder)}")

write(libtsinorder)