\#include <QApplication>
\#include "${windowname}Window.h"
\#include <ros/ros.h>

int main(int argc, char** argv)
{
    ros::init(argc, argv, "${packagename}");

    QApplication app(argc, argv);

    ros::NodeHandle nh;

    ${windowname}Window mw;
    mw.show();

    ros::Rate loopRate(10.0);
    while(ros::ok()) {
        ros::spinOnce();
        app.processEvents();

        loopRate.sleep();
    }

    return 0;
}
