# -*- coding: utf-8 -*-
# 
# namcap rules - depends
# Copyright (C) 2003-2009 Jason Chu <jason@archlinux.org>
# Copyright (C) 2011 Rémy Oudompheng <remy@archlinux.org>
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

"""Checks dependencies semi-smartly."""

import re
from Namcap.ruleclass import *
import Namcap.tags
from Namcap import package

# manual overrides for relationships outside the normal metadata
implicit_provides = {
	'java-environment': ['java-runtime'],
}

def getcustom(pkginfo):
	custom_name = {'^mingw-': ['mingw-w64-crt'],}
	custom_depend = set()
	for pattern in custom_name:
		if re.search(pattern, pkginfo['name']):
			custom_depend.update(custom_name[pattern])
	return custom_depend

def getprovides(depends):
	provides = {}
	for i in depends:
		provides[i] = set()
		if i in implicit_provides:
			provides[i].update(implicit_provides[i])
		pac = package.load_from_db(i)
		if pac is None:
			continue
		if not pac["provides"]:
			continue
		provides[i].update(pac["provides"])
	return provides

def analyze_depends(pkginfo):
	errors, warnings, infos = [], [], []

	# compute needed dependencies + recursive
	dependlist = set(pkginfo.detected_deps.keys())
	provideslist = getprovides(dependlist)
	# FIXME part of actual or pkg deps?
	customlist = getcustom(pkginfo)
	for i in dependlist:
		infos.append(("dependency-covered-by-link-dependence %s", i))
	needed_depend = dependlist | customlist

	# Find all the covered dependencies from the PKGBUILD
	pkginfo.setdefault("depends", [])
	# FIXME pkginfo should not have dups - add a test
	explicitdepend = set(pkginfo["depends"])
	# Get the provides so we can reference them later
	explicitprovides = getprovides(explicitdepend)

	# Include the optdepends from the PKGBUILD
	pkginfo.setdefault("optdepends", [])
	optdepend = set(pkginfo["optdepends"])

	# The set of all provides for detected dependencies
	allprovides = set()
	for plist in provideslist.values():
		allprovides |= plist

	# Do the actual message outputting stuff
	for i in dependlist:
		# if the needed package is itself:
		if i == pkginfo["name"]:
			continue
		# FIXME: ignore glibc for now, far too many packages are broken
		if i == "glibc":
			continue
		# the dependency is satisfied by a depends
		if i in explicitdepend:
			continue
		# the dependency is satisfied by a provides
		if i in explicitprovides:
			continue
		# the package provides the required dependency
		if i in provideslist and (provideslist[i] & explicitdepend): # FIXME exp provide as well?
			continue
		# compute dependency reason
		reasons = pkginfo.detected_deps[i]
		reason_strings = [Namcap.tags.format_message(reason) for reason in reasons]
		reason = ', '.join(reason_strings)
		# still not found, maybe it is specified as optional
		if i in optdepend:
			warnings.append(("dependency-detected-but-optional %s (%s)", (i, reason)))
			continue
		# maybe, it is pulled as a provider for an optdepend
		if provideslist[i] & optdepend:
			warnings.append(("dependency-detected-but-optional %s (%s)", (i, reason)))
			continue
		# now i'm pretty sure i didn't find it.
		errors.append(("dependency-detected-not-included %s (%s)", (i, reason)))

	for i in explicitdepend:
		# FIXME:
		# - add mandatory dependencies, or
		# - add implicit dep within pacman/makepkg
		# multilib packages must depend on their regular counterparts
		if pkginfo["name"].startswith('lib32-'):
			if i == pkginfo["name"].partition('-')[2]:
				continue
			else:
				errors.append(("multilib-dependency-detected-not-included %s", i))
				continue
		# a dependency is unneeded if:
		#   it is not in the depends as we see them
		#   it does not pull some needed dependency which provides it
		if i not in needed_depend and i not in allprovides:
			warnings.append(("dependency-not-needed %s", i))
	infos.append(("depends-by-namcap-sight depends=(%s)", ' '.join(dependlist) ))

	return errors, warnings, infos

# vim: set ts=4 sw=4 noet:
