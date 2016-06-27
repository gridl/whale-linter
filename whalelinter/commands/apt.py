#!/usr/bin/env python3
from whalelinter.app        import App
from whalelinter.dispatcher import Dispatcher
from whalelinter.commands.command import PackageManager


@Dispatcher.register(token='run', command='apt-get')
@Dispatcher.register(token='run', command='apt')
class Apt(PackageManager):

    @staticmethod
    def remove(lst, element):
        ret = False
        if element in lst:
            lst.remove(element)
            ret = True

        return ret

    _callbacks = {}

    def __init__(self, token, command, args, line):
        PackageManager.__init__(self, token, command, args, line)

        Apt.register(self)(type(self).install)
        Apt.register(self)(type(self).is_parameter_present, name='install', parameter='-y', args=args)
        Apt.register(self)(type(self).is_parameter_present, name='install', parameter='--no-install-recommends', args=args)
        Apt.register(self)(type(self).upgrade)
        Apt.register(self)(type(self).dist_upgrade, name='dist-upgrade')

        for method in self.methods:
            if self.subcommand == method:
                self.react(method)

    def install(self):
        for idx, package in enumerate(self.packages):
            if '=' not in package:
                App._collecter.throw(3003, self.line_number, keys={'package': package})
            else:
                self.packages[idx] = package.split('=')[0]

        if sorted(self.packages) != self.packages:
            App._collecter.throw(3002)

    def upgrade(self):
        App._collecter.throw(2008, self.line_number)

        for idx, package in enumerate(self.packages):
            if '=' not in package:
                App._collecter.throw(3003, self.line_number, keys={'package': package})
            else:
                packages[idx] = package.split('=')[0]

        if self.packages and sorted(self.packages) == self.packages:
            App._collecter.throw(3002)

    def dist_upgrade(self):
        App._collecter.throw(2011, self.line_number)
