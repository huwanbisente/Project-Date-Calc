from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

def calculate_business_days(start_date, end_date, day_exceptions):
    current_date = start_date
    total_days = 0
    excluded_days = 0

    while current_date <= end_date:
        total_days += 1
        if current_date.strftime('%A').lower() in day_exceptions:
            excluded_days += 1
        current_date += timedelta(days=1)

    return total_days - excluded_days

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date = parse_date(request.form['start_date'])
        end_date = parse_date(request.form['end_date'])
        day_exceptions = get_day_exceptions(request.form['day_exceptions'])
        business_days = calculate_business_days(start_date, end_date, day_exceptions)

        return render_template('result.html', start_date=start_date, end_date=end_date, business_days=business_days)

    return render_template('index.html')

def parse_date(date_string):
    if date_string.lower() == 'today':
        return datetime.now().date()
    return datetime.strptime(date_string, "%Y-%m-%d").date()

def get_day_exceptions(day_exceptions_string):
    if day_exceptions_string.lower() == 'none':
        return []
    elif 'weekend' in day_exceptions_string.lower():
        return ['saturday', 'sunday']
    return [day.strip().lower() for day in day_exceptions_string.split(',')]

if __name__ == "__main__":
    app.run(debug=True)
