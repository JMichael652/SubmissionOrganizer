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
import sys

# Setup initial config variables
download_path = ''
course_prefix = "CS-2261-A-"
submission_suffix = "_submissions.zip"
tograde_path = '' 
basepath = os.getcwd()
students = []

# Give welcome message
print ("\n================================================================="
        "===============")
print "Welcome to the CS 2261 Canvas Student Submission Organizer!"
print "    ...searching for config folder"

def test_config():
    """Return whether a config folder exists in a completed state.
    """

    if not os.path.exists(basepath + "/.config"):
        print "        None found."
        return False
    
    if not os.path.exists(basepath + "/.config/students.txt"):
        print "        No student file found in config folder."
        return False
    
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

    # Create the students file (will be populated later)
    open(basepath + "/.config/students.txt", 'w+').close()

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
        if choice == 'Y' or choice == 'y':
            try:
                os.mkdir(tograde_path)
            except OSError:
                print "\nCould not create '%s'." % tograde_path
                choice = ''
        else:
            print ''  # Newline for when not 'Y', but not when OSError
        if not (choice == 'Y' or choice == 'y'):
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
    global download_path
    global tograde_path
    
    # Get the students list
    studfile = open(basepath + "/.config/students.txt", 'r')
    students = studfile.read().split('\n')
    studfile.close()

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
print "    ...searching for submissions in %s" % download_path

found = False
for item in os.listdir(download_path):
    suffix_index = item.rfind(submission_suffix)
    if suffix_index > 0 and \
        suffix_index == len(item) - len(submission_suffix) and \
        item.find(course_prefix) == 0:
            submission_title = item
    else:  # There was no submission zip found
        print "        None found matching pattern '%sASSIGNMENT%s'" % \
            (course_prefix, submission_suffix)
        print "No bulk download ZIP file from Canvas found."
        print "Try downloading again, then re-run this organizer."
        sys.exit()

print "        Found %s" % submission_title
assignment_title = submission_title.substring(len(course_prefix), suffix_index)
print assignment_title
# TODO Unzip the bulk folder to "./temp_itsname"
print "    ...unzipping bulk submission folder into temporary file"
# TODO For all the submissions in the folder
print "    ...assigning submissions to students"
# TODO Create a dictionary mapping student lastfirstmiddle to their filename
# TODO If the "./config/students.txt" is empty, ask user which to add to it
section = []  # Array of lastfirstmiddle of students in section
# TODO Warn user of students in section who did not submit any file
missing_subs = []  # Array of names of students with no submission
# TODO Iterate through students in section, add to missing if not in dictionary
if len(missing_subs) > 0:
    print "        Missing Submission for: ",
    for student in missing_subs:
        print student,
    print ""  # Force newline
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

