#!/usr/bin/env python
# encoding: utf-8

from Alfred import Items, Tools
from collections import Counter, OrderedDict
from Plist import Plist
import os

def get_selection(key, query):
    variables = get_variables()
    if key in variables:
        v = variables[key]
        isValid = False if query == str() else True
        items.setItem(
            arg = u"set|{0}|{1}".format(key, query),
            quicklookurl = u"{0}/docs/{1}.md".format(workflow_dir, key),
            subtitle = u"Add new value and press enter (\u2318 Delete value, \u21E7 for Help)",
            title = "Change {0}: {1}".format(key, v),
            valid = isValid,
        )
        items.addMod(
            arg = 'set|{0}|'.format(key),
            key = 'cmd',
            subtitle = 'Delete Value',
        )
        items.setIcon('icons/edit.png', 'image')
        items.addItem()
    else:
        items.setItem(
            title = "Variable not found",
            valid = False
        )
        items.addItem()

def get_variables():
    config = Plist().getConfig()
    return OrderedDict(sorted(config.items()))

def print_config(query):
    variables = get_variables()
    for variable, value in variables.items():
        if query == str() or query in variable:
            v_subtitle = '<EMPTY>' if value == str() else value
            items.setItem(
                arg = u"selection|{0}|{1}".format(variable, value),
                quicklookurl = u"{0}/docs/{1}.md".format(workflow_dir, variable),
                subtitle = u"Value: {0} (\u21E7 for Help)".format(v_subtitle),
                title = variable,
            )
            icon = 'icons/check.png' if value != str() else 'icons/question.png'
            items.setIcon(icon, 'image')
            items.addItem()

def write_config(key, val):
    value = Tools.normalize(val)
    Plist().setVariable(key, value)

query = Tools.getArgv(1)
action_key_value = Tools.getEnv('action_key_value')
[action, key, value] = action_key_value.split('|') if action_key_value != str() else [str(), str(), str()]
workflow_dir = os.getcwd()
query = Tools.getArgv(1)

items = Items()

if action == str():
    print_config(query)
elif action == 'selection':
    get_selection(key, query)
else:
    write_config(key, value)
    print_config(query)

items.write()
