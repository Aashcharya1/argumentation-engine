"""Local UI/API. Run python server.py and open http://127.0.0.1:8000."""
import json
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from engine import ArgumentationFramework, GroundedMechanism, jsonable


def analyse(data):
    af = ArgumentationFramework(data['arguments'], data['attacks'])
    if len(af.arguments) > 10:
        raise ValueError('Interactive exhaustive analysis supports at most 10 arguments')
    semantics = ['grounded', 'complete', 'preferred', 'stable', 'semi-stable']
    s = data.get('set', [])
    answer = {'extensions': {k: af.extensions(k) for k in semantics},
              'labellings': af.legal_labellings(),
              'set_analysis': dict(conflict_free=af.conflict_free(s), admissible=af.admissible(s),
                                   complete=af.complete(s), defended=af.characteristic(s)),
              'acceptance': {a: {k: af.acceptance_status(a, k) for k in semantics}
                             for a in sorted(af.arguments)}}
    if 'ownership' in data:
        game = GroundedMechanism(af, data['ownership'])
        reports = data.get('reports', data['ownership'])
        sp, witness = game.strategyproof()
        condition, path = game.odd_path_condition()
        answer['strategic'] = dict(outcome=game.outcome(reports),
                                  utilities=[game.utility(i, reports) for i in range(len(reports))],
                                  best_responses=[game.best_responses(i, reports) for i in range(len(reports))],
                                  strategyproof=sp, deviation=witness, condition=condition, odd_walk=path)
    return jsonable(answer)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {'/': ('web/index.html', 'text/html; charset=utf-8'),
                  '/results': ('results/summary.csv', 'text/csv; charset=utf-8')}
        if self.path not in routes:
            self.send_error(404)
            return
        filename, mime = routes[self.path]
        payload = (Path(__file__).parent / filename).read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        if self.path != '/api/analyse':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', 0))
            if not 0 < length <= 100000:
                raise ValueError('Invalid request length')
            result = analyse(json.loads(self.rfile.read(length)))
            code = 200
        except (ValueError, KeyError, TypeError, IndexError) as exc:
            result, code = {'error': str(exc)}, 400
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    print(f'Argumentation Lab: http://127.0.0.1:{args.port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
