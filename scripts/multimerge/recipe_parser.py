import re
import os

import gradio as gr

from modules import sd_models

from scripts.multimerge.recipe import MergeRecipe, S_WS, S_AD, S_SG

class RecipeParser():
    def __init__(self, txt_recipe=None):
        self.recipes = {}
        self.vars_system = {}
        self.vars_user = {}
        self.vars_txt = {}
        if txt_recipe and txt_recipe != "":
            self.txt_recipe = txt_recipe
            # self.recipes = {}  # {"1": recipe_1}
            self.recipes, self.vars_system, self.vars_user, self.vars_txt = self._parse_recipe(self.txt_recipe)

    def send_to_recipe(self, A, B, C, O, M, S, F, CF):
        def _get_modelname(X):
            if X and X != "":
                _model = sd_models.get_closet_checkpoint_match(X)
                if _model:
                    return os.path.splitext(os.path.basename(_model.filename))[0]
            return X

        _recipe = MergeRecipe(A, B, C, O, M, S, F, CF)
        if _recipe.can_process():
            _index = len(self.recipes) + 1
            if re.search("__[O]{1}\d+__", _recipe.A):
                self.vars_system.update({_recipe.A:""})
            else:
                _recipe.A = _get_modelname(_recipe.A)
            if re.search("__[O]{1}\d+__", _recipe.B):
                self.vars_system.update({_recipe.B:""})
            else:
                _recipe.B = _get_modelname(_recipe.B)
            if _recipe.C and _recipe.C != "" and re.search("__[O]{1}\d+__", _recipe.C):
                self.vars_system.update({_recipe.C:""})
            else:
                _recipe.C = _get_modelname(_recipe.C)
            self.recipes.update({_index: _recipe})

    def output_txt(self):
        _ret = "# Recipe \n"
        for _recipe in self.recipes.values():
            _recipe:MergeRecipe = _recipe
            if _recipe.C and _recipe.S == S_AD :
                _ret += f"{_recipe.O} = {_recipe.A} + {_recipe.B} + {_recipe.C}, {_recipe.M}"
            else:
                _ret += f"{_recipe.O} = {_recipe.A} + {_recipe.B}, {_recipe.M}"
            if _recipe.F:
                _ret += ", fp16"
            if _recipe.CF:
                _ret += f", {_recipe.CF}"
            _ret += "\n"
        #
        _ret += "\n# Variables(System) \n"
        for _item in self.vars_system.keys():
            _ret += f"{_item}" + "\n"
        #
        _ret += "\n# Variables(User defined) \n"
        for _item in self.vars_user.keys():
            _ret += f"{_item}" + "\n"
        return _ret

    def _parse_recipe(self, _txt_recipe):

        def _dispatch_recipe(_line_recipe):
            _O = _line_recipe.strip().split("=")[0].strip()
            _A = _line_recipe.strip().split('=')[1].strip().split(',')[0].strip().split('+')[0].strip()
            _B = _line_recipe.strip().split('=')[1].strip().split(",")[0].strip().split("+")[1].strip()
            try:
                _C = _line_recipe.strip().split("=")[1].strip().split(",")[0].strip().split("+")[2].strip()
            except:
                _C = None
            _M = _line_recipe.strip().split("=")[1].split(",")[1]
            try:
                _F = True if "fp16" in [x.strip() for x in _line_recipe.strip().split("=")[1].split(",")[2:]] else False
            except:
                _F = False
            try:
                _CF = "safetensors" if "safetensors" in [x.strip() for x in _line_recipe.strip().split("=")[1].split(",")[2:]] else "ckpt"
            except:
                _CF = "ckpt"

            if not _C:
                _S = S_WS
            else:
                _S = S_AD

            _ret = {"A": _A, "B": _B, "C": _C, "O": _O, "M": _M, "F": _F, "S": _S, "CF": _CF}

            # check vals
            _vars_system = {}
            _vars_user = {}
            for value in _ret.values():
                try:
                    if value and len(value.strip().split("__")) > 2:
                        if re.search("__[O]{1}\d+__", value):
                            _vars_system.update({value:""})
                        else:
                            _vars_user.update({value:""})
                except:
                    pass
            _ret_recipe = MergeRecipe(_A, _B, _C, _O, _M, _S, _F, _CF)
            return _ret_recipe, _vars_system, _vars_user

        def _dispatch_variable(_line_variable):
            _ret = _line_variable.split("__")
            _note = _line_variable.split(",")
            if len(_ret) > 1:
                _ret = _ret[1]
            else:
                return None
            if len(_note) > 1:
                _note = _note[1]
            else:
                return None
            if _ret and _note:
                return {f"__{_ret}__":_note}
            else:
                return None

        _recipes = {}      # {"1": <MergeRecipe>}
        _vars_system = {}  # {"__O1__": ""}   # variable in recipe
        _vars_user = {}    # {"__SD15__": ""} # variable in recipe
        _vars_txt = {}    # {"__SD15__": "comments or suggestion for this variables."}
        index = 1
        for _line in _txt_recipe.split("\n"):
            if index > 10:
                print(f"  ignored: {_line}")
                continue
            _ret = ""
            _line = _line.strip()
            # ignore lines start with "#", None, empty.
            if _line == None or _line == "" or _line[0] == "#":
                continue
            # ignore in-line comment
            _line = _line.split("#")[0]

            # Recipe
            # O1 = A1 + B1, 0.1
            # O2 = A2 + B2 + C2, 0.2
            # O3 = A3 + __O1__, 0.3
            # O4 = A4 + __SD15__, 0.4
            # O5 = A5 + B5, 0.5, fp16
            # Variables
            # __SD15__, put your sd1.5.
            if _line.strip()[0] == "_":
                _ret = _dispatch_variable(_line)
                if _ret:
                    _vars_txt.update(_ret)
            else:
                _ret_recipe, _ret_vars_system, _ret_vars_user = _dispatch_recipe(_line)
                if _ret_recipe:
                    _recipes.update({f"{index}": _ret_recipe})
                if _ret_vars_system:
                    _vars_system.update(_ret_vars_system)
                if _ret_vars_user:
                    _vars_user.update(_ret_vars_user)
                index += 1

            if index > 10:
                print(f"Warning: text line num for recipe over 10. Rest of txt ignored.")
                continue

        return _recipes, _vars_system, _vars_user, _vars_txt

    # UI output for UI:Recipe
    def output_grupdate_uirecipe(self, grs: list):
        _vars = self.vars_user
        _ret = []
        for _var_name in _vars.keys():
            if _var_name and _var_name != "":
                _ret += [gr.update(visible=True), gr.update(value=_var_name, visible=True), gr.update(visible=True)]
            else:
                _ret += [gr.update(visible=False), gr.update(value="", visible=False), gr.update(value="", visible=False)]
        _ret += [gr.update(visible=False)] * (len(grs) - len(_vars)*3)
        return _ret

    # UI output for UI:Merge board
    def output_grupdate_uimerge(self):
        """
            update gr in UI:Multi-Merge
                A1, B1, C1, M1, S1, F1, O1, CF1,
                A2, B2, C2, M2, S2, F2, O2, CF2,
                A3, B3, C3, M3, S3, F3, O3, CF3,
                A4, B4, C4, M4, S4, F4, O4, CF4,
                A5, B5, C5, M5, S5, F5, O5, CF5,
                A6, B6, C6, M6, S6, F6, O6, CF6,
                A7, B7, C7, M7, S7, F7, O7, CF7,
                A8, B8, C8, M8, S8, F8, O8, CF8,
                A9, B9, C9, M9, S9, F9, O9, CF9,
                A10,B10,C10,M10,S10,F10,O10,CF10
        """
        def _get_model_title(X):
            if X and X != "" and X != None:
                _model = sd_models.get_closet_checkpoint_match(X)
                if _model:
                    return _model.title
            return X

        _ret_all = []
        index = 0
        for _recipe in self.recipes.values():
            _recipe:MergeRecipe = _recipe
            _ret = []
            _ret.append(gr.update(value=_get_model_title(_recipe.A)))
            _ret.append(gr.update(value=_get_model_title(_recipe.B)))
            _ret.append(gr.update(value=_get_model_title(_recipe.C)))
            _ret.append(gr.update(value=float(_recipe.M)))
            _ret.append(gr.update(value=_recipe.S))
            _ret.append(gr.update(value=_recipe.F))
            _ret.append(gr.update(value=_recipe.O))
            _ret.append(gr.update(value=_recipe.CF))
            _ret_all += _ret
            index += 1
        for i in range(index, 10):
            _ret = [None,None,None,None,None,None,None,None]
            _ret_all += _ret
        return _ret_all

    def apply_vars(self, vars:dict):
        for _recipe in self.recipes.values():
            _recipe:MergeRecipe = _recipe
            _recipe.apply_variables(vars)
