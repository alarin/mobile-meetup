from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs this project as a FastCGI application. Requires flup."
    args = '[various KEY=val options, use `runfcgi help` for help]'

    def handle(self, *args, **options):
        from django.conf import settings
        from django.utils import translation
        # Activate the current language, because it won't get activated later.
        try:
            translation.activate(settings.LANGUAGE_CODE)
        except AttributeError:
            pass
        runfastcgi(args)

    def usage(self, subcommand):
        from django.core.servers.fastcgi import FASTCGI_HELP
        return FASTCGI_HELP


def runfastcgi(argset=[], **kwargs):
    import os
    import newrelic
    
    from django.core.servers.fastcgi import FASTCGI_OPTIONS
    from django.conf import settings
    from django.core.servers.fastcgi import fastcgi_help

    options = FASTCGI_OPTIONS.copy()
    options.update(kwargs)
    for x in argset:
        if "=" in x:
            k, v = x.split('=', 1)
        else:
            k, v = x, True
        options[k.lower()] = v

    if "help" in options:
        return fastcgi_help()

    try:
        import flup
    except ImportError, e:
        print >> sys.stderr, "ERROR: %s" % e
        print >> sys.stderr, "  Unable to load the flup package.  In order to run django"
        print >> sys.stderr, "  as a FastCGI application, you will need to get flup from"
        print >> sys.stderr, "  http://www.saddi.com/software/flup/   If you've already"
        print >> sys.stderr, "  installed flup, then make sure you have it in your PYTHONPATH."
        return False

    flup_module = 'server.' + options['protocol']

    if options['method'] in ('prefork', 'fork'):
        wsgi_opts = {
            'maxSpare': int(options["maxspare"]),
            'minSpare': int(options["minspare"]),
            'maxChildren': int(options["maxchildren"]),
            'maxRequests': int(options["maxrequests"]),
        }
        flup_module += '_fork'
    elif options['method'] in ('thread', 'threaded'):
        wsgi_opts = {
            'maxSpare': int(options["maxspare"]),
            'minSpare': int(options["minspare"]),
            'maxThreads': int(options["maxchildren"]),
        }
    else:
        return fastcgi_help("ERROR: Implementation must be one of prefork or thread.")

    wsgi_opts['debug'] = options['debug'] is not None

    try:
        import importlib
        module = importlib.import_module('.%s' % flup_module, 'flup')
        WSGIServer = module.WSGIServer
    except:
        print "Can't import flup." + flup_module
        raise
        return False

    # Prep up and go
    from django.core.handlers.wsgi import WSGIHandler

    if options["host"] and options["port"] and not options["socket"]:
        wsgi_opts['bindAddress'] = (options["host"], int(options["port"]))
    elif options["socket"] and not options["host"] and not options["port"]:
        wsgi_opts['bindAddress'] = options["socket"]
    elif not options["socket"] and not options["host"] and not options["port"]:
        wsgi_opts['bindAddress'] = None
    else:
        return fastcgi_help("Invalid combination of host, port, socket.")

    if options["daemonize"] is None:
        # Default to daemonizing if we're running on a socket/named pipe.
        daemonize = (wsgi_opts['bindAddress'] is not None)
    else:
        if options["daemonize"].lower() in ('true', 'yes', 't'):
            daemonize = True
        elif options["daemonize"].lower() in ('false', 'no', 'f'):
            daemonize = False
        else:
            return fastcgi_help("ERROR: Invalid option for daemonize parameter.")

    daemon_kwargs = {}
    if options['outlog']:
        daemon_kwargs['out_log'] = options['outlog']
    if options['errlog']:
        daemon_kwargs['err_log'] = options['errlog']
    if options['umask']:
        daemon_kwargs['umask'] = int(options['umask'], 8)

    if daemonize:
        from django.utils.daemonize import become_daemon
        become_daemon(our_home_dir=options["workdir"], **daemon_kwargs)

    if options["pidfile"]:
        fp = open(options["pidfile"], "w")
        fp.write("%d\n" % os.getpid())
        fp.close()

    import newrelic.agent
    newrelic.agent.initialize(os.path.join(settings.PROJECT_PATH, 'newrelic.ini'))

    handler = WSGIHandler()
    handler = newrelic.agent.wsgi_application()(handler)
    WSGIServer(handler, **wsgi_opts).run()