from flask import Flask, render_template, request

app = Flask("SickoMode")

@app.route("/", methods=['GET', 'POST'])
def home():
    return "Whats Up"



if __name__ == "__main__":
    # Run app
    app.run(host="0.0.0.0", port=80)
