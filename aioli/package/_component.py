# -*- coding: utf-8 -*-

from aioli.utils.http import format_path


class Component:
    pkg = None
    log = None

    @classmethod
    def _pkg_bind(cls, pkg):
        cls.pkg = pkg
        cls.log = pkg.log

    async def on_ready(self):
        """Called upon initialization"""

    def __repr__(self):
        return f'<{self.__class__.__name__} at {hex(id(self))}>'
