import math
import os
import sys

from modules import sd_models, extras

S_WS = "Weighted sum"
S_AD = "Add difference"
S_SG = "Sigmoid"
choise_of_method = [S_WS, S_AD, S_SG]


class MergeRecipe():
    def __init__(self, A, B, C, O, M, S, F):
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

        self.A = A
        self.B = B
        self.C = C
        self.O = O
        self.S = self._adjust_method(method=S, model_C=C)
        self.M = self._adjust_multi_by_method(method=S, multi=M)
        self.F = (F == "True")

        self.vars = {}  # runtime variables

    def can_process(self):
        if self.A == "" or self.B == "" or self.A == None or self.B == None:
            return False
        if (self.C == "" or self.C == None) and self.S == S_AD:
            return False
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

    def run_merge(self, index):
        sd_models.list_models()

        print( "Starting merge under settings below,")
        print( "  A: {}".format(f"{self.A}" if self.A == self.row_A else f"{self.row_A} -> {self.A}"))
        print( "  B: {}".format(f"{self.B}" if self.B == self.row_B else f"{self.row_B} -> {self.B}"))
        print( "  C: {}".format(f"{self.C}" if self.C == self.row_C else f"{self.row_C} -> {self.C}"))
        print(f"  S: {self.S}")
        print(f"  M: {self.M}")
        print(f"  F: {self.F}")
        print(f"  O: {self.O}")

        try:
            results = extras.run_modelmerger(
                self.A,
                self.B,
                self.C,
                self.S,
                self.M,
                self.F,
                self.O
            )
        except Exception as e:
            print("Error loading/saving model file:", file=sys.stderr)
            sd_models.list_models()  # to remove the potentially missing models from the list
            return "Error: loading/saving model file. It doesn't exist or the name contains illegal characters"

        # update vars
        self._update_o_filename(index, results[0])

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
