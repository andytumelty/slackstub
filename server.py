#!/usr/bin/env python3

from flask import Flask, jsonify, request
import time
import base64
import string
import random
import logging
from copy import deepcopy

app = Flask(__name__)

team_id = "TABC1DEF2"


def generate_user_id():
    user_id = 'U' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    while user_id in [u['id'] for u in users]:
        user_id = generate_user_id()
    return user_id


def get_emails(users):
    emails = []
    for u in users:
        try:
            emails.append(u['profile']['email'])
        except:
            pass
    return emails


def find_user_by_email(users, email):
    for user in users:
        try:
            if user['profile']['email'] == email:
                return user
        except:
            pass

# Initial users list
users = [
    {
        "color": "757575",
        "deleted": False,
        "id": "USLACKBOT",
        "is_admin": False,
        "is_app_user": False,
        "is_bot": False,
        "is_owner": False,
        "is_primary_owner": False,
        "is_restricted": False,
        "is_ultra_restricted": False,
        "name": "slackbot",
        "profile": {
            "always_active": True,
            "avatar_hash": "sv1444671949",
            "display_name": "slackbot",
            "display_name_normalized": "slackbot",
            "fields": None,
            "first_name": "slackbot",
            "image_192": "https://cfr.slack-edge.com/66f9/img/slackbot_192.png",
            "image_24": "https://cfr.slack-edge.com/0180/img/slackbot_24.png",
            "image_32": "https://cfr.slack-edge.com/7f1a0/plugins/slackbot/assets/service_32.png",
            "image_48": "https://cfr.slack-edge.com/7f1a0/plugins/slackbot/assets/service_48.png",
            "image_512": "https://cfr.slack-edge.com/1801/img/slackbot_512.png",
            "image_72": "https://cfr.slack-edge.com/0180/img/slackbot_72.png",
            "last_name": "",
            "phone": "",
            "real_name": "slackbot",
            "real_name_normalized": "slackbot",
            "skype": "",
            "status_emoji": "",
            "status_expiration": 0,
            "status_text": "",
            "status_text_canonical": "",
            "team": "TBBP6HRC6",
            "title": ""
        },
        "real_name": "slackbot",
        "team_id": "TBBP6HRC6",
        "tz": None,
        "tz_label": "Pacific Daylight Time",
        "tz_offset": -25200,
        "updated": 0
    }
]

# Initial channels list
invited = [
]


# Object used to populate user on invite
user_template = {
    "color": "9f69e7",
    "deleted": False,
    "has_2fa": False,
    "id": "UABCDEFGH",
    "is_admin": True,
    "is_app_user": False,
    "is_bot": False,
    "is_owner": True,
    "is_primary_owner": True,
    "is_restricted": False,
    "is_ultra_restricted": False,
    "name": "user",
    "profile": {
        "avatar_hash": "sv1444671949",
        "display_name": "A User",
        "display_name_normalized": "A User",
        "email": "user@localhost",
        "image_192": "https://cfr.slack-edge.com/66f9/img/slackbot_192.png",
        "image_24": "https://cfr.slack-edge.com/0180/img/slackbot_24.png",
        "image_32": "https://cfr.slack-edge.com/7f1a0/plugins/slackbot/assets/service_32.png",
        "image_48": "https://cfr.slack-edge.com/7f1a0/plugins/slackbot/assets/service_48.png",
        "image_512": "https://cfr.slack-edge.com/1801/img/slackbot_512.png",
        "image_72": "https://cfr.slack-edge.com/0180/img/slackbot_72.png",
        "phone": "",
        "real_name": "A User",
        "real_name_normalized": "A User",
        "skype": "",
        "status_emoji": "",
        "status_expiration": 0,
        "status_text": "",
        "status_text_canonical": "",
        "team": team_id,
        "title": ""
    },
    "real_name": "A User",
    "team_id": team_id,
    "tz": "Europe/London",
    "tz_label": "British Summer Time",
    "tz_offset": 3600,
    "updated": 1529499351
}


@app.route("/api/auth.test", methods=['POST'])
def auth_test():
    return jsonify(
        {
            "ok": True,
            "team": "stub",
            "team_id": team_id,
            "url": "https://stub.local/",
            "user": "stub",
            "user_id": generate_user_id()
        }
    )


@app.route("/api/users.list", methods=['POST'])
def users_list():
    response_users = users

    """
        members = [
            {"id": 1},
            {"id": 2},
            {"id": 3}
        ]

        api_call('users.list', data={"limit": 1, "cursor": "base64(user:2)"})
        > {
            "members": {"id": 2},
            "next_cursor": base64(user:3),
            "offset": base64(user:3)
        }
    """
    response = {
        "cache_ts": int(time.time()),
        "ok": True
    }

    cursor = request.form.get('cursor', '')
    if cursor:
        # find user by cursor, go from there
        user_id = base64.b64decode(cursor).decode('utf-8')
        index = ['user:' + u['id'] for u in response_users].index(user_id)
        app.logger.debug('cursor index: {}'.format(index))
        response_users = response_users[index:]

    if 'limit' in request.form.keys():
        limit = int(request.form['limit'])

        if len(response_users) > limit:
            next_id = response_users[limit]['id']
            response_users = response_users[:limit]
            response['offset'] = next_id
            next_cursor = 'user:' + next_id
            response['response_metadata'] = {'next_cursor': base64.b64encode(next_cursor.encode('utf-8')).decode('utf-8')}
        else:
            response['response_metadata'] = {'next_cursor': ''}

        response_users = response_users[:limit]

    response['members'] = response_users

    return jsonify(
        response
    )


@app.route("/api/users.admin.invite", methods=['POST'])
def users_admin_invite():
    email = request.form['email']
    user_emails = get_emails(users)

    if email in user_emails:
        return jsonify(
            {
                "error": "already_in_team",
                "ok": False
            }
        )
    elif email in invited:
        return jsonify(
            {
                "error": "already_invited",
                "ok": False
            }
        )
    else:
        invited.append(email)

        app.logger.debug('invited: {}'.format(invited))

        return jsonify(
            {
                "ok": True
            }
        )


@app.route("/api/users.admin.setInactive", methods=['POST'])
def users_admin_set_inactive():
    user_id = request.form['user']
    for u in users:
        if u['id'] == user_id:
            user = u
            break
    # FIXME user not found
    user['deleted'] = True
    return jsonify(
        {
            "ok": True
        }
    )


@app.route("/meta/invite.accept", methods=['POST'])
def meta_invite_accept():
    email = request.form['email']
    invited.remove(email)

    new_user = deepcopy(user_template)
    new_user['profile']['email'] = email
    new_user['id'] = generate_user_id()
    users.append(new_user)

    app.logger.debug('users: {}'.format(get_emails(users)))
    app.logger.debug('invited: {}'.format(invited))

    return jsonify(
        {
            "ok": True
        }
    )


@app.route("/meta/invite.accept.all", methods=['POST'])
def meta_invite_accept_all():
    global invited
    app.logger.debug('invited: {}'.format(invited))

    for email in invited:
        app.logger.debug('accepting: {}'.format(email))
        new_user = deepcopy(user_template)
        new_user['profile']['email'] = email
        new_user['id'] = generate_user_id()
        users.append(new_user)

    invited = []

    app.logger.debug('users: {}'.format(get_emails(users)))
    app.logger.debug('invited: {}'.format(invited))

    return jsonify(
        {
            "ok": True
        }
    )



if __name__ == '__main__':
    app.run('0.0.0.0')
