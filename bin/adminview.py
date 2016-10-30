import colander
import deform.widget

from pyramid.httpexceptions import HTTPFound
from pyramid.decorator import reify
from .models.models import DBSession, Forum
from pyramid.security import authenticated_userid
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
    )

import datetime

class WikiPage(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    detail = colander.SchemaNode(
    colander.String(),
    widget=deform.widget.RichTextWidget()
)

class Adminview(object):
    def __init__(self, request):
        self.request = request
        self.logged_in = authenticated_userid(self.request)

    @reify
    def news_form(self):
        schema = WikiPage()
        return deform.Form(schema, buttons=('submit',))

    @reify
    def reqts(self):
        return self.news_form.get_widget_resources()

    @view_config(route_name='news_add', permission='editor', renderer='templates/adminforum/news_add.pt')
    def news_add(self):
        form = self.news_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.news_form.validate(controls)
            except deform.ValidationFailure as e:
                # Form is NOT valid
                return dict(title='Add Wiki Page', form=e.render())
            # Add a new page to the database
            new_title = appstruct['title']
            new_detail = appstruct['detail']
            DBSession.add(Forum(new_title, new_detail, datetime.datetime.now()))
            # Get the new ID and redirect
            page = DBSession.query(Forum).filter_by(title=new_title).one()
            new_ifd = page.ifd
            url = self.request.route_url('news_view', ifd=new_ifd)
            return HTTPFound(url)
        return dict(title='Add News Page', form=self.news_form.render())

    @view_config(route_name='news_delete', permission='editor')
    def news_delete(self):
        ifd = int(self.request.matchdict['ifd'])
        thisnews =  DBSession.query(Forum).filter_by(ifd=ifd).one()
        DBSession.delete(thisnews)

        url = self.request.route_url('list_news')
        return HTTPFound(url)

    @view_config(route_name='news_view', permission='editor', renderer='templates/adminforum/news_view.pt')
    def news_view(self):
        ifd = int(self.request.matchdict['ifd'])
        page = DBSession.query(Forum).filter_by(ifd=ifd).one()
        return dict(page=page, title=page.title)

    @view_config(route_name='list_news', permission='editor', renderer='templates/adminforum/list_news.pt')
    def list_news(self):
        pages = DBSession.query(Forum).order_by(Forum.createdtime.desc())
        return dict(title='Welcome to the Wiki', pages=pages)
