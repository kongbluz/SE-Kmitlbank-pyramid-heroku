from .securitys.security import RootFactory

def includeme(config):
    config.add_static_view(name='css', path='bin:static/css', cache_max_age=3600)
    config.add_static_view(name='images', path='bin:static/images', cache_max_age=3600)
    config.add_static_view(name='js', path='bin:static/js', cache_max_age=3600)
    config.add_route('home','/')
    config.add_route('login','/login')
    config.add_route('logout','/logout')
    config.add_route('service','/service')
    config.add_route('contact','/contact')
    config.add_route('about','/about')
    config.add_route('register','/register')
    config.add_route('success', '/register/success')
    config.add_route('accountregister','/accountregister')
    config.add_route('news', '/news/linkto/{ifd}')

    config.add_route('profile','/profile', factory = RootFactory)
    config.add_route('transfer','/transfer', factory = RootFactory)
    config.add_route('loan','/loan', factory = RootFactory)
    config.add_route('transaction', '/transaction', factory = RootFactory)
    config.add_route('autopay', '/autopay', factory = RootFactory)

    config.add_route('trade', '/service/trade')
    config.add_route('addpp','/service/prompay/add')
    config.add_route('tradepp', '/service/prompay/trade')

    config.add_route('news_view', '/news/view/{ifd}', factory = RootFactory)
    config.add_route('news_add', '/news/add', factory = RootFactory)
    config.add_route('news_delete', 'news/delete/{ifd}', factory = RootFactory)
    config.add_route('list_news', '/news/lists', factory = RootFactory)
    config.add_static_view('deform_static', 'deform:static/')
