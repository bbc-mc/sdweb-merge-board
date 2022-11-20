import gradio as gr

from modules import sd_models

from scripts.multimerge.recipe_parser import RecipeParser

default_recipe = " \
# Sample Recipe \n\
SD-WD Fix = __SD15__ + __WD13__, 0.05 \n\
SW-F = __O1__ + __F222__ + __SD15__, 1.0 \n\
r34gg = __r34__ + __gg__, 0.5 \n\
r34gg-wd = __O3__ + __WD13__, 0.5 \n\
gwf = __O4__ + __F222__, 0.5 \n\
test06 = __O2__ + __O5__, 0.3\
"

choice_of_models = [ x.title for x in sd_models.checkpoints_list.values()]

def on_ui_tabs():
    with gr.Tab("Recipe"):
        with gr.Row():
            with gr.Column():
                txt_recipe = gr.TextArea(label="Recipe", value=default_recipe, placeholder="Input your merge recipe and click 'Parse' button.")
                txt_parse_result = gr.TextArea(label="Parse Result", visible=True, interactive=False)
            with gr.Column():
                with gr.Row():
                    btn_parse_recipe = gr.Button("Parse Recipe", variant="primary")
                    btn_send_recipe_to_multi_merge = gr.Button("Send to Multi-Merge", variant="primary")
                with gr.Row():
                    btn_reset_recipe = gr.Button("Reset recipe text area")
                    btn_reset_vars = gr.Button("Reset vars")
                with gr.Row():
                    with gr.Column(variant="panel"):
                        with gr.Row(visible=False) as row_01:
                            txt_vars_01 = gr.Text(label="var_01", visible=False, interactive=False)
                            drp_vars_01 = gr.Dropdown(label="var_01", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_02:
                            txt_vars_02 = gr.Text(label="var_02", visible=False, interactive=False)
                            drp_vars_02 = gr.Dropdown(label="var_02", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_03:
                            txt_vars_03 = gr.Text(label="var_03", visible=False, interactive=False)
                            drp_vars_03 = gr.Dropdown(label="var_03", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_04:
                            txt_vars_04 = gr.Text(label="var_04", visible=False, interactive=False)
                            drp_vars_04 = gr.Dropdown(label="var_04", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_05:
                            txt_vars_05 = gr.Text(label="var_05", visible=False, interactive=False)
                            drp_vars_05 = gr.Dropdown(label="var_05", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_06:
                            txt_vars_06 = gr.Text(label="var_06", visible=False, interactive=False)
                            drp_vars_06 = gr.Dropdown(label="var_06", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_07:
                            txt_vars_07 = gr.Text(label="var_07", visible=False, interactive=False)
                            drp_vars_07 = gr.Dropdown(label="var_07", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_08:
                            txt_vars_08 = gr.Text(label="var_08", visible=False, interactive=False)
                            drp_vars_08 = gr.Dropdown(label="var_08", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_09:
                            txt_vars_09 = gr.Text(label="var_09", visible=False, interactive=False)
                            drp_vars_09 = gr.Dropdown(label="var_09", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_10:
                            txt_vars_10 = gr.Text(label="var_10", visible=False, interactive=False)
                            drp_vars_10 = gr.Dropdown(label="var_10", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_11:
                            txt_vars_11 = gr.Text(label="var_11", visible=False, interactive=False)
                            drp_vars_11 = gr.Dropdown(label="var_11", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_12:
                            txt_vars_12 = gr.Text(label="var_12", visible=False, interactive=False)
                            drp_vars_12 = gr.Dropdown(label="var_12", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_13:
                            txt_vars_13 = gr.Text(label="var_13", visible=False, interactive=False)
                            drp_vars_13 = gr.Dropdown(label="var_13", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_14:
                            txt_vars_14 = gr.Text(label="var_14", visible=False, interactive=False)
                            drp_vars_14 = gr.Dropdown(label="var_14", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_15:
                            txt_vars_15 = gr.Text(label="var_15", visible=False, interactive=False)
                            drp_vars_15 = gr.Dropdown(label="var_15", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_16:
                            txt_vars_16 = gr.Text(label="var_16", visible=False, interactive=False)
                            drp_vars_16 = gr.Dropdown(label="var_16", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_17:
                            txt_vars_17 = gr.Text(label="var_17", visible=False, interactive=False)
                            drp_vars_17 = gr.Dropdown(label="var_17", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_18:
                            txt_vars_18 = gr.Text(label="var_18", visible=False, interactive=False)
                            drp_vars_18 = gr.Dropdown(label="var_18", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_19:
                            txt_vars_19 = gr.Text(label="var_19", visible=False, interactive=False)
                            drp_vars_19 = gr.Dropdown(label="var_19", choices=choice_of_models, visible=False, interactive=True)
                        with gr.Row(visible=False) as row_20:
                            txt_vars_20 = gr.Text(label="var_20", visible=False, interactive=False)
                            drp_vars_20 = gr.Dropdown(label="var_20", choices=choice_of_models, visible=False, interactive=True)
                        vars_list = [
                            row_01, txt_vars_01, drp_vars_01,
                            row_02, txt_vars_02, drp_vars_02,
                            row_03, txt_vars_03, drp_vars_03,
                            row_04, txt_vars_04, drp_vars_04,
                            row_05, txt_vars_05, drp_vars_05,
                            row_06, txt_vars_06, drp_vars_06,
                            row_07, txt_vars_07, drp_vars_07,
                            row_08, txt_vars_08, drp_vars_08,
                            row_09, txt_vars_09, drp_vars_09,
                            row_10, txt_vars_10, drp_vars_10,
                            row_11, txt_vars_11, drp_vars_11,
                            row_12, txt_vars_12, drp_vars_12,
                            row_13, txt_vars_13, drp_vars_13,
                            row_14, txt_vars_14, drp_vars_14,
                            row_15, txt_vars_15, drp_vars_15,
                            row_16, txt_vars_16, drp_vars_16,
                            row_17, txt_vars_17, drp_vars_17,
                            row_18, txt_vars_18, drp_vars_18,
                            row_19, txt_vars_19, drp_vars_19,
                            row_20, txt_vars_20, drp_vars_20
                        ]

    def on_parse_recipe(txt_recipe):
        _perser = RecipeParser(txt_recipe)
        _ret = [gr.update(value=_perser.output_txt())] + _perser.output_grupdate_uirecipe(vars_list)
        return _ret
    btn_parse_recipe.click(
        fn=on_parse_recipe,
        inputs=[txt_recipe],
        outputs=[txt_parse_result] + vars_list
    )

    def on_reset_recipe():
        return [gr.update(value=default_recipe), gr.update(value="")]
    btn_reset_recipe.click(
        fn=on_reset_recipe,
        inputs=[],
        outputs=[txt_recipe, txt_parse_result]
    )

    def on_reset_vars():
        sd_models.list_models()
        choice_of_models = sd_models.checkpoint_tiles()
        _ret = []
        for i in range(int(len(vars_list)/3)):
            _ret += [ gr.update(visible=False), gr.update(value="", visible=False), gr.update(value="", visible=False, choices=choice_of_models) ]
        return _ret
    btn_reset_vars.click(
        fn=on_reset_vars,
        inputs=[],
        outputs=vars_list
    )

    _ret = [txt_recipe, txt_parse_result, btn_send_recipe_to_multi_merge] + vars_list

    return _ret
