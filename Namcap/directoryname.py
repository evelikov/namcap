# 
# namcap rules - directoryname
# Copyright (C) 2003-2007 Jason Chu <jason@archlinux.org>
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

import tarfile

class package:
	def short_name(self):
		return "directoryname"
	def long_name(self):
		return "Checks for standard directories."
	def prereq(self):
		return "tar"
	def analyze(self, pkginfo, tar):
		valid_paths = ['etc/', 'usr/bin/', 'usr/sbin/', 'usr/lib', 'usr/include/', 'usr/man/', 'usr/share/', 'opt/', '.PKGINFO', '.INSTALL', '.FILELIST', '._install', 'usr/X11R6/bin/', 'usr/X11R6/include/', 'usr/X11R6/lib/', 'usr/X11R6/man/', 'usr/X11R6/share/', 'lib', 'sbin/']
		ret = [[],[],[]]
		for i in tar.getnames():
			# Replace multiple /'s at the end of a string with a single /
			# Not sure if this is a python bug or a makepkg bug
			if i.endswith('/'):
				i = i.rstrip('/') + '/'
			fileok = 0
			for j in valid_paths:
				# matches directory names (j, filename) or parent directories (filename, j)
				if i[0:len(j)] == j or j[0:len(i)] == i:
					fileok = 1
			if not fileok:
				ret[1].append("File (" + i + ") exists in a non-standard directory.")
		return ret
	def type(self):
		return "tarball"
