import logging
import logging.config
import os
import sqlite3

import config
import check_obj_size as objsz

config = config.get_config()


logger = logging.getLogger(__name__)


def validate_object(volume=None, obj=None):
    """
    Ensure object is complete and can be found in the gorilla db.
    """

    size_value = objsz.check_obj_size(obj)
    if size_value != 2:
        logger.info(f"File size validation failed for: {obj}")
        return None
    else:
        obj_dict = check_db(os.path.basename(obj))
        return obj_dict


def check_db(obj):
    """
    example result from query:
    {
        GUID: 'FC15B4F7AB88-8000FFFF-FFFF-E582-F2F2',
        NAME: '61980_050380_SAVAGEKINGDOM_ARMYOFDARKNESS_25P_CTC_VM_WAV',
        DATATAPEID: '154149',
        SOURCECREATEDT: '5/1/18 15:10',
        CREATEDT: '5/1/18 15:14',
        LASTMDYDT: '5/2/18 16:28',
        RURI: 'FC15B4F7AB88-8000FFFF-FFFF-E5AD-D63E',
        TITLETYPE: 'archive',
        FILENAME: '61980_050380_SAVAGEKINGDOM_ARMYOFDARKNESS_25P_CTC_VM_WAV_20180501151000.zip',
        AO_COMMENT: '61980_050380_SavageKingdom_ArmyOfDarkness_25p_CTC_VM_WAV',
        OC_COMPONENT_NAME: 'mnt\\lun02\\Gorilla\\RuriStorage\\D6\\3E\\FC15B4F7AB88-8000FFFF-FFFF-E5AD-D63E',
     }
    """
    try:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        sql = """SELECT * FROM assets WHERE ruri = ?"""
        params = (str(obj),)
        row = cur.execute(sql, params).fetchone()
        conn.close()

        if row is not None:
            obj_dict = {
                "GUID": row[0],
                "NAME": row[1],
                "DATATAPEID": row[2],
                "SOURCECREATEDT": row[3],
                "CREATEDT": row[4],
                "LASTMDYDT": row[5],
                "RURI": row[6],
                "TITLETYPE": row[7],
                "FILENAME": row[8],
                "AO_COMMENT": row[9],
                "OC_COMPONENT_NAME": row[10],
            }

        else:
            obj_dict = None

        print(obj_dict)
        return obj_dict

    except Exception as e:
        conn_err_msg = f"Error on connection to database.db - {e}"
        logger.exception(conn_err_msg)


if __name__ == "__main__":
    check_db()
