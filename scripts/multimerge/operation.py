from scripts.multimerge.recipe import MergeRecipe


class MergeOperation:
    def __init__(self):
        self.recipes = {}

    def can_process(self):
        _ret = True
        for _index, _recipe in self.recipes.items():
            _recipe:MergeRecipe = _recipe
            _ret = _ret and _recipe.can_process()
        return _ret

    def add_merge(self, index, A, B, C, M, S, F, O, CF):
        if index and index != "" and index >= 0:
            _recipe = MergeRecipe(A, B, C, O, M, S, F, CF)
            if _recipe.can_process():
                self.recipes.update({index: _recipe})

    def get_process_num(self):
        return len(self.recipes)

    def run_merge(self, skip_merge_if_exists=False):
        _ret_all = []
        _vars = {}  # {"__A1__": "sd-v1-5-pruned.ckpt"}
        for _index, _recipe in self.recipes.items():
            _recipe:MergeRecipe = _recipe
            # apply current variables
            _recipe.apply_variables(_vars)
            # run merge
            _ret = _recipe.run_merge(_index, skip_merge_if_exists)
            _ret_all.append(_ret)
            # update vars
            _vars.update(_recipe.get_vars())
        return _ret_all  # _ret message list
