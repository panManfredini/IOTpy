# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

from twisted.application import app

from twisted.python.runtime import platformType
if platformType == "win32":
    from twisted.scripts._twistw import ServerOptions, \
        WindowsApplicationRunner as _SomeApplicationRunner
else:
    from twisted.scripts._twistd_unix import ServerOptions, \
        UnixApplicationRunner as _SomeApplicationRunner


def run(application):
    config = ServerOptions()
    config.parseOptions()
    runner = _SomeApplicationRunner(config)
    runner.preApplication()
    runner.application = application
    runner.logger.start(application)
    runner.postApplication()
    runner.logger.stop()

    if runner._exitSignal is not None:
        app._exitWithSignal(runner._exitSignal)