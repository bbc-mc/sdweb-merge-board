#
#
#
import os
import datetime
from csv import DictWriter, DictReader

from modules import scripts, sd_models


CSV_FILE_PATH = "csv/history.tsv"
HEADERS = [
    "model_O", "model_O_hash", "model_A", "model_A_hash", "model_B", "model_B_hash", "model_C", "model_C_hash",
    "multiplier", "interpolation_method", "save_as_float16", "checkpoint_format", "lane_index", "datetime",
    ]
path_root = scripts.basedir()


class MergeHistory():

    def __init__(self):
        self.filepath = os.path.join(path_root, CSV_FILE_PATH)
        if os.path.exists(self.filepath):
            self.update_header()

    def add_history(self, A, B, C, S, M, F, O, CF, index):
        def _update_model_data(_dict, M, header=""):
            if M is not None and M != "" and header != "":
                _m = sd_models.get_closet_checkpoint_match(M)
                _dict.update({
                    f"model_{header}": os.path.basename(_m.filename),
                    f"model_{header}_hash": _m.hash
                    })

        _history_dict = {}
        _update_model_data(_history_dict, A, "A")
        _update_model_data(_history_dict, B, "B")
        _update_model_data(_history_dict, C, "C")
        _update_model_data(_history_dict, O, "O")
        _history_dict.update({"interpolation_method": f"{S}"})
        _history_dict.update({"multiplier": f"{M}"})
        _history_dict.update({"save_as_float16": f"{F}"})
        _history_dict.update({"checkpoint_format": f"{CF}"})
        _history_dict.update({"lane_index": index})
        _history_dict.update({"datetime": f"{datetime.datetime.now()}"})

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
                with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                    dw = DictWriter(f, fieldnames=HEADERS, delimiter='\t')
                    dw.writeheader()
                    dw.writerows(hist_data)
