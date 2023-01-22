#
#
#
import os
import datetime
from csv import DictWriter, DictReader
import shutil

from modules import scripts


CSV_FILE_ROOT = "csv/"
CSV_FILE_PATH = "csv/history.tsv"
HEADERS = [
    "model_O", "model_O_hash", "model_O_sha256",
    "model_A", "model_A_hash", "model_A_sha256",
    "model_B", "model_B_hash", "model_B_sha256",
    "model_C", "model_C_hash", "model_C_sha256",
    "multiplier", "interpolation_method", "save_as_float16", "checkpoint_format", "lane_index", "datetime",
    ]
path_root = scripts.basedir()


class MergeHistory():
    def __init__(self):
        self.fileroot = os.path.join(path_root, CSV_FILE_ROOT)
        self.filepath = os.path.join(path_root, CSV_FILE_PATH)
        if not os.path.exists(self.fileroot):
            os.mkdir(self.fileroot)
        if os.path.exists(self.filepath):
            self.update_header()

    def add_history(self,
                model_A_name, model_A_hash, model_A_sha256,
                model_B_name, model_B_hash, model_B_sha256,
                model_C_name, model_C_hash, model_C_sha256,
                model_O_name, model_O_hash, model_O_sha256,
                S, M, F, CF, index):

        _history_dict = {
            "model_O": model_O_name,
            "model_O_hash": model_O_hash,
            "model_O_sha256": model_O_sha256,
            "model_A": model_A_name,
            "model_A_hash": model_A_hash,
            "model_A_sha256": model_A_sha256,
            "model_B": model_B_name,
            "model_B_hash": model_B_hash,
            "model_B_sha256": model_B_sha256,
            "model_C": model_C_name,
            "model_C_hash": model_C_hash,
            "model_C_sha256": model_C_sha256,
            "multiplier": f"{M}",
            "interpolation_method": f"{S}",
            "save_as_float16": f"{F}",
            "checkpoint_format": f"{CF}",
            "lane_index": index,
            "datetime": f"{datetime.datetime.now()}"
        }

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                dw = DictWriter(f, fieldnames=HEADERS, delimiter='\t')
                dw.writeheader()
        # save to file
        with open(self.filepath, "a", newline="", encoding='utf-8') as f:
            dw = DictWriter(f, fieldnames=HEADERS, delimiter='\t')
            dw.writerow(_history_dict)

    def update_header(self):
        hist_data = []
        if os.path.exists(self.filepath):
            # check header in case HEADERS updated
            with open(self.filepath, "r", newline="", encoding="utf-8") as f:
                dr = DictReader(f, delimiter='\t')
                if dr.fieldnames:
                    new_header = [ x for x in HEADERS if x not in dr.fieldnames ]
                    if len(new_header) > 0:
                        # need update.
                        hist_data = [ x for x in dr]
            if len(hist_data) > 0:
                # backup before change
                shutil.copy(self.filepath, self.filepath + ".bak")
                with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                    dw = DictWriter(f, fieldnames=HEADERS, delimiter='\t')
                    dw.writeheader()
                    dw.writerows(hist_data)
