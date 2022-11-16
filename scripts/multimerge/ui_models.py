import gradio as gr

from modules import sd_models

def on_ui_tabs():
    with gr.Tab("Models"):
        with gr.Column():
            with gr.Row():
                gr.HTML("<h1>This is your models list.</h1>")
                btn_listup_checkpoints = gr.Button("List-Up checkpoints")
            with gr.Row():
                df_checkpoints = gr.Dataframe(
                    headers=['filename', 'title', 'hash', 'model_name', 'config'],
                    datatype=["str", "str", "str", "str", "str"],
                    col_count=(5, "fixed"),
                    wrap=True
                )

    # == Models ==
    def listup_checkpoints():
        _models = [ x for x in sd_models.checkpoints_list.values()]
        return gr.update(value=_models)
    btn_listup_checkpoints.click(
        fn=listup_checkpoints,
        inputs=[],
        outputs=[df_checkpoints]
    )
