# -*- coding: utf-8 -*-

import sublime_plugin
import re

class PlaceImageCommand(sublime_plugin.EventListener):
  def on_query_completions(self, view, prefix, locations):
    pi_snip = '<img src="http://placehold.it/${1:300x240}"${2: width="${1/^x?([^x]+)x?.*$/$1/}" height="${1/^([^x]*?)x?([^x]+)x?$/$2/}"} title="PLACE.IT: [${1/^x?([^x]+)x?.*$/$1/} x ${1/^([^x]*?)x?([^x]+)x?$/$2/}]" alt="" />'
    placeit = '<img src="http://placehold.it/%sx%s"${1: width="%s" height="%s"} title="PLACE.IT: [%s x %s]" alt="" />'
    kitten  = '<img src="http://placekitten.com/%s/%s"${1: width="%s" height="%s"} title="KITTEN: [%s x %s]" alt="" />'
    pattern = r'^pi(?:(\d+)(?:(X|x)(\d+))?)?$'
    match   = re.match(pattern, prefix, re.I)

    if match:
      groups = match.groups()
      numNil = groups.count(None)

      if numNil == 3:
        val = pi_snip
      elif numNil == 2:
        width  = groups[0]
        height = width
        val    = placeit % ((width, height) * 3)
      else:
        width  = groups[0]
        height = groups[2]
        tmpl   = kitten if groups[1] == 'X' else placeit
        val    = tmpl % ((width, height) * 3)

    else:
      val = None

    return [(prefix, val)] if val else []
