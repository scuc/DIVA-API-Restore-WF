import logging
import logging.config
import os
from pathlib import Path

import config as cfg

logger = logging.getLogger(__name__)

config = cfg.get_config()
root_paths = config["paths"]["mac_root_path"]
watch_folder = config["paths"]["watch_folder"]


def check_watch_folders():
    obj_dict = {}
    for path in root_paths:
        if "video-research" not in path:
            volume_name = path.split("/")[2]
        else:
            volume_name = f"Quantum2/{path.split('/')[-2]}"
        p = Path(path, watch_folder)
        logger.info(f"Checking Path: {str(p.as_posix())}")
        restored_objs = [
            x for x in p.rglob("*") if x.is_file() and not x.name.startswith(".")
        ]
        if len(restored_objs) != 0:
            logger.info(f"{len(restored_objs)} new restored objects found.\n")
            obj_dict.update({volume_name: restored_objs})
        else:
            logger.info("No new objects in watchfolder.\n")
            continue

    return obj_dict


if __name__ == "__main__":
    check_watch_folders()
