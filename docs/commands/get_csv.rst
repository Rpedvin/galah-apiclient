get_csv
=======

Get a CSV containing all of the scores of all of the students for a particular
assignment.

The format of the CSV is ``email,score,date``, where score will be ``None`` if
the user's last submission did not have a score associated with it.

Example of a line: ``magicman@school.edu,None,2013-02-12-13-31-02``.

Note that currently only the most recent submission is grabbed, it does not look
for the most recent submission with a score.

Reference
---------

.. function:: get_csv(assignment):
    
    :param id: The assignment to grab scores for.

Example Usage
-------------

>>> get_csv 10/6
--Acting as user john@admin.edu--
The CSV file for this assignment is being created.
The server is requesting that you download a file...
Where would you like to save it (default: ./assignment.csv)?: 
File ./assignment.csv already exists, would you like to overwrite it (y, n)? y
File saved to ./assignment.csv.

Permissions
-----------

**admin** and **teacher** users can use this command.
