# Copyright 2017 Google Inc. All rights reserved.
# Use of this source code is governed by the Apache 2.0 license that can be
# found in the LICENSE file.
"""Microsoft Internet Explorer testing (based on the Edge support)"""
import os
import platform
from .microsoft_edge import Edge
from .os_util import run_elevated

class InternetExplorer(Edge):
    """Microsoft Edge"""
    def __init__(self, path, options, job):
        Edge.__init__(self, path, options, job)

    def get_driver(self):
        """Get the webdriver instance"""
        from selenium import webdriver
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'support', 'IE')
        reg_file = os.path.join(path, 'keys.reg')
        if os.path.isfile(reg_file):
            run_elevated('reg', 'IMPORT "{0}"'.format(reg_file))
        if platform.machine().endswith('64'):
            path = os.path.join(path, 'amd64', 'IEDriverServer.exe')
        else:
            path = os.path.join(path, 'x86', 'IEDriverServer.exe')
        driver = webdriver.Ie(executable_path=path)
        return driver

    def kill(self):
        """Kill any running instances"""
        processes = ['iexplore.exe', 'smartscreen.exe', 'dllhost.exe']
        for exe in processes:
            try:
                run_elevated('taskkill', '/F /T /IM {0}'.format(exe))
            except Exception:
                pass

    def clear_cache(self):
        """Clear the browser cache"""
        run_elevated('RunDll32.exe', 'InetCpl.cpl,ClearMyTracksByProcess 6655')
