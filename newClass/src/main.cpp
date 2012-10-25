#include <qstring.h>
#include <qstringlist.h>
#include <qregexp.h>
#include <qfile.h>
//#include <qdom.h>
//Added by qt3to4:
#include <Q3TextStream>
#include <stdlib.h>

#include <sys/stat.h>

#include <iostream>
#include <vector>
using namespace std;

bool g_verbose = false;

void printUsage()
{
   cout << "\nOptions:\n" << endl;
   cout << "--------------" << endl;
   cout << "newClass MyNewClass" << endl;
}

int main(int argc, char **argv)
{
   bool insertConstructors = false;

   char c;
   while((c = getopt(argc, argv, "ch")) != EOF)
   {
      switch(c)
      {
         case 'c':
            insertConstructors = true;
            break;
         case 'h':
         default:
            printf("\nSyntax: newClass [Options] ClassName\n");
            printf("-c insert constructors\n");
            printf("--------------\n");
            printf("-h this help\n\n");
            exit(0);
            break;
      }
   }

   if(optind < 0) {
      printUsage();
      exit(1);
   }
   char* className = argv[optind];

   QString cn = className;

   //cout << cn << endl;

   QString first = cn.mid(0, 1);
   QString rest = cn.mid(1);

   QString lower = first.lower() + rest;

   QString headerName = lower + ".h";
   QString sourceName = lower + ".cpp";

   cout << "Creating class <" << qPrintable(cn) << "> in " << qPrintable(headerName) << " and " << qPrintable(sourceName) << endl;
   cout << "Constructors inserted." << endl;

   QRegExp r("([A-Z])");
   QString hCopy = headerName;
   QString caps = hCopy.replace(r, "_\\1");
   caps = caps.replace(".", "_").upper();
   //cout << caps;

   QString headerTxt = "#ifndef " + caps + "\n" 
      + "#define " + caps + "\n\n"
      + "class " + cn + "\n"
      + "{\n   public:\n";
      if(insertConstructors) {
         headerTxt += "      " + cn + "();\n"
            + "      ~" + cn + "();\n";
      }
      headerTxt = headerTxt + "\n};\n\n"
      + "#endif\n\n";

   QString srcTxt = "#include \"" + headerName + "\"\n"
      + "\n";
   if(insertConstructors) {
      srcTxt += cn + "::" + cn + "()\n"
         + "{\n\n}\n"
         + "\n"
         + cn + "::~" + cn + "()\n"
         + "{\n\n}\n"
         + "\n";
   }
/*
   cout << "Header: " << headerName << endl;
   cout << headerTxt;
   cout << "Source: " << sourceName << endl;
   cout << srcTxt;
*/

   struct stat sStat;
   if(stat(headerName.latin1(), &sStat) == 0) {
      printf("File: <%s> already exists, aborting.\n", headerName.latin1());
      exit(1);
   }
   if(stat(sourceName.latin1(), &sStat) == 0) {
      printf("File: <%s> already exists, aborting.\n", sourceName.latin1());
      exit(1);
   }

   QFile header(headerName);
   if(!header.open(QIODevice::WriteOnly)) {
      printf("err\n");
      return 1;
   }
   Q3TextStream s(&header);
   s << headerTxt;
   header.close();

   QFile source(sourceName);
   if(!source.open(QIODevice::WriteOnly)) {
      printf("err\n");
      return 1;
   }
   Q3TextStream s2(&source);
   s2 << srcTxt;
   source.close();

   return 0;
}

