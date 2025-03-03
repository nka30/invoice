from flask import Flask,render_template,request
from LLM import analyze_query
from db import init_DB
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("interface.html")
@app.route("/userquery", methods=["POST"])
def userquery():
    userquery = request.form.get('userquery')
    try:
        result = analyze_query(userquery)
    except Exception as e:
        return f"Error in processing query: {str(e)}", 500
    return result,200

if __name__ == '__main__':
    init_DB()
    app.run(debug=True)