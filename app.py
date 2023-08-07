import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        essay = request.form["essay"]
        grade = request.form["grade"]
        prompt = request.form["prompt"]
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=generate_prompt(grade, prompt, essay),
            temperature=0,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(grade, prompt, essay):
    return """Your task is to grade an essay of a {} student with the given prompt and grading criteria. 
The prompt is delimited by angle brackets.
The grading criteria is delimited by the triple backticks.
The essay to be graded is delimited by triple quotes.
<{}>
```
1. Content -- fully answering the task (5 marks)
2. Communicative achievement -- clear ideas, formal English, tone of language (5 marks)
3. Organization -- text structure, coherence, cohesion (5 marks)
4. Language -- grammar, vocabulary (5 marks)
```
\"\"\"{}\"\"\"
    """.format(
        grade,
        prompt,
        essay
    )

# """   
# Your task is to grade an essay of a {} student with the given prompt and grading criteria. 
# The prompt is delimited by angle brackets.
# The grading criteria is delimited by the triple backticks.
# The essay to be graded is delimited by triple quotes.
# <{}>
# ```
# 1. Content -- fully answering the task (5 marks)
# 2. Communicative achievement -- clear ideas, formal English, tone of language (5 marks)
# 3. Organization -- text structure, coherence, cohesion (5 marks)
# 4. Language -- grammar, vocabulary (5 marks)
# ```
# """{}"""

# Use the following format for the output:
# Content: <score and comments on content>
# Communicative achievement: <score and comments communicative achievement>
# Organization: <score and comments on organization>
# Language: <score and comments on grammar and vocabulary>
# Overall comments: <strength and weakness of the essay>
# Final grade: <overall grade for the essay>
# Edited version: <essay with grammatical and spelling errors fixed>

# """