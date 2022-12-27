# Merge Board
#
# extension of AUTOMATIC1111 web ui
#
# 2022/11/06 bbc_mc
#

from collections import namedtuple

import gradio as gr
from modules import scripts, script_callbacks
from modules import sd_models

from scripts.multimerge import ui_merge, ui_recipe, ui_models
from scripts.multimerge.operation import MergeOperation
from scripts.multimerge.recipe_parser import RecipeParser
from scripts.multimerge.recipe import MergeRecipe

path_root = scripts.basedir()

#
# UI callback
#
def on_ui_tabs():

    with gr.Blocks() as main_block:

        #UI:Multi-Merge
        btn_run_merge, btn_reload_checkpoints, btn_send_to_recipe, submit_result, btn_clear_merge_settings, \
        A1, B1, C1, M1, S1, F1, O1, CF1, \
        A2, B2, C2, M2, S2, F2, O2, CF2, \
        A3, B3, C3, M3, S3, F3, O3, CF3, \
        A4, B4, C4, M4, S4, F4, O4, CF4, \
        A5, B5, C5, M5, S5, F5, O5, CF5, \
        A6, B6, C6, M6, S6, F6, O6, CF6, \
        A7, B7, C7, M7, S7, F7, O7, CF7, \
        A8, B8, C8, M8, S8, F8, O8, CF8, \
        A9, B9, C9, M9, S9, F9, O9, CF9, \
        A10,B10,C10,M10,S10,F10,O10,CF10, \
        _checkpoint_listener, chk_skip_merge_if_exists = ui_merge.on_ui_tabs()

        # UI:Recipe
        txt_recipe, txt_parse_result, btn_send_recipe_to_multi_merge, \
        row_01, txt_vars_01, drp_vars_01, \
        row_02, txt_vars_02, drp_vars_02, \
        row_03, txt_vars_03, drp_vars_03, \
        row_04, txt_vars_04, drp_vars_04, \
        row_05, txt_vars_05, drp_vars_05, \
        row_06, txt_vars_06, drp_vars_06, \
        row_07, txt_vars_07, drp_vars_07, \
        row_08, txt_vars_08, drp_vars_08, \
        row_09, txt_vars_09, drp_vars_09, \
        row_10, txt_vars_10, drp_vars_10, \
        row_11, txt_vars_11, drp_vars_11, \
        row_12, txt_vars_12, drp_vars_12, \
        row_13, txt_vars_13, drp_vars_13, \
        row_14, txt_vars_14, drp_vars_14, \
        row_15, txt_vars_15, drp_vars_15, \
        row_16, txt_vars_16, drp_vars_16, \
        row_17, txt_vars_17, drp_vars_17, \
        row_18, txt_vars_18, drp_vars_18, \
        row_19, txt_vars_19, drp_vars_19, \
        row_20, txt_vars_20, drp_vars_20 \
        = ui_recipe.on_ui_tabs()

        # UI:Models
        ui_models.on_ui_tabs()

        # Footer
        gr.HTML(
            """
            <p style="font-size: 12px" align="right">
            <b>Multi Model Merge</b> extension by <a href="https://github.com/bbc-mc" target="_blank">bbc_mc</a><br />
            For <a href="https://github.com/AUTOMATIC1111/stable-diffusion-webui" target="_blank">stable-diffusion-webui</a> by AUTOMATIC1111<br />
            License: MIT
            </p>
            """
        )

        #
        # Vars of recipe
        #
        vars_list = [
            txt_vars_01, drp_vars_01,
            txt_vars_02, drp_vars_02,
            txt_vars_03, drp_vars_03,
            txt_vars_04, drp_vars_04,
            txt_vars_05, drp_vars_05,
            txt_vars_06, drp_vars_06,
            txt_vars_07, drp_vars_07,
            txt_vars_08, drp_vars_08,
            txt_vars_09, drp_vars_09,
            txt_vars_10, drp_vars_10,
            txt_vars_11, drp_vars_11,
            txt_vars_12, drp_vars_12,
            txt_vars_13, drp_vars_13,
            txt_vars_14, drp_vars_14,
            txt_vars_15, drp_vars_15,
            txt_vars_16, drp_vars_16,
            txt_vars_17, drp_vars_17,
            txt_vars_18, drp_vars_18,
            txt_vars_19, drp_vars_19,
            txt_vars_20, drp_vars_20
        ]

        #
        # Events
        #
        # == Multi Merge ==
        def modelmerger(
                    A1, B1, C1, M1, S1, F1, O1, CF1,
                    A2, B2, C2, M2, S2, F2, O2, CF2,
                    A3, B3, C3, M3, S3, F3, O3, CF3,
                    A4, B4, C4, M4, S4, F4, O4, CF4,
                    A5, B5, C5, M5, S5, F5, O5, CF5,
                    A6, B6, C6, M6, S6, F6, O6, CF6,
                    A7, B7, C7, M7, S7, F7, O7, CF7,
                    A8, B8, C8, M8, S8, F8, O8, CF8,
                    A9, B9, C9, M9, S9, F9, O9, CF9,
                    A10,B10,C10,M10,S10,F10,O10,CF10,
                    chk_skip_merge_if_exists
                ):
            merge_ope = MergeOperation()
            merge_ope.add_merge(1, A1, B1, C1, M1, S1, F1, O1, CF1)
            merge_ope.add_merge(2, A2, B2, C2, M2, S2, F2, O2, CF2)
            merge_ope.add_merge(3, A3, B3, C3, M3, S3, F3, O3, CF3)
            merge_ope.add_merge(4, A4, B4, C4, M4, S4, F4, O4, CF4)
            merge_ope.add_merge(5, A5, B5, C5, M5, S5, F5, O5, CF5)
            merge_ope.add_merge(6, A6, B6, C6, M6, S6, F6, O6, CF6)
            merge_ope.add_merge(7, A7, B7, C7, M7, S7, F7, O7, CF7)
            merge_ope.add_merge(8, A8, B8, C8, M8, S8, F8, O8, CF8)
            merge_ope.add_merge(9, A9, B9, C9, M9, S9, F9, O9, CF9)
            merge_ope.add_merge(10,A10,B10,C10,M10,S10,F10,O10,CF10)

            if not merge_ope.can_process():
                return "Error loading merge settings. A or B missing."

            _process_total = merge_ope.get_process_num()
            print(f"Start Merge processes. Total process num: {_process_total} .")

            # run merge
            _ret_all = merge_ope.run_merge(skip_merge_if_exists=chk_skip_merge_if_exists)

            print(f"All Multi-Merge process finished. {len(_ret_all)} files.")
            for _ret in _ret_all:
                print(f"  {_ret[0]}")

            # make output for gr.HTML
            _ret_html = f"<p style='font-size: 18px'>All Multi-Merge process finished. Output {len(_ret_all)} ckpt files.<br />"
            for _ret in _ret_all:
                _ret_html += f" - {_ret[1]}<br />"
            _ret_html += "</p>"
            return _ret_html

        btn_run_merge.click(
            fn=modelmerger,
            inputs=[
                A1, B1, C1, M1, S1, F1, O1, CF1,
                A2, B2, C2, M2, S2, F2, O2, CF2,
                A3, B3, C3, M3, S3, F3, O3, CF3,
                A4, B4, C4, M4, S4, F4, O4, CF4,
                A5, B5, C5, M5, S5, F5, O5, CF5,
                A6, B6, C6, M6, S6, F6, O6, CF6,
                A7, B7, C7, M7, S7, F7, O7, CF7,
                A8, B8, C8, M8, S8, F8, O8, CF8,
                A9, B9, C9, M9, S9, F9, O9, CF9,
                A10,B10,C10,M10,S10,F10,O10,CF10,
                chk_skip_merge_if_exists
            ],
            outputs=[submit_result]
        )

        def reload_checkpoints():
            sd_models.list_models()
            return [gr.update(choices=ui_merge.get_choise_of_models_with_vars(i//3+1), value="") for i in range(len(_checkpoint_listener))]
        btn_reload_checkpoints.click(
            fn=reload_checkpoints,
            inputs=[],
            outputs=_checkpoint_listener
        )

        # on UI:Merge to UI:Recipe
        def on_send_to_recipe(
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
                ):
            _parser = RecipeParser()
            _parser.send_to_recipe(A1, B1, C1, O1, M1, S1, F1, CF1)
            _parser.send_to_recipe(A2, B2, C2, O2, M2, S2, F2, CF2)
            _parser.send_to_recipe(A3, B3, C3, O3, M3, S3, F3, CF3)
            _parser.send_to_recipe(A4, B4, C4, O4, M4, S4, F4, CF4)
            _parser.send_to_recipe(A5, B5, C5, O5, M5, S5, F5, CF5)
            _parser.send_to_recipe(A6, B6, C6, O6, M6, S6, F6, CF6)
            _parser.send_to_recipe(A7, B7, C7, O7, M7, S7, F7, CF7)
            _parser.send_to_recipe(A8, B8, C8, O8, M8, S8, F8, CF8)
            _parser.send_to_recipe(A9, B9, C9, O9, M9, S9, F9, CF9)
            _parser.send_to_recipe(A10,B10,C10,O10,M10,S10,F10,CF10)
            return [gr.update(value=_parser.output_txt()), gr.update(value="")]
        btn_send_to_recipe.click(
            fn=on_send_to_recipe,
            inputs=[
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
                ],
            outputs=[txt_recipe, txt_parse_result],
            _js="select_tab_recipe"
        )

        # UI:recipe send to Merge
        def on_send_recipe_to_merge(
            txt_recipe,
            txt_vars_01, drp_vars_01,
            txt_vars_02, drp_vars_02,
            txt_vars_03, drp_vars_03,
            txt_vars_04, drp_vars_04,
            txt_vars_05, drp_vars_05,
            txt_vars_06, drp_vars_06,
            txt_vars_07, drp_vars_07,
            txt_vars_08, drp_vars_08,
            txt_vars_09, drp_vars_09,
            txt_vars_10, drp_vars_10,
            txt_vars_11, drp_vars_11,
            txt_vars_12, drp_vars_12,
            txt_vars_13, drp_vars_13,
            txt_vars_14, drp_vars_14,
            txt_vars_15, drp_vars_15,
            txt_vars_16, drp_vars_16,
            txt_vars_17, drp_vars_17,
            txt_vars_18, drp_vars_18,
            txt_vars_19, drp_vars_19,
            txt_vars_20, drp_vars_20
            ):
            VARS = namedtuple("variables", ["name", "ckpt"])
            _list = [
                VARS(txt_vars_01, drp_vars_01),
                VARS(txt_vars_02, drp_vars_02),
                VARS(txt_vars_03, drp_vars_03),
                VARS(txt_vars_04, drp_vars_04),
                VARS(txt_vars_05, drp_vars_05),
                VARS(txt_vars_06, drp_vars_06),
                VARS(txt_vars_07, drp_vars_07),
                VARS(txt_vars_08, drp_vars_08),
                VARS(txt_vars_09, drp_vars_09),
                VARS(txt_vars_10, drp_vars_10),
                VARS(txt_vars_11, drp_vars_11),
                VARS(txt_vars_12, drp_vars_12),
                VARS(txt_vars_13, drp_vars_13),
                VARS(txt_vars_14, drp_vars_14),
                VARS(txt_vars_15, drp_vars_15),
                VARS(txt_vars_16, drp_vars_16),
                VARS(txt_vars_17, drp_vars_17),
                VARS(txt_vars_18, drp_vars_18),
                VARS(txt_vars_19, drp_vars_19),
                VARS(txt_vars_20, drp_vars_20)
                ]
            _vars = {}
            for _item in _list:
                _item:VARS = _item
                if _item.name and _item.name != "" and _item.ckpt and _item.ckpt != "":
                    _vars.update({_item.name: _item.ckpt})

            _parser = RecipeParser(txt_recipe)
            if _parser == None:
                return [ None for _ in range(7*10) ]
            else:
                _parser.apply_vars(_vars)
                return _parser.output_grupdate_uimerge()

        btn_send_recipe_to_multi_merge.click(
            fn=on_send_recipe_to_merge,
            inputs=[txt_recipe] + vars_list,
            outputs=[
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
            ],
            _js="select_tab_merge"
        )

    # return required as (gradio_component, title, elem_id)
    return (main_block, "Merge Board", "merge_board"),

# on_UI
script_callbacks.on_ui_tabs(on_ui_tabs)
