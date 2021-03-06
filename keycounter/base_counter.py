#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import logging

from .storage import CountDataStorage

__version__ = '0.2.2'


class BaseKeyCounter(object):
    '''Base skeleton for a KeyCounter instance'''

    name = 'KeyCounter'
    version = __version__

    def __init__(self):
        '''
        Init the counter.
        - Load config
        - Setup UI
        - Start event loop
        '''
        self.key_count = 0
        self.daily_reset = True

        self.today = datetime.now()
        self.setup_storage()

    def setup_storage(self):
        self.storage = CountDataStorage()

    def log(self, *args, **kwargs):
        '''Logging'''
        logging.debug(*args, **kwargs)

    def load_config(self):
        '''Load configuration from storage'''
        raise NotImplementedError(u'Should be implemented in subclass')

    def save_config(self):
        '''Save configuration to storage'''
        raise NotImplementedError(u'Should be implemented in subclass')

    def start(self):
        '''Start the event loop'''
        self.key_count = self.load_data(datetime.now())

    def stop(self):
        '''Stop the event loop and save current count'''
        self.save_data(datetime.now(), self.key_count)
        self.storage.export()

    def do_daily_reset(self):
        '''Reset count and start a new day'''
        self.log('Perform daily reset')
        yesterday_count = self.key_count - 1
        self.save_data(self.today, yesterday_count)
        self.storage.export()
        self.key_count -= yesterday_count
        if self.key_count < 0:
            self.key_count = 0
        self.update_ui()

    def load_data(self, day):
        '''Load count data for specific day'''
        return self.storage.get(day)

    def save_data(self, day, count):
        '''Save count data for specific day'''
        self.storage.save(day, count)

    def check_daily_reset(self):
        '''Check whether it's time to do daily reset'''
        now = datetime.now()
        if now.day != self.today.day:
            self.do_daily_reset()
            self.today = now

    def update_count(self):
        '''Update count and reflect the change to UI'''
        self.key_count += 1
        self.update_ui()

    def update_ui(self):
        '''Update user interface'''
        raise NotImplementedError(u'Should be implemented in subclass')

    def handle_keyevent(self, _):
        '''
        Handle key event, properly change count and UI.
        This method should be properly registered to OS's KeyUp event.
        '''
        self.update_count()
        if self.daily_reset:
            self.check_daily_reset()
