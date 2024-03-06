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

    # full gorilla path with the objectname, backslashes replaced
    corrected_oc_name = obj_dict["OC_COMPONENT_NAME"].replace("\\", "/")
    print(f"CORRECTED OC NAME: {corrected_oc_name}")

    # full list gorilla path components, without the object name
    oc_path_list = corrected_oc_name.split("/")[-6:]
    print(f"OC PATH LIST: {oc_path_list}")

    filename = f"{obj_dict['AO_COMMENT']}_{obj_dict['FILENAME'][-18:]}"

    print(f"OBJ DICT AO COMMENT: {obj_dict['AO_COMMENT']}")
    print(f"OBJ DICT FILENAME: {obj_dict['FILENAME']}")
    print(f"FILENAME: {filename}")

    oc_path = "/".join(oc_path_list[:6])
    new_oc_path = "/".join(oc_path_list[:5])

    org_path_name = Path(
        "/Volumes",
        obj_dict["volume"],
        watch_folder,
        oc_path,
    )

    new_path_name = Path(
        "/Volumes",
        obj_dict["volume"],
        watch_folder,
        new_oc_path,
        filename,
    )

    print(f"ORG PATH NAME: {org_path_name}")
    print(f"NEW PATH NAME: {new_path_name}")

    try:
        org_path_name.rename(new_path_name)
        logger.info(f"File Renamed: {org_path_name.name} >> {new_path_name.name}")
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
                f"File moved into: {os.path.join('/Volumes', obj_dict['volume'], '__Restore', obj_dict['FILENAME'])}"
            )
        else:
            count += 1
            source_name = source_path.name
            name_check = source_name.split(".")

            # append the filename with _{count} to avoid overwritting duplicates
            if name_check[0].endswith("_" + str(count)):
                new_source_name = source_name.replace(f"_{count}.", f"_{count + 1}.", 1)
            else:
                new_source_name = name_check[0] + f"_{count}." + name_check[-1]

            source_path = source_path.rename(Path(source_path.parent, new_source_name))

        return

    except Exception as e:
        logger.error(f"Error moving object: {e}")
        return


if __name__ == "__main__":
    move_object()
