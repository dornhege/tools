\#ifndef ${windownameupper}_WINDOW_H
\#define ${windownameupper}_WINDOW_H

\#include <QMainWindow>
\#include "ui_${windowname}Window.h"

class ${windowname}Window : public QMainWindow, protected Ui::${windowname}Window
{
    Q_OBJECT

    public:
        ${windowname}Window();
        ~${windowname}Window();

};

\#endif

