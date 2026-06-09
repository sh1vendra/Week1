import gradio as gr
from generator import generate


def handle_query(question: str) -> tuple[str, str]:
    if not question.strip():
        return "", ""
    result = generate(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("## Texas State University Professor & Course Review Assistant")
    question_input = gr.Textbox(label="Your question")
    ask_btn = gr.Button("Ask")
    answer_output = gr.Textbox(label="Answer", lines=8)
    sources_output = gr.Textbox(label="Sources", lines=4)

    ask_btn.click(fn=handle_query, inputs=question_input, outputs=[answer_output, sources_output])
    question_input.submit(fn=handle_query, inputs=question_input, outputs=[answer_output, sources_output])

demo.launch()
