#!/usr/bin/env python

from Cheetah.Template import Template
import sys

package_dir = sys.argv[1]
window_name = sys.argv[2]
window_name_cap = window_name.upper()
template_base_dir = sys.argv[3]

print "Creating files in:", package_dir, "for windowname:", window_name

replacements = [{'windowname' : window_name,
                'windownameupper' : window_name_cap,
                'packagename' : package_dir}]

cmake_template = Template(file=template_base_dir + "/templates/CMakeLists.txt", searchList=replacements)
f = file(package_dir + "/CMakeLists.txt", 'w')
f.write(str(cmake_template))
f.close()

main_template = Template(file=template_base_dir + "/templates/main.cpp", searchList=replacements)
f = file(package_dir + "/src/main.cpp", 'w')
f.write(str(main_template))
f.close()

ui_template = Template(file=template_base_dir + "/templates/mainWindow.ui", searchList=replacements)
f = file(package_dir + "/src/" + window_name + "Window.ui", 'w')
f.write(str(ui_template))
f.close()

header_template = Template(file=template_base_dir + "/templates/mainWindow.h", searchList=replacements)
f = file(package_dir + "/src/" + window_name + "Window.h", 'w')
f.write(str(header_template))
f.close()

cpp_template = Template(file=template_base_dir + "/templates/mainWindow.cpp", searchList=replacements)
f = file(package_dir + "/src/" + window_name + "Window.cpp", 'w')
f.write(str(cpp_template))
f.close()

