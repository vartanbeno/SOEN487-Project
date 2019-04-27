from flask import Response


def response(message, code=200):
    return Response(f'{{"message": "{message}"}}', status=code, mimetype='application/json')
