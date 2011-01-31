# 
# namcap rules - pkgname
# Copyright (C) 2009 Hugo Doria <hugo@archlinux.org>
# 
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from Namcap.ruleclass import *

class package(PkgInfoRule):
	def short_name(self):
		return "pkgnameindesc"
	def long_name(self):
		return "Verifies if the package name is included on package description"
	def analyze(self, pkginfo, tar):
		ret = [[], [], []]
		if hasattr(pkginfo, 'name') and hasattr(pkginfo, 'desc'):
			if pkginfo.name.lower() in pkginfo.desc.lower().split():
				ret[1].append(("pkgname-in-description", ()))
		return ret

# vim: set ts=4 sw=4 noet:
