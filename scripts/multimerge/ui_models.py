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
                    headers=['filename', 'title', 'hash', 'model_name', 'config', 'sha256'],
                    datatype=["str", "str", "str", "str", "str", "str"],
                    col_count=(6, "fixed"),
                    wrap=True
                )

    # == Models ==
    def model_data(model_info):
        filename = model_info.filename if hasattr(model_info, "filename") else ""
        title = model_info.title if hasattr(model_info, "title") else ""
        hash = model_info.hash if hasattr(model_info, "hash") else ""
        model_name = model_info.model_name if hasattr(model_info, "model_name") else ""
        config = model_info.config if hasattr(model_info, "config") else ""
        sha256 = model_info.sha256 if hasattr(model_info, "sha256") else ""
        return (filename, title, hash, model_name, config, sha256)
    def listup_checkpoints():
        _models = [ model_data(x) for x in sd_models.checkpoints_list.values()]
        return gr.update(value=_models)
    btn_listup_checkpoints.click(
        fn=listup_checkpoints,
        inputs=[],
        outputs=[df_checkpoints]
    )
