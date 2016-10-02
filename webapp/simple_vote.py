from operator import attrgetter

from flask import Flask, request, abort

from webapp.model import Vote, Item
from jinja2 import Environment, PackageLoader

app = Flask(__name__)
env = Environment(autoescape=True, loader=PackageLoader('webapp', 'templates'))


@app.route('/', methods=['GET'])
def show_votes():
    votes = Vote.objects
    template = env.get_template('votes.html')
    return template.render(votes=votes)


@app.route('/', methods=['POST'])
def edit_votes():
    name = request.form['name']
    action = request.form['action']
    if action == 'ADD':
        Vote(name).save()
    return show_votes()


def render_vote(id, name, items):
    template = env.get_template('vote.html')
    return template.render(items=items, name=name, id=id)


@app.route('/vote', methods=['GET'])
def show_vote():
    id = request.args.get('id', None)
    vote = Vote.objects.get(id=id)
    if vote is None:
        abort(404)
    name = vote.name
    items = vote.items

    return render_vote(items=items, name=name, id=id)


@app.route('/vote', methods=['POST'])
def edit_vote():
    action = request.form['action']
    id = request.form['id']
    vote = Vote.objects.get(id=id)
    if vote is None:
        abort(400)
    name = vote.name

    if action == 'ADD':
        new_item_name = request.form['name']
        item = Item(name=new_item_name, point=0)
        item.save()
        vote.items.append(item)
        vote.save()
    elif action == 'VOTE':
        chosen = request.form['chosen']
        item = Item.objects.get(id=chosen)
        if chosen is None:
            abort(400)
        item.point += 1
        item.save()
        vote.items.sort(key=attrgetter('point'), reverse=True)
        vote.save()

    return render_vote(items=vote.items, name=name, id=id)


# This is for debugger
def port_check(hostname, port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((hostname, port))
    except socket.gaierror:
        sock.close()
        return False
    sock.close()
    return result == 0


if __name__ == '__main__':
    # This is for debugger
    debug_port = 5678
    if port_check('debug_host', debug_port):
        import pydevd
        pydevd.settrace('debug_host', port=debug_port, stdoutToServer=True, stderrToServer=True)

    app.run(host='0.0.0.0')
