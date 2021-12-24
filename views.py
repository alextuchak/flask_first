from flask import request, jsonify
from flask.views import MethodView
from app import app, db
from validator import validate
from models import User
from models import Ads
from schema import USER_CREATE, ADS_CREATE


class UserView(MethodView):

    def get(self, user_id):
        user = User.by_id(user_id)
        return jsonify(user.to_dict())

    @validate('json', USER_CREATE)
    def post(self):
        user = User(**request.json)
        user.set_password(request.json['password'])
        user.add()
        return jsonify(user.to_dict())


class AdsView(MethodView):
    def get(self, ads_id):
        ads = Ads.by_id(ads_id)
        return jsonify(ads.to_dict())

    @validate('json', ADS_CREATE)
    def post(self):
        token = request.headers.get('Authorization')
        user = User.query.filter_by(token=token).all()
        if user:
            ads = Ads(**request.json)
            ads.add()
            return jsonify(ads.to_dict())
        else:
            return {'status': 'auth error'}

    def delete(self, ads_id):
        token = request.headers.get('Authorization')
        user_from_req = User.query.filter_by(token=token).all()
        owner_id = Ads.query.filter_by(id=ads_id).all()
        ads = Ads.query.get(ads_id)
        db.session.delete(ads)
        db.session.commit()
        return {'status': 'deleted'}


@app.route('/health/', methods=['GET', ])
def health():
    if request.method == 'GET':
        return jsonify({'status': 'OK'})

    return {'status': 'OK'}


app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('user_get'), methods=['GET', ])
app.add_url_rule('/users/', view_func=UserView.as_view('users_create'), methods=['POST', ])
app.add_url_rule('/ads/<int:ads_id>', view_func=AdsView.as_view('ads_get'), methods=['GET'],)
app.add_url_rule('/ads/', view_func=AdsView.as_view('ads_post'), methods=['POST'],)
app.add_url_rule('/ads/<int:ads_id>', view_func=AdsView.as_view('ads_delete'), methods=['DELETE'],)
