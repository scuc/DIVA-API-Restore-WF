import logging
import logging.config
import shutil

from pathlib import Path

import config


config = config.get_config()
watch_folder = config["paths"]["watch_folder"]


logger = logging.getLogger(__name__)


def rename_object(obj_dict):
    """
    Move a restored object out of the sub-dir tree and rename  with a proper file extension.
    """

    rename_msg = f"Begin obj rename and move for: {obj_dict['ruri']}"
    logger.info(rename_msg)

    org_name = Path(obj_dict["volume"], watch_folder, obj_dict["oc_component_name"])
    new_name = Path(obj_dict["volume"], watch_folder, obj_dict["filename"])

    try:
        org_name.rename(new_name)
        logger.info(f"File Renamed: {org_name.name} >> {new_name.name}")

    except Exception as e:
        logger.error(f"Error renaming object: {e}")

    return


def move_object(obj_dict):
    """
    Move and object into top level dir, if a object with the same name already exists in this location,
    append the file name.
    """
    count = 0
    while True:
        try:
            source_path = Path(obj_dict["volume"], watch_folder, obj_dict["filename"])
            dest_path = Path(obj_dict["volume"], "_Restore", obj_dict["filename"])

            if not dest_path.exists():
                shutil.move(source_path, dest_path)
            if dest_path.exists() and count < 5:
                count += 1
                source_name = source_path.name
                name_check = source_name.split(".")

                if name_check[0].endswith("_" + str(count)):
                    new_source_name = source_name[:] + f"_{count + 1}"
                else:
                    new_source_name = name_check + f"_{count}"

                source_path = source_path.rename(
                    Path(source_path.parent, new_source_name)
                )
                continue
            else:
                logger.info(
                    f"Too many copies of {source_path.name} exist in destination path."
                )
            return

        except Exception as e:
            logger.error(f"Error moving object: {e}")
            return


if __name__ == "__main__":
    move_object(
        # Path("/Users/cucos001/Desktop/Gorilla_CSV_WatchFolder/FC15B4F7AB88-80001000-0000-257D-6F2A.csv "),
        # Path("/Users/cucos001/Desktop/Gorilla_CSV_WatchFolder/_DONE")
        # fileName="056957_WONDERFULLYWEIRD_SUPERFREAKS_EM_WAV_20170216093000.zip",
        # objectName="FC15B4F7AB88-8000FFFF-FFFF-ECE8-39D0",
        # folderPath="/Volumes/Quantum2/DaletStorage/Gorilla_DIVA_Restore/mnt/lun02/Gorilla/RuriStorage/69/42/FC15B4F7AB88-8000FFFF-FFFF-ED3C-6942"
    )
