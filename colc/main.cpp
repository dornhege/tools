#include <QApplication>
#include <QColorDialog>
#include <QColor>
#include <stdio.h>

int main(int argc, char** argv) {
   QApplication app(argc, argv);

   QColorDialog d;
   d.show();

   int ret = app.exec();

   QColor c = d.selectedColor();
   printf("#%02x%02x%02x\n", c.red(), c.green(), c.blue());
   printf("%d, %d, %d\n", c.red(), c.green(), c.blue());
   printf("%f, %f, %f\n", (double)c.red()/255., (double)c.green()/255., (double)c.blue()/255.);

   return ret;
}
