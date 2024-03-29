# -*- coding: utf-8 -*-
import os
from optparse import OptionParser


def main(input_file_path, schema, table):
    """This function takes in an input file path, a schema, and a table name and creates a new output file in the same directory as the input file. The output file will have a $node_id column added to each line. The function returns the output file path.

    :param input_file_path: str
    :param schema: str
    :param table: str
    :returns: output_file_path (str): The path to the output file.
    Processing Logic:
        - Creates an output file path by adding '_as_node.csv' to the end of the input file path.
        - Opens the input file and output file using the specified encoding.
        - Reads each line of the input file and adds a $node_id column to the beginning of the line.
        - Writes the modified line to the output file.
        - Increments the line number and continues until the end of the input file is reached.

    """

    # create the output file in the same directory as the input file
    output_file_path = os.path.splitext(input_file_path)[0] + "_as_node" + ".csv"

    # you may have to change the encoding
    with open(
        input_file_path, mode="r", encoding="utf-16le", newline=""
    ) as input_file, open(
        output_file_path, mode="w", encoding="utf-16le", newline=""
    ) as output_file:

        line = input_file.readline(5_000_000)
        line_number = 0

        # read each line of the input file, add a $node_id column and write down the result on the output file
        while line:
            if line_number == 0:
                newline = (
                    "\ufeff"
                    + '{"type":"node","schema":"'
                    + schema
                    + '","table":"'
                    + table
                    + '","id":'
                    + str(line_number)
                    + "}\t"
                    + line[1:]
                )
            else:
                newline = (
                    '{"type":"node","schema":"'
                    + schema
                    + '","table":"'
                    + table
                    + '","id":'
                    + str(line_number)
                    + "}\t"
                    + line
                )
            output_file.write(newline)
            line_number += 1
            line = input_file.readline(5_000_000)


if __name__ == "__main__":

    parser = OptionParser()

    parser.add_option(
        "-f", "--file", action="store", type="string", dest="input_file_name"
    )
    parser.add_option("-s", "--schema", action="store", type="string", dest="schema")
    parser.add_option("-t", "--table", action="store", type="string", dest="table")

    (options, args) = parser.parse_args()

    # retrieve options if not provided by the user
    if options.input_file_name == None:
        options.name = input(
            "Please enter the full path to the csv file you will import as a node table:"
        )
    if options.schema == None:
        options.name = input(
            "Please enter the SQL schema of the node table you will populate:"
        )
    if options.table == None:
        options.name = input(
            "Please enter the SQL name of the node table you are populate:"
        )

    main(options.input_file_name, options.schema, options.table)
