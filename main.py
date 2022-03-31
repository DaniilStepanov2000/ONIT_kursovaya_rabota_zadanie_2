import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/apply_filter', methods=['GET', 'POST'])
def apply_filter():
    if request.method == 'POST':
        result = request.form.to_dict()
        if result['filter'] == 'listen':
            ports = run_scan('LISTEN')
            print(ports)
        elif result['filter'] == 'established':
            ports = run_scan('ESTABLISHED')
        return render_template('ports_table.html', data={'data': ports}, filter_type={'filter_type': result['filter']})
    return render_template('ports_table.html', data={'data': ''}, filter_type={'filter_type': ''})


def run_scan(state):
    ports_number = []
    ports = subprocess.Popen('lsof -i tcp -n -P | grep {}'.format(state), shell=True,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = ports.stdout.readlines()
    new_data = []
    for d in data:
        if isinstance(d, bytes):
            new_data.append(d.decode())
    if state == 'LISTEN':
        for d in new_data:
            ports_number.append(d.split()[-2].split(':')[-1])
        print('listen ports: {}'.format(ports_number))
        return sorted(set(ports_number))
    elif state == 'ESTABLISHED':
        for d in new_data:
            ports_number.append(d.split()[-2].split('->')[0].split(':')[-1])
        print('established ports: {}'.format(ports_number))
        return sorted(set(ports_number))


if __name__ == '__main__':
    app.run(debug=True)


