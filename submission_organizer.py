# The main script that takes in the bulk ZIP archive and organizes it by
# student in the user's section.
# =============================================================================
# General Structure of submission ZIP:
# Name: Class-Name-Section-Assignment-Name_submissions.zip
#   ex. CS-2261-A-Lab02_submissions.zip
# Contents: for every student, the following:
#   lastfirstmiddle_{number}_{number}_submissionname.zip
#       this is the actual student submission zip, renamed with the prefix

import os
import shutil
import sys
import zipfile

# Setup initial config variables
download_path = ''
course_prefix = "CS-2261-A-"
submission_suffix = "_submissions.zip"
tograde_path = ''
students = []
nonsection_students = []
basepath = os.getcwd()
_divider = '='*80

# Give welcome message
print ("\n" + _divider)
print "Welcome to the CS 2261 Canvas Student Submission Organizer!"
print "    ...searching for config folder"

def test_config():
    """Return whether a config folder exists in a completed state.
    """

    if not os.path.exists(basepath + "/.config"):
        print "        None found."
        return False
    
    # Not checking student file, because an empty one causes the assigner
    # if not os.path.exists(basepath + "/.config/students.txt"):
    #    print "        No student file found in config folder."
    #    return False
    
    if not os.path.exists(basepath + "/.config/paths.txt"):
        print "        No paths file found in config folder."
        return False

    pathfile = open(basepath + "/.config/paths.txt", 'r')
    paths = pathfile.read()
    pathfile.close()

    paths = paths.split('\n')
    if len(paths) < 2:
        print "        No valid paths file found in config folder."
        return False
    paths = paths[0].split('=') + paths[1].split('=')
    if len(paths) < 4 or \
            paths[0] != "DOWNLOAD_PATH" or \
            paths[2] != "TOGRADE_PATH" or \
            not os.path.exists(paths[1]) or \
            not os.path.exists(paths[3]):
        print "        No valid paths file found in config folder."
        return False

    # No problems with config, so return True
    return True

def init_config():
    """Initialize a new config folder.
    Called if a valid one was not found at startup.
    """
    
    # Create the config folder
    if not os.path.exists(basepath + "/.config"):
        print "    ...creating new config folder"
        os.mkdir(basepath + "/.config")

    # Opting to not do this and have the assigner do it later
    # Create the students file (will be populated later)
    # open(basepath + "/.config/students.txt", 'w+').close()

    # Get the paths file output ready
    newpaths = ''

    # Find the download path
    print ("\nEnter the path to your downloads folder (where you expect to find"
           " the bulk\ndownload folder from Canvas):")
    print "> ", # raw_input prompt not working because of flushing
    sys.stdout.flush()
    download_path = raw_input()
    while not os.path.exists(download_path):
        print ("\nThe path '%s' does not exist,\nor you do not have permission"
                " to access it. Enter another path:") % download_path
        print "> ",
        sys.stdout.flush()
        download_path = raw_input()
    newpaths = "DOWNLOAD_PATH=" + download_path + '\n'

    # Find the to-grade directory path
    print ("\nEnter the path to the folder you want to put the assignment "
           "folder, full of\norganized submissions:")
    print "> ",
    sys.stdout.flush()
    tograde_path = raw_input()
    while not os.path.exists(tograde_path):
        print "\n'%s' does not exist.\nWould you like to create it? (Y/N)" % \
            tograde_path
        print "> ",
        sys.stdout.flush()
        choice = raw_input()
        if choice.lower() == 'y':
            try:
                os.mkdir(tograde_path)
            except OSError:
                print "\nCould not create '%s'." % tograde_path
                choice = ''
        else:
            print ''  # Newline for when not 'Y', but not when OSError
        if not choice.lower() == 'y':
            print "Enter another path:"
            print "> ",
            sys.stdout.flush()
            tograde_path = raw_input()

    newpaths += "TOGRADE_PATH=" + tograde_path

    # Write the new paths to the file
    pathfile = open(basepath + '/.config/paths.txt', 'w+')
    pathfile.write(newpaths)
    pathfile.close()
    
    print "\nConfig folder created.\n"
    sys.stdout.flush()

def read_config():
    """Reads in the config files to set the script config variables.
    Returns nothing, but sets the global variables.
    """
    
    # Reference the global variables
    global students
    global nonsection_students
    global download_path
    global tograde_path
    
    # Get the students list
    # If it does not exist, the assigner will make it later
    if os.path.exists(basepath + "/.config/students.txt"):
        studfile = open(basepath + "/.config/students.txt", 'r')
        students = studfile.read().split('\n')
        studfile.close()
        while '' in students:
            students.remove('')
    else:
        students = []

    # Get the list of students not in the grader's section
    if os.path.exists(basepath + "/.config/nonsection.txt"):
        studfile = open(basepath + "/.config/nonsection.txt", 'r')
        nonsection_students = studfile.read().split('\n')
        studfile.close()
        while '' in nonsection_students:
            nonsection_students.remove('')
    else:
        nonsection_students = []

    # Get the download path and to-grade directory
    pathfile = open(basepath + "/.config/paths.txt", 'r')
    paths = pathfile.read().split('\n')
    pathfile.close()
    paths = paths[0].split('=') + paths[1].split('=')
    download_path = paths[1]
    tograde_path = paths[3]
 
# Check if further setup is needed, or has been completed
if not test_config():
    sys.stdout.flush()
    init_config()
read_config()

# Get the submission file
print "    ...searching for bulk submission archive in %s" % download_path

possibles = []
for item in os.listdir(download_path):
    suffix_index = item.rfind(submission_suffix)
    if suffix_index > 0 and \
        suffix_index == len(item) - len(submission_suffix) and \
        item.find(course_prefix) == 0:
            possibles += [item]

# If there were no possible bulk submission files found
if len(possibles) == 0:
    print "        None found matching pattern '%sASSIGNMENT%s'" % \
        (course_prefix, submission_suffix)
    print _divider + '\n'
    print "No bulk download ZIP file from Canvas found."
    print "Try downloading again, then re-run this organizer."
    sys.exit()

# If possibles have a file in tograde already, remove then as a possible
for item in [copy for copy in possibles]:
    possible_title = item[len(course_prefix): \
        item.rfind(submission_suffix)]
    if os.path.exists(tograde_path + '/' + possible_title): 
        possibles.remove(item)

# If possibles is now empty, all bulk submission files have already been graded
if len(possibles) == 0:
    print "        No ungraded bulk zips found."
    print _divider
    print ("\nThere are bulk submission zips, but all of them already have "
            "been previously\nprocessed. Delete the assignment folders in\n'%s'"            " to reprocess them.") % tograde_path
    sys.exit()

submission_title = possibles[0]

print "        Submission selected:", submission_title
assignment_title = submission_title[len(course_prefix): \
    submission_title.rfind(submission_suffix)]
print "        Assignment title:", assignment_title



# Create temporary folder and unzip submission folder to it
temp_path = download_path + "/temp_" + submission_title[:-4]
if os.path.exists(temp_path):  # If temp_file was previously undeleted
    shutil.rmtree(temp_path, ignore_errors=True)  # Remove the entire tree
os.mkdir(temp_path)
print "    ...unzipping bulk submission folder into temporary file"
bulk = zipfile.ZipFile(download_path + '/' + submission_title)
bulk.extractall(temp_path)


def assign_students():
    """Assigns students to the students file in the config folder.
    Assigns all other students to the nonstudents file.
    This is called after unzipping to the temp folder if the students file is
    empty."""

    students_all = []
    for item in os.listdir(temp_path):
        # Add 'lastfirstmiddle' from the filename 'lastfirstmiddle_2345_etc...'
        students_all += [item[:item.find('_')]]

    # Assign students numbers for section assignment
    non_section = {}
    for i in range(1,len(students_all)+1):
        non_section[i] = students_all[i-1]
    section = {}

    # Prepare to build the tables of students in the section and not
    max_namelen = max([len(name) for name in students_all])
    table_colsize = 6 + max_namelen  # Each item is ' ###: lastmiddlefirst'
    table_cols = 80 // table_colsize

    # Giant ugly loop for printing the section and non_section tables
    # ...and taking the user input for whether to add or remove from section
    # ...and actually doing the adding and removing
    choice = -1
    while choice != 3:

        # Place non-section students in table
        print "\n" + _divider + ("\nStudents not in section (format is "
            "lastname - firstname - middlename):\n") + _divider
        cur_col = 0
        for number in sorted(non_section):
            if cur_col == table_cols:
                print ''
                cur_col = 0
            print (" %3d: %-"+str(max_namelen)+"s") % \
                    (number, non_section[number]),
            cur_col += 1
        print ''

        # Place section students in table
        print _divider + "\nStudents in section:\n" + _divider
        cur_col = 0
        for number in sorted(section):
            if cur_col == table_cols:
                print ''
                cur_col = 0
            print (" %3d: %-"+str(max_namelen)+"s") % (number, section[number]),
            cur_col += 1
        print ''

        # Decide whether to add, remove, or save section
        print _divider + ("\nSELECT: (1) Add to section, (2) Remove from "
                          "section, (3) Save section and finish\n> "),

        choice = 4  # Code for not a valid selection
        while choice == 4:
            sys.stdout.flush()
            choice = raw_input()
            if '1' in choice or 'add' in choice.lower():
                print ("\nEnter student numbers to add to section "
                       "(eg. 1, 3, 8):\n> "),
                choice = 1
            elif '2' in choice or 'remove' in choice.lower():
                print ("\nEnter student numbers to remove from section "
                       "(eg. 1, 3, 8):\n> "),
                choice = 2
            elif '3' in choice or 'save' in choice.lower():
                choice = 3
            else:
                print "'" + choice + "' is not a valid selection.\n> ",
                choice = 4
    
        # Interpret choice
        stud_list = []
        if choice == 1 or choice == 2:  # Add or remove
            sys.stdout.flush()
            in_list = raw_input().split(',')
            for item in in_list:
                try:
                    stud_list += [int(item)]
                except:
                    pass
        if choice == 1:  # Add
            for number in stud_list:
                if number in non_section:
                    section[number] = non_section[number]
                    del non_section[number]
        elif choice == 2:  # Remove
            for number in stud_list:
                if number in section:
                    non_section[number] = section[number]
                    del section[number]
        else:  # Save

            if len(section) == 0:  # No students actually added
                return
            
            global students
            global nonsection_students
            students = [section[number] for number in sorted(section)]
            nonsection_students = [non_section[number] for number in \
                sorted(non_section)]
            print ''
            print _divider + "\nFinal Section:\n" + _divider
            max_namelen = max([len(name) for name in students]) + 2
            table_cols = 80 // max_namelen
            col_num = 0
            for student in students:
                if col_num == table_cols:
                    print ''
                    col_num = 0
                print ("%-"+str(max_namelen)+"s") % student,
                col_num += 1
            print ''
            print _divider

            # Save the results to the config files
            print "    ...saving section to configs"
            studfile = open(basepath + '/.config/students.txt', 'w+')
            for student in students:
                studfile.write(student + "\n")
            studfile.close()

            studfile = open(basepath + '/.config/nonsection.txt', 'w+')
            for student in nonsection_students:
                studfile.write(student + "\n")
            studfile.close()

# Check to see if assigning students to section is necessary
while len(students) == 0:
    print "\nStudents have not been assigned to your section."
    print "Press Enter to open the section assigner..."
    sys.stdout.flush()
    raw_input()
    assign_students()
    if len(students) == 0:
        print "\n\nAssigning resulted in no students being added..."

# Find submissions of students in grader's section
print "    ...assigning submissions to students"
submissions = {}
unclassified = {}
for submission in os.listdir(temp_path):
    author = submission[:submission.find('_')]
    if author in students:  # We want to process this submission
        submissions[author] = submission
    elif author not in nonsection_students:  # The student is unclassified
        unclassified[author] = submission

# Consider adding unclassified students to section
if len(unclassified) > 0:
    new_students = {}
    for i in range(1, len(unclassified)+1):
        new_students[i] = unclassified.keys()[i-1]
    print "\nThe following students have not been seen in a previous session:"
    for number in new_students:
        print "%2d: %s" % (number, new_students[number])
    print "\nEnter student numbers to add to section (eg. 1, 3, 8)\n> ",
    sys.stdout.flush()
    in_list = raw_input().split(',')

    # Interpret the input and remove them from new_students
    stud_list = []
    for item in in_list:
        try:
            stud_list += [int(item)]
        except:
            pass
    changes = []
    for number in stud_list:
        if number in new_students:
            changes += [new_students[number]]
            del new_students[number]

    # If students were selected, add to students, submissions, and config
    if len(changes) > 0:
        print "\nThe following students have been added to your section:"
        studfile = open(basepath + "/.config/students.txt", 'a')
        for student in changes:
            studfile.write(student + '\n')
            students += [student]
            submissions[student] = unclassified[student]
            print "  " + student
        studfile.close()
        print '\n'

    # Add the unchosen unclassified students to the nonsection
    studfile = open(basepath + "/.config/nonsection.txt", 'a')
    for number in new_students:
        studfile.write(new_students[number] + '\n')
        nonsection_students += [new_students[number]]
    studfile.close()

# Find students in section with no submission
missing_subs = []
for student in submissions:
    if len(submissions[student]) == 0:
        missing_subs += [student]
        del submission[student]

# Make project folder for unzipping submissions
tograde_path += '/' + assignment_title
os.mkdir(tograde_path)



# At the end, report which students in section had no submission
if len(missing_subs) > 0:
    print "        Missing submission for the following:"
    for student in missing_subs:
        print "  " + student,
    print ''
# TODO Delete submissions for students not in "./config/students.txt"
print "    ...removing submissions for students from other sections"
# TODO Create folder for this assigment in dest_directory
print "    ...creating folder for %s" % assignment_title
# TODO Create folder for each student
print "    ...creating student subfolders"
# TODO Unzip student submissions to the folder
print "    ...unzipping student submissions into student subfolders"
student = ""
submission = ""
# TODO If file could not be unzipped, report the error and just copy to folder
print "        Submission by '%s' could not be unzipped." % student
print "            Submission: '%s'" % submission
print "        ...copying problem file to student subfolder"
# TODO Copy the nonfunctional zip to the student's subfolder
# TODO Else, remove the zip
# TODO Remove the temporary folder and original zip
print "    ...removing temp folder"
print "    ...removing bulk submission zip"
print "Done."

