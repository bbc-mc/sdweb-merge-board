import math
import os
import sys
import re

from modules import sd_models, extras, shared

from scripts.multimerge.util.merge_history import MergeHistory

S_WS = "Weighted sum"
S_AD = "Add difference"
S_SG = "Sigmoid"
choise_of_method = [S_WS, S_AD, S_SG]

mergeHistory = MergeHistory()


class MergeRecipe():
    def __init__(self, A, B, C, O, M, S, F:bool, CF):
        if C == None:
            C = ""
        if O == None:
            O = ""
        self.row_A = A
        self.row_B = B
        self.row_C = C
        self.row_O = O
        self.row_M = M
        self.row_S = S
        self.row_F = F
        self.row_CF = CF if CF in ["ckpt", "safetensors"] else "ckpt"

        self.A = A
        self.B = B
        self.C = C
        self.O = re.sub(r'[\\|/|:|?|.|"|<|>|\|\*]', '-', O)
        self.S = self._adjust_method(method=S, model_C=C)
        self.M = self._adjust_multi_by_method(method=S, multi=M)
        self.F = self.row_F
        self.CF = self.row_CF

        self.vars = {}  # runtime variables

    def can_process(self, index=0):
        if self.A == "" or self.B == "" or self.A == None or self.B == None:
            return False
        if (self.C == "" or self.C == None) and self.S == S_AD:
            return False
        if index > 0:
            # invalid var check
            # __O3__, line=4 => ok
            # __O3__, line=2 => error
            pass
        return True

    def apply_variables(self, _vars:dict):
        def _apply(_param, _vars):
            if not _param or _param == "":
                return _param
            if _param in _vars.keys():
                _var = _vars.get(_param)  # i.e. self.row_A = __O1__, _vars["__O1__"] = _var = "xxxx.ckpt"
                if _var and _var != "":
                    return sd_models.get_closet_checkpoint_match(_var).title
            return _param
        self.A = _apply(self.row_A, _vars)
        self.B = _apply(self.row_B, _vars)
        self.C = _apply(self.row_C, _vars)

    def run_merge(self, index, skip_merge_if_exists, config_source):
        sd_models.list_models()
        if skip_merge_if_exists:
            _filename = self.O + "." + self.CF if self.O != "" else self._estimate_ckpt_name()
            if self._check_ckpt_exists(_filename):
                # exists
                _result = f"Checkpoint already exist: {_filename}"
                print(f"Merge skipped. Same name checkpoint already exists.")
                print(f"  O: {_filename}")
                self._update_o_filename(index, _result)
                return [f"[skipped] {_filename}", f"[skipped] {_filename}"]

        print( "Starting merge under settings below,")
        print( "  A: {}".format(f"{self.A}" if self.A == self.row_A else f"{self.row_A} -> {self.A}"))
        print( "  B: {}".format(f"{self.B}" if self.B == self.row_B else f"{self.row_B} -> {self.B}"))
        print( "  C: {}".format(f"{self.C}" if self.C == self.row_C else f"{self.row_C} -> {self.C}"))
        print(f"  S: {self.S}")
        print(f"  M: {self.M}")
        print(f"  F: {self.F}")
        print( "  O: {}".format(f"{self.O}" if self.O != "" else f" -> {self._estimate_ckpt_name()}"))
        print(f" CF: {self.CF}")

        try:
            results = extras.run_modelmerger(self.A, self.B, self.C, self.S, self.M, self.F, self.O, self.CF, config_source)
        except TypeError:
            # backward compatibility for change of run_modelmerger
            # 2023/01/11
            # https://github.com/AUTOMATIC1111/stable-diffusion-webui/commit/954091697fce7a1b7997d5f3d73551f793f6bebc
            print("Try to use old 'run_modelmerger' params. 'config_source' is ignored")
            try:
                results = extras.run_modelmerger(self.A, self.B, self.C, self.S, self.M, self.F, self.O, self.CF)
            except TypeError as te:
                # backward compatibility for change of run_modelmerger
                # 2022/11/27
                # https://github.com/AUTOMATIC1111/stable-diffusion-webui/commit/dac9b6f15de5e675053d9490a20e0457dcd1a23e/modules/extras.py#L253
                print("Try to use old 'run_modelmerger' params. 'Checkpoint format is forced to 'ckpt'")
                try:
                    results = extras.run_modelmerger(self.A, self.B, self.C, self.S, self.M, self.F, self.O)
                except Exception as e:
                    print(type(e))
                    print(e)
                    return ["Error", "Error"]
            except Exception as e:
                print("Error: at recipe.run_merge: ", file=sys.stderr)
                print(type(e), file=sys.stderr)
                print(e, file=sys.stderr)
                sd_models.list_models()  # to remove the potentially missing models from the list

                # try to figure out whats going on
                def _dprint_model_exists(header, model):
                    if model != "" and sd_models.get_closet_checkpoint_match(model) is not None:
                        if os.path.exists(sd_models.get_closet_checkpoint_match(model).filename):
                            print("  {}: is exists:True  [{}]".format(header, model), file=sys.stderr)
                        else:
                            print("  {}: is exists:False [{}]".format(header, model), file=sys.stderr)
                    else:
                        print("  {}: not found:   [{}]".format(header, model), file=sys.stderr)
                _dprint_model_exists("A", self.A)
                _dprint_model_exists("B", self.B)
                _dprint_model_exists("C", self.C)

                return ["Error: at recipe.run_merge. "] *2

        except Exception as e:
            print(e)

        # update vars
        self._update_o_filename(index, results[0])

        # save log
        mergeHistory.add_history(
            self.A,
            self.B,
            self.C,
            self.S,
            self.M,
            self.F,
            self.O,
            self.CF,
            index)

        #
        return [f"Merge complete. Checkpoint saved as: [{self.O}]", self.O]


    def get_vars(self):
        return self.vars

    #
    # local func
    #
    def _update_o_filename(self, index, results):
        """
        update self.O and vars {"__Ox__": self.O}
        """
        # Checkpoint saved to " + output_modelname
        ckpt_name = " ".join(results.split(" ")[3:])
        ckpt_name = os.path.basename(ckpt_name)  # expect aaaa.ckpt
        ckpt_name = sd_models.get_closet_checkpoint_match(ckpt_name).title
        # update
        self.O = ckpt_name
        self.vars.update({f"__O{index}__": ckpt_name})

    def _adjust_method(self, method, model_C):
        if method == S_SG:
            return S_WS
        if model_C == None or model_C == "":
            return S_WS
        return method

    def _adjust_multi_by_method(self, method, multi):
        if method == S_SG:
            multi = self._alpha_of_inv_sigmoid(multi)
        else:
            multi = multi
        return multi

    def _alpha_of_weighted_sum(self, alpha):
        """
        Weighted sum
            (1-alpha)*theta0 + alpha * theta1
          = theta0 + (theta1 - theta0) * alpha
        """
        return alpha

    def _alpha_of_sigmoid(self, alpha):
        alpha = float(alpha)
        return alpha * alpha * (3 - (2 * alpha))

    def _alpha_of_inv_sigmoid(self, alpha):
        alpha = float(alpha)
        return 0.5 - math.sin(math.asin(1.0 - 2.0 * alpha) / 3.0)

    def _check_ckpt_exists(self, _O):
        ckpt_dir = shared.cmd_opts.ckpt_dir or sd_models.model_path
        output_modelname = os.path.join(ckpt_dir, _O)
        if os.path.exists(ckpt_dir) and os.path.exists(output_modelname) and os.path.isfile(output_modelname):
            return True
        else:
            return False

    def _estimate_ckpt_name(self):
        _A = sd_models.get_closet_checkpoint_match(self.A)
        _B = sd_models.get_closet_checkpoint_match(self.B)
        _M = self.M
        _S = self.S
        _CF = self.CF

        # File name generation code from
        #
        # AUTO 685f963
        # modules/extras.py
        # def run_modelmerger
        # L314
        _filename = \
        _A.model_name + '_' + str(round(1-_M, 2)) + '-' + \
        _B.model_name + '_' + str(round(_M, 2)) + '-' + \
        _S.replace(" ", "_") + \
        '-merged.' +  \
        _CF
        return _filename
