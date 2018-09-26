# The main script that takes in the bulk ZIP archive and organizes it by
# student in the user's section.
# =============================================================================
# General Structure of submission ZIP:
# Name: Class-Name-Section-Assignment-Name_submissions.zip
#   ex. CS-2261-A-Lab02_submissions.zip
# Contents: for every student, the following:
#   lastfirstmiddle_{number}_{number}_submissionname.zip
#       this is the actual student submission zip, renamed with the prefix


# Setup initial config variables
download_path = "~/Downloads"
course_prefix = "CS-2261-A-"
submission_suffix = "_submissions.zip"
dest_directory = "~/Documents/GT/CS2261/ToGrade"


# Give welcome message
print "Welcome to the CS 2261 Canvas Student Submission Organizer!"
print "\t...searching for config folder"
# TODO If there is no "./config" directory
print "\t\tNone found."
print "\t...creating config folder"
# TODO Create the config directory "./config"
# TODO Create the empty student file "./config/students.txt"
print "\t...searching for submissions in %s" % download_path
# TODO If there is no download found
print "\t\tNone found matching pattern '%sASSIGNMENT%s'" % \
    (course_prefix, submission_suffix)
print "No bulk download ZIP file from Canvas found."
print "Try downloading again, then re-run this organizer."
# TODO Else (the download was found)
submission_title = ""
print "\t\tFound %s" % submission_title
assignment_title = ""
# TODO Unzip the bulk folder to "./temp_itsname"
print "\t...unzipping bulk submission folder into temporary file"
# TODO For all the submissions in the folder
print "\t...assigning submissions to students"
# TODO Create a dictionary mapping student lastfirstmiddle to their filename
# TODO If the "./config/students.txt" is empty, ask user which to add to it
section = []  # Array of lastfirstmiddle of students in section
# TODO Warn user of students in section who did not submit any file
missing_subs = []  # Array of names of students with no submission
# TODO Iterate through students in section, add to missing if not in dictionary
if len(missing_subs) > 0:
    print "\t   Missing Submission for: ",
    for student in missing_subs:
        print student,
    print ""  # Force newline
# TODO Delete submissions for students not in "./config/students.txt"
print "\t...removing submissions for students from other sections"
# TODO Create folder for this assigment in dest_directory
print "\t...creating folder for %s" % assignment_title
# TODO Create folder for each student
print "\t...creating student subfolders"
# TODO Unzip student submissions to the folder
print "\t...unzipping student submissions into student subfolders"
student = ""
submission = ""
# TODO If file could not be unzipped, report the error and just copy to folder
print "\t\tSubmission by '%s' could not be unzipped." % student
print "\t\t\tSubmission: '%s'" % submission
print "\t\t...copying problem file to student subfolder"
# TODO Copy the nonfunctional zip to the student's subfolder
# TODO Else, remove the zip
# TODO Remove the temporary folder and original zip
print "\t...removing temp folder"
print "\t...removing bulk submission zip"
print "Done."

