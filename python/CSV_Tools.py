import csv
import os


def csv_reader(file_path, delimiter=",", encoding="utf-8"):
    """
    Reads a csv file and converts to list
    :param file_path: full path to csv
    :param delimiter: separation character
    :param encoding: encoding of csv file
    :return: csv as a list
    """
    with open(file_path, encoding=encoding) as file:
        # read csv
        return list(csv.reader(file, delimiter=delimiter))


def csv_writer(file_path, list_to_write, delimiter=","):
    """
    Writes 2D list to csv. Will create file if it does not exist.
    :param file_path: Path of file to write to
    :param list_to_write: List to write to csv
    :param delimiter: CSV delimiter character
    :return: Writes list to csv file
    """
    with open(file_path, "w") as csv_out:
        writer = csv.writer(csv_out, delimiter=delimiter, lineterminator='\n')
        for i in list_to_write:
            writer.writerow(i)


def text_writer(file_path, content):
    """
    Writes a string to a file. Will create file if it does not exist.
    :param file_path: Path of file to write to.
    :param content: String to write to file
    :return: Writes string to file
    """
    with open(file_path, "w") as f:
        f.write(content)


def column_header_add(csv_list):
    """
    Adds headers to csv as "Column1, Column2, Column3" ...
    :param csv_list: input csv file as a list.
    :return: csv_list with header row added
    """
    row_lengths = [len(x) for x in csv_list]
    max_row_len = max(row_lengths)
    header_names = ["Column" + str(x) for x in range(1, max_row_len + 1)]
    csv_list.insert(0, header_names)


def csv_combine(folder_path):
    """
    Combines all CSVs within a folder.
    Each csv must have same number of headers.
    Columns must be identically ordered.

    :param folder_path: Path to folder without trailing "\\"
    :return: 2D list of combined csv files
    """
    csv_combined = []

    count = 0
    for fileName in os.listdir(folder_path):
        if fileName.endswith(".csv"):
            file_path = folder_path + "\\" + fileName

            # append whole first csv to retain header rows
            if count == 0:
                csv_list = csv_reader(file_path)

                # add "SourceFile" column to csv
                csv_list[0].append("SourceFile")

                # populates "SourceFile" column for each row
                for row in csv_list[1:]:
                    row.append(str(fileName))

                csv_combined.extend(csv_list)

            # if not the first file in directory, append whole csv without the header rows
            else:
                csv_list = csv_reader(file_path)

                # populates "SourceFile" column for each row
                for row in csv_list:
                    row.append(str(fileName))

                csv_combined.extend(csv_list[1:])
        count += 1

    # print(str(count) + " CSVs combined")
    return csv_combined


def single_header(csv_list, header_rows, title_row):
    """
    For CSVs with multiple header rows. Removes all but one header row.
    :param csv_list: csv that has been converted to a 2D list.
    :param header_rows: Number of header rows.
    :param title_row: Header row that contains values to use a header.
    :return: 2D list with a single header.
    """
    header = csv_list[title_row-1]
    csv_content = csv_list[header_rows:]
    csv_list = csv_content.insert(0, header)
    return csv_list


def indexer(header_list, cols_to_index):
    """
    Returns column index numbers when given column names
    :param header_list: A list of all column names
    :param cols_to_index: A list of column names to index
    :return: A list of column index values
    """
    indexes = [header_list.index(x) for x in cols_to_index]
    return indexes


def required_fields(csv_list, cols_to_check):
    """
    Removes any rows that are missing a required value
    :param csv_list: csv that has been converted to a 2D list.
    :param cols_to_check: Column indexes of the columns that should not be null
    :return: A 2D list with only records that contain all required values
    """
    rows_to_remove = []
    new_csv_list = []
    for row in csv_list[1:]:
        for col in cols_to_check:
            if row[col] == "" and row not in rows_to_remove:
                rows_to_remove.append(row)
    for row in csv_list:
        if row not in rows_to_remove:
            new_csv_list.append(row)
    return new_csv_list


def column_reducer(csv_list, cols, remove=True):
    """
    Reduces number of columns in a csv
    :param csv_list: csv that has been converted to a 2D list.
    :param cols: Column indexes to remove or retain
    :param remove: [True  = Remove]  [False = Retain]
    :return: a copy with unwanted columns removed
    """
    if remove is False:
        remove_cols = []
        keep_cols = cols
        for x in range(0, len(csv_list[0])):
            if x not in keep_cols:
                remove_cols.append(x)
        cols = remove_cols

    reduced_csv = [list(x) for x in csv_list]
    cols = sorted(cols, reverse=True)
    for row in reduced_csv:
        for col in cols:
            del row[col]
    return reduced_csv


def unique_col_values(csv_list, col_name, records=False):
    """
    :param csv_list: input csv file as a list.
    :param col_name: Column to filter to unique
    :param records: FALSE sets the function to return a list of the unique values within a column.
                    TRUE sets the function to return a copy of the input where each row is the first row that the
                    unique value appears in.
    :return: Either a 1D list or 2D list depending on "records" variable is set to.
    """
    name_col_index = indexer(csv_list[0], [str(col_name)])
    col_values = [x[name_col_index[0]] for x in csv_list[1:] if x[name_col_index[0]] is not ""]
    unique_value_list = sorted(set(col_values))

    if records is False:
        value_list = unique_value_list
        return value_list

    if records is True:
        # takes first record where unique value appears
        records_unique_val = []
        unique_used = []
        for row in csv_list[1:]:
            if row[name_col_index[0]] in unique_value_list and row[name_col_index[0]] not in unique_used:
                records_unique_val.append(row)
                unique_used.append(row[name_col_index[0]])
            else:
                pass
        records_unique_val.insert(0, csv_list[0])
        value_list = records_unique_val
        return value_list


def csv_sort(csv_list, sort_col_name):
    """
    Sorts a csv by a column
    :param csv_list: csv that has been converted to a 2D list.
    :param sort_col_name: Name of column that will be sorted
    :return: sorted csv list
    """
    # stores header since they will be removed below
    csv_headers = [csv_list[0]]
    # indexes sort col
    sort_col = csv_headers[0].index(sort_col_name)
    # sorts csv list sans headers
    csv_sorted = sorted(csv_list[1:], key=lambda x: x[sort_col])
    # empties csvList so that headers and csvSorted can be re-added in order
    csv_list = []
    # appends headers
    for row in csv_headers:
        csv_list.append(row)
        # appends sorted csv rows
    for row in csv_sorted:
        csv_list.append(row)

    return csv_list


def attribute_filter(csv_list, target_value, target_col_name):
    """
    Filter a 2D table by a single value in a single column.

    :param csv_list: A 2D Table converted to a list
    :param target_value: The value that the list will be filtered to
    :param target_col_name: The column that the target_value will exist in
    :return: a filtered copy of in_list
    """
    headers = csv_list[0]
    target_col_index = headers.index(target_col_name)

    filtered_list = [headers]
    for row in csv_list:
        if str(row[target_col_index]) == str(target_value):
            filtered_list.append(row)

    return filtered_list


def left_join(p_table, f_table, p_key, f_key, insert_w_pkey=False):
    """
    Performs a left join between two 2D lists
    :param p_table: Primary table
    :param f_table: Foreign table
    :param p_key: Primary Key
    :param f_key: Foreign Key
    :param insert_w_pkey: False = append / True = insert without p_key
    :return: joined table as a 2D list
    """
    p_key_col = indexer(p_table[0], [p_key])[0]
    f_key_col = indexer(f_table[0], [f_key])[0]

    # holds joined table
    joined_table = []

    # joins headers
    joined_headers = p_table[0]
    field_count = 1
    for header in f_table[0]:
        # removes the fKey col header from appearing in final join
        if header != f_table[0][f_key_col]:
            if insert_w_pkey is False:
                joined_headers.append(header)
            if insert_w_pkey is True:
                joined_headers.insert(p_key_col + field_count, header)
            field_count += 1

    joined_table.append(joined_headers)
    # print(joinedHeaders)

    # only keeps first occurrence of f_key
    f_keys = []
    f_table_2 = []

    for row in f_table:
        if str(row[f_key_col]) not in f_keys:
            f_keys.append(str(row[f_key_col]))
            f_table_2.append(row)

    for pRow in p_table[1:]:
        key = str(pRow[p_key_col])
        joined_row = pRow

        for fRow in f_table_2[1:]:
            if str(fRow[f_key_col]) == key:
                cell_count = 0
                for cell in fRow:
                    # removes the fKey col from appearing in final join
                    if cell != fRow[f_key_col]:
                        if insert_w_pkey is False:
                            joined_row.append(cell)
                        if insert_w_pkey is True:
                            joined_row.insert(p_key_col + cell_count, cell)
                    cell_count += 1

        if key not in f_keys:
            if insert_w_pkey is False:
                joined_row.append("")
            if insert_w_pkey is True:
                joined_row.insert(p_key_col + 1, "")

        joined_table.append(joined_row)
    return joined_table
