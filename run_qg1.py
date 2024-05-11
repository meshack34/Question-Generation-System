import argparse
from questiongenerator import QuestionGenerator
from questiongenerator import print_qa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--answer_style",
        default="all",
        type=str,
        help="The desired type of answers. Choose from ['all', 'sentences', 'multiple_choice']",
    )
    parser.add_argument("--model_dir", type=str, default=None)
    parser.add_argument("--num_questions", type=int, default=10)
    parser.add_argument("--show_answers", dest="show_answers", action="store_true", default=True)
    parser.add_argument("--text_file", type=str, required=True)
    parser.add_argument("--use_qa_eval", dest="use_qa_eval", action="store_true", default=True)
    parser.add_argument("--output_pdf", type=str, required=True)
    return parser.parse_args()


def create_pdf(qa_list, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter

    # Set up the PDF layout
    c.setFont("Helvetica", 12)
    margin = 50
    y_position = height - margin

    # Write questions and answers to the PDF
    for question, answer in qa_list:
        c.drawString(margin, y_position, "Q: " + question)
        y_position -= 20
        c.drawString(margin, y_position, "A: " + answer)
        y_position -= 40
        if y_position <= margin:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - margin

    # Save the PDF
    c.save()


if __name__ == "__main__":
    args = parse_args()
    with open(args.text_file, 'r') as file:
        text_file = file.read()
    qg = QuestionGenerator()
    qa_list = qg.generate(
        text_file,
        num_questions=int(args.num_questions),
        answer_style=args.answer_style,
        use_evaluator=args.use_qa_eval
    )
    create_pdf(qa_list, args.output_pdf)
