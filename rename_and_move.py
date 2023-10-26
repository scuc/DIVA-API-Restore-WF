import logging
import logging.config
import os
import shutil

# import wordninja

from pathlib import Path

import config


config = config.get_config()
watch_folder = config["paths"]["watch_folder"]


logger = logging.getLogger(__name__)


# def fix_capitalization(obj_dict):
#     word_list = wordninja.split(obj_dict["FILENAME"])
#     print(word_list)


def rename_object(obj_dict):
    """
    Move a restored object out of the sub-dir tree and rename  with a proper file extension.
    """

    rename_msg = f"Begin obj rename and move for: {obj_dict['RURI']}"
    logger.info(rename_msg)

    # fix_capitalization(obj_dict)
    corrected_oc_name = obj_dict["OC_COMPONENT_NAME"].replace("\\", "/")
    corrected_oc_path = os.path.dirname(corrected_oc_name)

    filename = f"{obj_dict['AO_COMMENT']}_{obj_dict['FILENAME'][-18:]}"

    org_name = Path("/Volumes", obj_dict["volume"], watch_folder, corrected_oc_name)
    new_name = Path(
        "/Volumes",
        obj_dict["volume"],
        watch_folder,
        corrected_oc_path,
        filename,
    )

    try:
        org_name.rename(new_name)
        logger.info(f"File Renamed: {org_name.name} >> {new_name.name}")
        obj_dict.update({"renamed_path": new_name})

    except Exception as e:
        logger.error(f"Error renaming object: {e}")

    return obj_dict


def move_object(obj_dict):
    """
    Move and object into top level dir, if a object with the same name already exists in this location,
    append the file name.
    """
    count = 0
    while True:
        try:
            print(f"\nRENAMED PATH: {obj_dict['renamed_path']}\n")
            source_path = Path(
                "/Volumes", obj_dict["volume"], watch_folder, obj_dict["renamed_path"]
            )
            dest_path = Path(
                "/Volumes", obj_dict["volume"], "_Restore", obj_dict["renamed_path"]
            )

            if not dest_path.exists():
                shutil.move(source_path, dest_path)
            if dest_path.exists() and count < 2:
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
    move_object()
