TEMPLATE = app

CONFIG += console debug qt

INCLUDEPATH += .

OBJECTS_DIR = .obj/
MOC_DIR = .obj/

TARGET = newClass
DESTDIR = $(HOME)/bin/

#######################
# C/CPP SOURCES 
#######################
HEADERS += 

SOURCES += \
           src/main.cpp

#The following line was inserted by qt3to4
QT +=  qt3support 
