import json
import re

from flask import Blueprint, url_for, request, redirect, render_template, session

from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, Publishing, Channel

pub_page = Blueprint('publishings', __name__)
@pub_page.route('/moderate/<int:id>/<string:idc>',methods=["GET","POST"])
@login_required()
def moderate_publishing(id,idc):
    pub = db.session.query(Publishing).filter(Publishing.post_id==id,Publishing.channel_id==idc).first()
    chan = db.session.query(Channel).filter(Channel.name == idc).first()
    pub.date_from = str_converter(pub.date_from)
    pub.date_until = str_converter(pub.date_until)
    if request.method=="GET":
        if pub.extra is not None:
            pub.extra = json.loads(pub.extra)
        # add the circles (specific for google+)
        # if chan.module=='superform.plugins.Gplus':
        #     circles = list_circle(chan.config)
        circles = [('domain', 'My Domain (Publish in Public)'), ('1', 'phillliiiipe'), ('2', 'tamere'), ('3', '69'),
                   ('4', '42')]
        return render_template('moderate_post.html', pub=pub, list_circles=circles, module=chan.module)
    else:
        extra = dict()
        if chan.module == "superform.plugins.Gplus":
            extra['disablesharing'] = True if request.form.get("disablesharing") is not None else False
            extra['disablecomments'] = True if request.form.get("disablecomments") is not None else False
            circles = []
            for key in request.form.to_dict().keys():
                if re.match(r".+_circle", key):
                    circles.insert(0, key.split("_")[0])
            extra['circles'] = circles
            pub.extra = json.dumps(extra)
        pub.title = request.form.get('titlepost')
        pub.description = request.form.get('descrpost')
        pub.link_url = request.form.get('linkurlpost')
        pub.image_url = request.form.get('imagepost')
        pub.date_from = datetime_converter(request.form.get('datefrompost'))
        pub.date_until = datetime_converter(request.form.get('dateuntilpost'))
        #state is shared & validated
        pub.state = 1
        db.session.commit()
        #running the plugin here
        c=db.session.query(Channel).filter(Channel.name == pub.channel_id).first()
        plugin_name = c.module
        c_conf = c.config
        from importlib import import_module
        plugin = import_module(plugin_name)
        plugin.run(pub, c_conf)

        return redirect(url_for('index'))

