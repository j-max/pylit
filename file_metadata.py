import glob
import os


def find_directory_files(directory_path):
    
    dir_files = glob.glob(
        directory_path + "**/*.txt", 
        recursive=True
    )

    return dir_files


def sort_files_by_modified_date(list_of_file_paths):

    """Given a list of file_paths, sort all files
    by date modified.  

    parameters: 
    directory_path: a list of file paths in a directory path to search
    
    Return:
    dir_files: List of tuples with first value the date modified 
    in osfiles and their date modified.
    TIme is in seconds relative to when time starts (Jan)
    """

    # define a list of tuples with time modified and the path to the file
    file_times = [
        (os.path.getmtime(file_name), 
         file_name
        ) for file_name in list_of_file_paths
    ] 
    # Sort list by the time modified, most recent first
    file_times.sort(reverse=True)

    return file_times


def count_words_in_file(list_of_file_paths):

    """
    Given a list of file_paths, count the words in each file 
    """

    # Define tuple of word_counts to allow sorting
    word_counts = []

    for file_path in list_of_file_paths:

        # count the number of words in each path
        number_of_words = 0
        with open(file_path, 'r') as read_file:
            data = read_file.read()
    
            lines = data.split()

            number_of_words += len(lines)
            
            word_counts.append((number_of_words,file_path))

    # sort the results by files with most words
    word_counts.sort(reverse=True)

    # define dictionary of file_name: word_count that is sorted
    # by word count
    word_counts = {
        file_info[1]: file_info[0]
        for file_info in word_counts
    }

    return word_counts