import logging
import logging.config
import os
import yaml

from collections import Counter
from datetime import datetime

from time import localtime, strftime

import config
import check_restore_dir as objs
import rename_and_move as renmv
import validate_obj as valobj


config = config.get_config()

logging_config = config["paths"]["logging_config"]


logger = logging.getLogger(__name__)


def set_logger():
    """
    Setup logging configuration
    """

    with open(logging_config, "rt") as f:
        config = yaml.safe_load(f.read())

        # get the file name from the handlers, append the date to the filename.
        for i in config["handlers"].keys():
            # local_datetime = str(strftime("%A, %d. %B %Y %I:%M%p", localtime()))

            if "filename" in config["handlers"][i]:
                log_filename = config["handlers"][i]["filename"]
                base, extension = os.path.splitext(log_filename)
                today = datetime.today()

                log_filename = "{}_{}{}".format(
                    base, today.strftime("%Y%m%d%H%M%S"), extension
                )
                config["handlers"][i]["filename"] = log_filename
            else:
                continue

        logger = logging.config.dictConfig(config)

    return logger


def main():
    start_message()

    object_dict = objs.check_watch_folders()

    summary = Counter(
        {
            "Quantum1": 0,
            "Quantum2": 0,
            "Quantum3": 0,
            "Quantum4": 0,
            "Isilon2": 0,
        }
    )

    if len(object_dict) != 0:
        for key, value in object_dict.items():
            for obj in value:
                obj_dict = valobj.validate_object(volume=key, obj=obj)
                if obj_dict is not None:
                    obj_dict.update({"volume": key})
                    object_dict = renmv.rename_object(obj_dict)
                    renmv.move_object(obj_dict)
                    summary.update(key)
                else:
                    logger.info(f"object id not found in the DB - {obj}")

    else:
        logger.info("No new Gorilla Objects found.")
        pass

    complete_message(summary)


def start_message():
    date_start = str(strftime("%A, %d. %B %Y %I:%M%p", localtime()))

    start_msg = f"\n\
    ================================================================\n\
                DIVA Restore WatchFolder - Start\n\
                    {date_start}\n\
    ================================================================\n\
   "
    logger.info(start_msg)


def complete_message(summary):
    date_end = str(strftime("%A, %d. %B %Y %I:%M%p", localtime()))

    complete_msg = f"\n\
    ================================================================\n\
                DIVA Restore WatchFolder - Complete\n\
                    {date_end}\n\
                    {[print(f'{key}:{value}') for key, value in summary.items()]}\n\
    ================================================================\n\
    "
    logger.info(complete_msg)
    return


if __name__ == "__main__":
    set_logger()
    main()
