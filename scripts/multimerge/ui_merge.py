
import gradio as gr

from modules import sd_models

from scripts.multimerge.recipe import S_WS, S_AD, S_SG, choise_of_method

Variables_Output = ["__O1__", "__O2__", "__O3__", "__O4__", "__O5__", "__O6__", "__O7__", "__O8__", "__O9__", "__O10__"]

def get_choise_of_models_with_vars(current_line=10):
    return Variables_Output[:current_line-1] + sd_models.checkpoint_tiles()


def on_ui_tabs():

    _checkpoint_listener = []

    with gr.Tab("Multi Merge"):
        with gr.Column():
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Row():
                        btn_run_merge = gr.Button("Run Merge", variant="primary")
                        btn_send_to_recipe = gr.Button("Send to Recipe", variant="primary")
                        btn_reload_checkpoints = gr.Button("Reload Checkpoints")
                        btn_clear_merge_settings = gr.Button("Clear inputs")
                    with gr.Row():
                        with gr.Column(scale=1):
                            submit_result = gr.HTML(elem_id="modelmerger_result", show_label=False)
                        with gr.Column(scale=1):
                            with gr.Row():
                                radio_config_source = gr.Radio(choices=["A, B or C", "B", "C", "Don't"], value="A, B or C", label="Copy config from", type="index")
                                chk_skip_merge_if_exists = gr.Checkbox(label="Skip merge if same-name ckpt already exists", value=False, interactive=True)
                                chk_save_metadata = gr.Checkbox(value=True, label="Save metadata (.safetensors only)")

            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        with gr.Column():
                            with gr.Row(variant="panel"):
                                _line_number = 1
                                A1 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(A{_line_number}) Primary")
                                B1 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(B{_line_number}) Secondary")
                                C1 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(C{_line_number}) Thertiary")
                                O1 = gr.Textbox(label=f"(O{_line_number}) Output ckpt Name", interactive=True)
                                M1 = gr.Slider(minimum=0.0, maximum=1.0, step=0.001, label=f'(M{_line_number}) Multiplier', value=0.5, interactive=True)
                                S1 = gr.Dropdown(choices=choise_of_method, interactive=True, value=choise_of_method[0], label=f"(S{_line_number}) Inter-Method")
                                F1 = gr.Checkbox(value=False, interactive=True, label=f"(F{_line_number}) Save as float16")
                                CF1 = gr.Radio(choices=["ckpt", "safetensors"], interactive=True, value="ckpt", label=f"(CF{_line_number}) Checkpoint format")
                                _checkpoint_listener += [A1, B1, C1]
                    with gr.Row():
                        with gr.Column():
                            with gr.Row(variant="panel"):
                                _line_number = 2
                                A2 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(A{_line_number}) Primary")
                                B2 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(B{_line_number}) Secondary")
                                C2 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(C{_line_number}) Thertiary")
                                O2 = gr.Textbox(label=f"(O{_line_number}) Output ckpt Name", interactive=True)
                                M2 = gr.Slider(minimum=0.0, maximum=1.0, step=0.001, label=f'(M{_line_number}) Multiplier', value=0.5, interactive=True)
                                S2 = gr.Dropdown(choices=choise_of_method, interactive=True, value=choise_of_method[0], label=f"(S{_line_number}) Inter-Method")
                                F2 = gr.Checkbox(value=False, interactive=True, label=f"(F{_line_number}) Save as float16")
                                CF2 = gr.Radio(choices=["ckpt", "safetensors"], interactive=True, value="ckpt", label=f"(CF{_line_number}) Checkpoint format")
                                _checkpoint_listener += [A2, B2, C2]
                    with gr.Row():
                        with gr.Column():
                            with gr.Row(variant="panel"):
                                _line_number = 3
                                A3 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(A{_line_number}) Primary")
                                B3 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(B{_line_number}) Secondary")
                                C3 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(C{_line_number}) Thertiary")
                                O3 = gr.Textbox(label=f"(O{_line_number}) Output ckpt Name", interactive=True)
                                M3 = gr.Slider(minimum=0.0, maximum=1.0, step=0.001, label=f'(M{_line_number}) Multiplier', value=0.5, interactive=True)
                                S3 = gr.Dropdown(choices=choise_of_method, interactive=True, value=choise_of_method[0], label=f"(S{_line_number}) Inter-Method")
                                F3 = gr.Checkbox(value=False, interactive=True, label=f"(F{_line_number}) Save as float16")
                                CF3 = gr.Radio(choices=["ckpt", "safetensors"], interactive=True, value="ckpt", label=f"(CF{_line_number}) Checkpoint format")
                                _checkpoint_listener += [A3, B3, C3]
                    with gr.Row():
                        with gr.Column():
                            with gr.Row(variant="panel"):
                                _line_number = 4
                                A4 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(A{_line_number}) Primary")
                                B4 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(B{_line_number}) Secondary")
                                C4 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(C{_line_number}) Thertiary")
                                O4 = gr.Textbox(label=f"(O{_line_number}) Output ckpt Name", interactive=True)
                                M4 = gr.Slider(minimum=0.0, maximum=1.0, step=0.001, label=f'(M{_line_number}) Multiplier', value=0.5, interactive=True)
                                S4 = gr.Dropdown(choices=choise_of_method, interactive=True, value=choise_of_method[0], label=f"(S{_line_number}) Inter-Method")
                                F4 = gr.Checkbox(value=False, interactive=True, label=f"(F{_line_number}) Save as float16")
                                CF4 = gr.Radio(choices=["ckpt", "safetensors"], interactive=True, value="ckpt", label=f"(CF{_line_number}) Checkpoint format")
                                _checkpoint_listener += [A4, B4, C4]
                    with gr.Row():
                        with gr.Column():
                            with gr.Row(variant="panel"):
                                _line_number = 5
                                A5 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(A{_line_number}) Primary")
                                B5 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(B{_line_number}) Secondary")
                                C5 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(C{_line_number}) Thertiary")
                                O5 = gr.Textbox(label=f"(O{_line_number}) Output ckpt Name", interactive=True)
                                M5 = gr.Slider(minimum=0.0, maximum=1.0, step=0.001, label=f'(M{_line_number}) Multiplier', value=0.5, interactive=True)
                                S5 = gr.Dropdown(choices=choise_of_method, interactive=True, value=choise_of_method[0], label=f"(S{_line_number}) Inter-Method")
                                F5 = gr.Checkbox(value=False, interactive=True, label=f"(F{_line_number}) Save as float16")
                                CF5 = gr.Radio(choices=["ckpt", "safetensors"], interactive=True, value="ckpt", label=f"(CF{_line_number}) Checkpoint format")
                                _checkpoint_listener += [A5, B5, C5]
                    with gr.Row():
                        with gr.Column():
                            with gr.Row(variant="panel"):
                                _line_number = 6
                                A6 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(A{_line_number}) Primary")
                                B6 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(B{_line_number}) Secondary")
                                C6 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(C{_line_number}) Thertiary")
                                O6 = gr.Textbox(label=f"(O{_line_number}) Output ckpt Name", interactive=True)
                                M6 = gr.Slider(minimum=0.0, maximum=1.0, step=0.001, label=f'(M{_line_number}) Multiplier', value=0.5, interactive=True)
                                S6 = gr.Dropdown(choices=choise_of_method, interactive=True, value=choise_of_method[0], label=f"(S{_line_number}) Inter-Method")
                                F6 = gr.Checkbox(value=False, interactive=True, label=f"(F{_line_number}) Save as float16")
                                CF6 = gr.Radio(choices=["ckpt", "safetensors"], interactive=True, value="ckpt", label=f"(CF{_line_number}) Checkpoint format")
                                _checkpoint_listener += [A6, B6, C6]
                    with gr.Row():
                        with gr.Column():
                            with gr.Row(variant="panel"):
                                _line_number = 7
                                A7 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(A{_line_number}) Primary")
                                B7 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(B{_line_number}) Secondary")
                                C7 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(C{_line_number}) Thertiary")
                                O7 = gr.Textbox(label=f"(O{_line_number}) Output ckpt Name", interactive=True)
                                M7 = gr.Slider(minimum=0.0, maximum=1.0, step=0.001, label=f'(M{_line_number}) Multiplier', value=0.5, interactive=True)
                                S7 = gr.Dropdown(choices=choise_of_method, interactive=True, value=choise_of_method[0], label=f"(S{_line_number}) Inter-Method")
                                F7 = gr.Checkbox(value=False, interactive=True, label=f"(F{_line_number}) Save as float16")
                                CF7 = gr.Radio(choices=["ckpt", "safetensors"], interactive=True, value="ckpt", label=f"(CF{_line_number}) Checkpoint format")
                                _checkpoint_listener += [A7, B7, C7]
                    with gr.Row():
                        with gr.Column():
                            with gr.Row(variant="panel"):
                                _line_number = 8
                                A8 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(A{_line_number}) Primary")
                                B8 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(B{_line_number}) Secondary")
                                C8 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(C{_line_number}) Thertiary")
                                O8 = gr.Textbox(label=f"(O{_line_number}) Output ckpt Name", interactive=True)
                                M8 = gr.Slider(minimum=0.0, maximum=1.0, step=0.001, label=f'(M{_line_number}) Multiplier', value=0.5, interactive=True)
                                S8 = gr.Dropdown(choices=choise_of_method, interactive=True, value=choise_of_method[0], label=f"(S{_line_number}) Inter-Method")
                                F8 = gr.Checkbox(value=False, interactive=True, label=f"(F{_line_number}) Save as float16")
                                CF8 = gr.Radio(choices=["ckpt", "safetensors"], interactive=True, value="ckpt", label=f"(CF{_line_number}) Checkpoint format")
                                _checkpoint_listener += [A8, B8, C8]
                    with gr.Row():
                        with gr.Column():
                            with gr.Row(variant="panel"):
                                _line_number = 9
                                A9 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(A{_line_number}) Primary")
                                B9 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(B{_line_number}) Secondary")
                                C9 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(C{_line_number}) Thertiary")
                                O9 = gr.Textbox(label=f"(O{_line_number}) Output ckpt Name", interactive=True)
                                M9 = gr.Slider(minimum=0.0, maximum=1.0, step=0.001, label=f'(M{_line_number}) Multiplier', value=0.5, interactive=True)
                                S9 = gr.Dropdown(choices=choise_of_method, interactive=True, value=choise_of_method[0], label=f"(S{_line_number}) Inter-Method")
                                F9 = gr.Checkbox(value=False, interactive=True, label=f"(F{_line_number}) Save as float16")
                                CF9 = gr.Radio(choices=["ckpt", "safetensors"], interactive=True, value="ckpt", label=f"(CF{_line_number}) Checkpoint format")
                                _checkpoint_listener += [A9, B9, C9]
                    with gr.Row():
                        with gr.Column():
                            with gr.Row(variant="panel"):
                                _line_number = 10
                                A10 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(A{_line_number}) Primary")
                                B10 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(B{_line_number}) Secondary")
                                C10 = gr.Dropdown(choices=get_choise_of_models_with_vars(_line_number), interactive=True, label=f"(C{_line_number}) Thertiary")
                                O10 = gr.Textbox(label=f"(O{_line_number}) Output ckpt Name", interactive=True)
                                M10 = gr.Slider(minimum=0.0, maximum=1.0, step=0.001, label=f'(M{_line_number}) Multiplier', value=0.5, interactive=True)
                                S10 = gr.Dropdown(choices=choise_of_method, interactive=True, value=choise_of_method[0], label=f"(S{_line_number}) Inter-Method")
                                F10 = gr.Checkbox(value=False, interactive=True, label=f"(F{_line_number}) Save as float16")
                                CF10 = gr.Radio(choices=["ckpt", "safetensors"], interactive=True, value="ckpt", label=f"(CF{_line_number}) Checkpoint format")
                                _checkpoint_listener += [A10, B10, C10]

    #
    # Events
    #
    def on_clear_settings():
        _ret = [
            gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value=0.5),gr.update(value=S_WS),gr.update(value=False),gr.update(value=""),gr.update(value="ckpt"),
            gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value=0.5),gr.update(value=S_WS),gr.update(value=False),gr.update(value=""),gr.update(value="ckpt"),
            gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value=0.5),gr.update(value=S_WS),gr.update(value=False),gr.update(value=""),gr.update(value="ckpt"),
            gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value=0.5),gr.update(value=S_WS),gr.update(value=False),gr.update(value=""),gr.update(value="ckpt"),
            gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value=0.5),gr.update(value=S_WS),gr.update(value=False),gr.update(value=""),gr.update(value="ckpt"),
            gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value=0.5),gr.update(value=S_WS),gr.update(value=False),gr.update(value=""),gr.update(value="ckpt"),
            gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value=0.5),gr.update(value=S_WS),gr.update(value=False),gr.update(value=""),gr.update(value="ckpt"),
            gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value=0.5),gr.update(value=S_WS),gr.update(value=False),gr.update(value=""),gr.update(value="ckpt"),
            gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value=0.5),gr.update(value=S_WS),gr.update(value=False),gr.update(value=""),gr.update(value="ckpt"),
            gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value=0.5),gr.update(value=S_WS),gr.update(value=False),gr.update(value=""),gr.update(value="ckpt")
            ]
        return _ret
    btn_clear_merge_settings.click(
        fn=on_clear_settings,
        inputs=[],
        outputs=[
        A1, B1, C1, M1, S1, F1, O1, CF1, \
        A2, B2, C2, M2, S2, F2, O2, CF2, \
        A3, B3, C3, M3, S3, F3, O3, CF3, \
        A4, B4, C4, M4, S4, F4, O4, CF4, \
        A5, B5, C5, M5, S5, F5, O5, CF5, \
        A6, B6, C6, M6, S6, F6, O6, CF6, \
        A7, B7, C7, M7, S7, F7, O7, CF7, \
        A8, B8, C8, M8, S8, F8, O8, CF8, \
        A9, B9, C9, M9, S9, F9, O9, CF9, \
        A10,B10,C10,M10,S10,F10,O10,CF10
        ]
    )

    return \
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
        A10,B10,C10,M10,S10,F10,O10,CF10,\
        _checkpoint_listener, chk_skip_merge_if_exists, radio_config_source, chk_save_metadata
