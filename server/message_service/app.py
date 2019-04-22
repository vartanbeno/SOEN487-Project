from flask import Flask, jsonify, make_response, request
from config import DevConfig
from flask_cors import CORS
import sqlalchemy
import requests



# need an app before we import models because models need it
app = Flask(__name__)
from models import db, row2dict, Conversation, Message
from helpers.jwt import get_data_from_token

app.config.from_object(DevConfig)
cors = CORS(app)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route("/conversation", methods={"GET"})
def get_conversations():
    token = request.headers.get('Authorization').split(" ")[1]
    data = get_data_from_token(token)
    conversation_list = Conversation.query.filter_by(creator_id=data['sub'])
    response = jsonify({
        "user_id": data['sub'],
        "conversations": [row2dict(conversation) for conversation in conversation_list]
    })
    return make_response(response,200)


@app.route("/conversation/<conversation_id>", methods={"GET"})
def get_messages(conversation_id):
    c = Conversation.query.filter_by(id=conversation_id).first()
    response = jsonify({
        "id": c.id,
        "creator_id": c.creator_id,
        "participant_id": c.participant_id,
        "messages": []
    })
    return make_response(response, 200)


@app.route("/conversation/<conversation_id>/<message_limit>", methods={"GET"})
def get_messages_with_limit(conversation_id, message_limit):
    token = request.headers.get('Authorization').split(" ")[1]
    data = get_data_from_token(token)
    c = Conversation.query.filter_by(id=conversation_id).first()
    # messages = Message.query.with_parent(c).order_by(Message.id.desc()).limit(message_limit).all()
    messages = Message.query.order_by(Message.id.desc()).filter_by(conversation_id=conversation_id)
    response = jsonify({
        "user_id": data['sub'],
        "id": c.id,
        "creator_id": c.creator_id,
        "participant_id": c.participant_id,
        "messages": [row2dict(m) for m in messages]
    })
    return make_response(response, 200)


@app.route("/conversation", methods={"POST"})
def create_conversation():
    token = request.headers.get('Authorization').split(" ")[1]
    data = get_data_from_token(token)
    participant_id = int(request.get_json().get("participant_id"))
    if not participant_id:
        return make_response("Missing participant field", 400)
    print(type(participant_id))
    print(type(data['sub']))
    c = Conversation(creator_id=data['sub'], participant_id=participant_id)
    db.session.add(c)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put person. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return make_response(jsonify({
        "id": c.id,
        "creator_id": c.creator_id,
        "participant_id": c.participant_id
    }), 201)


@app.route("/message", methods={"POST"})
def post_message():
    token = request.headers.get('Authorization').split(" ")[1]
    data = get_data_from_token(token)
    conversation_id = request.get_json().get("conversation_id")
    receiverID = request.get_json().get('receiver_id')
    sender_id = data['sub']
    text = request.get_json().get("text")
    if not conversation_id or not sender_id or not text:
        return make_response("Missing body arguments", 400)
    m = Message(conversation_id=conversation_id, sender_id=sender_id, text=text)
    db.session.add(m)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put person. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)

    response = requests.put('http://127.0.0.1:8080/api/notifications/',
                 json={
                     "receiverID": receiverID,
                     "message": "You have a new message from {}".format(receiverID)},
                 headers={'Authorization':request.headers.get('Authorization')})
    print(response.status_code)
    return make_response(jsonify({
        "id": m.id,
        "conversation_id": m.conversation_id,
        "sender_id": m.sender_id,
        "text": m.text
    }), 201)


@app.route("/message/<message_id>", methods={"DELETE"})
def delete_message(message_id):
    m = Message.query.filter_by(id=message_id).first()
    db.session.delete(m)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put person. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return make_response("Message was deleted", 202)


if __name__ == '__main__':
    app.run(port=8081)
