# To host this calculator on a web page, we need a web framework.
# We'll use Flask (a lightweight Python web framework).
# Below, the calculator is provided as a web app with routes for user input and result display.
# Note: To run this, you need to install Flask (`pip install flask`).

from flask import Flask, render_template_string, request # Import necessary Flask functions
import math  # Import math for scientific calculations

app = Flask(__name__)  # Initialize the Flask app

# HTML template for displaying the calculator
template = """
<!doctype html>
<html>
  <head>
    <title>Simple & Scientific Calculator</title>
  </head>
  <body>
    <h2>Web Calculator</h2>
    <form method="POST">
      <!-- Input fields for the two numbers -->
      <label for="num1">First Number:</label>
      <input type="text" id="num1" name="num1">
      <br>
      <label for="num2">Second Number (leave empty for scientific):</label>
      <input type="text" id="num2" name="num2">
      <br>
      <!-- Dropdown for selecting the operator -->
      <label for="op">Operation:</label>
      <select id="op" name="op">
        <option value="+">Addition (+)</option>
        <option value="-">Subtraction (-)</option>
        <option value="*">Multiplication (*)</option>
        <option value="/">Division (/)</option>
        <option value="sqrt">Square Root (sqrt)</option>
        <option value="sin">Sine (sin)</option>
        <option value="log">Natural Logarithm (log)</option>
      </select>
      <br><br>
      <input type="submit" value="Calculate">
    </form>
    {% if result is not none %}
      <h3>Result: {{ result }}</h3>
    {% endif %}
    <!-- Explanation for the user -->
    <p>For scientific operations (sqrt, sin, log), only the first number is used.</p>
  </body>
</html>
"""

# Route for both displaying the form and showing the result
@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None  # Variable to store the result

    if request.method == 'POST':
        # Get form inputs; blank means None
        num1 = request.form.get('num1', '')
        num2 = request.form.get('num2', '')
        op = request.form.get('op', '')

        try:
            if op in ['sqrt', 'sin', 'log']:
                # Only one number needed for scientific functions
                number = float(num1)
                if op == 'sqrt':
                    # Square root
                    if number >= 0:
                        result = f"Square root of {number} = {math.sqrt(number)}"
                    else:
                        result = "Error: Square root of negative number!"
                elif op == 'sin':
                    # Sine (expects radians)
                    result = f"Sine of {number} radians = {math.sin(number)}"
                elif op == 'log':
                    # Natural log
                    if number > 0:
                        result = f"Natural logarithm of {number} = {math.log(number)}"
                    else:
                        result = "Error: Logarithm is only defined for positive numbers!"
            else:
                # For basic operations, need two numbers
                n1 = float(num1)
                n2 = float(num2)
                if op == '+':
                    result = f"{n1} + {n2} = {n1 + n2}"
                elif op == '-':
                    result = f"{n1} - {n2} = {n1 - n2}"
                elif op == '*':
                    result = f"{n1} * {n2} = {n1 * n2}"
                elif op == '/':
                    # Protect against division by zero
                    if n2 != 0:
                        result = f"{n1} / {n2} = {n1 / n2}"
                    else:
                        result = "Error: Division by zero is not allowed."
                else:
                    result = "Invalid operation selected."
        except ValueError:
            # Handles conversion errors if user input is not a valid float
            result = "Error: Please enter valid numeric values."

    # Render the web page with form and result
    return render_template_string(template, result=result)

# Main entry point to run the web server
# To run: `python filename.py` in terminal and browse to http://localhost:5000/
if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True)  # debug=True makes troubleshooting easier



