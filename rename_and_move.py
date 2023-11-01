import logging
import logging.config
import os
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

    rename_msg = f"Begin obj rename and move for: {obj_dict['RURI']}"
    logger.info(rename_msg)

    # full gorilla path with the objectname
    corrected_oc_name = obj_dict["OC_COMPONENT_NAME"].replace("\\", "/")

    # full gorilla path, without the object name
    corrected_oc_path = corrected_oc_name.split("/")[-3:]

    filename = f"{obj_dict['AO_COMMENT']}_{obj_dict['FILENAME'][-18:]}"

    org_name = Path(
        "/Volumes",
        obj_dict["volume"],
        watch_folder,
        corrected_oc_path[0],
        corrected_oc_path[1],
        obj_dict["RURI"],
    )

    new_path_name = Path(
        "/Volumes",
        obj_dict["volume"],
        watch_folder,
        corrected_oc_path[0],
        corrected_oc_path[1],
        filename,
    )

    try:
        org_name.rename(new_path_name)
        logger.info(f"File Renamed: {org_name.name} >> {new_path_name.name}")
        obj_dict.update({"renamed_path": new_path_name})

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
            source_path = Path(obj_dict["renamed_path"])
            dest_path = Path(
                "/Volumes",
                obj_dict["volume"],
                "__Restore",
                obj_dict["renamed_path"].name,
            )

            if not dest_path.exists():
                shutil.move(source_path, dest_path)
                logger.info(
                    f"File moved into: \
                    {os.path.join('/Volumes', obj_dict['volume'], '__Restore')}"
                )
                break
            if dest_path.exists() and count < 2:
                count += 1
                source_name = source_path.name
                name_check = source_name.split(".")

                # append the filename with _{count} to avoid overwritting duplicates
                if name_check[0].endswith("_" + str(count)):
                    new_source_name = source_name.replace(".", f"_{count + 1}.", 1)
                else:
                    new_source_name = name_check[0] + f"_{count}"

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
