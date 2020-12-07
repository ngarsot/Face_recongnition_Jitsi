import io
import os
import sqlite3

import numpy as np

from src.jitsi_app.constants import DB, DB_TABLE_NAME


# GENERIC FUNCTIONS
def adapt_array(arr):
    """
    Converts from numpy array to bytes in order to be loaded into the DB.
    """

    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    """
    Converts from bytes to numpy array when dumped from the DB.
    """

    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)

# GENERIC FUNCTIONS ==================================


def get_rows(db=DB):
    """
    Returns the all rows from the specific DB.

    :param db: str --> db path
    :return: In case of existing the DB, it returns a list of all db rows. Otherwise, None.
    """

    if os.path.isfile(db):
        with sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES) as db_conn:
            cur = db_conn.cursor()
            cur.execute(f"select * from {DB_TABLE_NAME}")
            return cur.fetchall()
    else:
        return None

# ==================================================
# ========== TO CREATE AND TO FILL THE DB ==========
# ==================================================
'''
if __name__ == '__main__':
    import pandas as pd

    from src.face_comparison.face_comparison_db import FaceComparisonDB
    
    # Edit it
    add_encodings_from_dir = True
    
    # DIR where to get the images to encoding and to load into the DB
    DATA_LOCATION_PATH = '../test_data/db/'
    
    # Edit it ==================================

    is_not_db_created = True if not os.path.isfile(DB) else False
    with sqlite3.connect(DB, detect_types=sqlite3.PARSE_DECLTYPES) as db_conn:
        if is_not_db_created:
            print(f'Database created in {DB_LOCATION_PATH} as {DB_NAME} (Full path --> {DB})')
            db_conn.execute(f"CREATE TABLE {DB_TABLE_NAME}(id integer primary key, name text, encoding array)")
            print(f'Table created --> {DB_TABLE_NAME}')

        if add_encodings_from_dir:
            obj_face_comp_db = FaceComparisonDB()
            for photo in os.listdir(DATA_LOCATION_PATH):
                photo_path = os.path.join(DATA_LOCATION_PATH, photo)
                obj_face_comp_db.encoding_unknown(image_path=photo_path)
                name_and_encodings = (obj_face_comp_db.unknown_name, obj_face_comp_db.unknown_encoding[0])
                db_conn.execute("INSERT INTO " + DB_TABLE_NAME + " VALUES (NULL, ?, ?)", name_and_encodings)

        # Create a dataframe table with pandas
        # table = pd.read_sql_query(f"SELECT * from {DB_TABLE_NAME}", db_conn)
        # print(table)

        cur = db_conn.cursor()
        cur.execute(f"select * from {DB_TABLE_NAME}")
        rows = cur.fetchall()
        for row in rows:
            print(row)
'''