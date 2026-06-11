#!/usr/bin/python3

import rospy
import numpy

from pairs_msgs.msg import ControlManagerDiagnostics
from pairs_msgs.msg import Reference
from pairs_msgs.srv import TrajectoryReferenceSrv,TrajectoryReferenceSrvRequest
from std_srvs.srv import Trigger,TriggerRequest

class Node:

    # #{ __init__(self)

    def __init__(self):

        rospy.init_node("sweeping_generator", anonymous=True)

        ## | --------------------- load parameters -------------------- |

        self.frame_id = rospy.get_param("~frame_id")

        self.heading_rate = rospy.get_param("~heading_rate")

        self.timer_main_rate = rospy.get_param("~timer_main/rate")

        rospy.loginfo('[RoboflyExample]: initialized')

        ## | ----------------------- subscribers ---------------------- |

        self.sub_control_manager_diag = rospy.Subscriber("~control_manager_diag_in", ControlManagerDiagnostics, self.callbackControlManagerDiagnostics)

        ## | --------------------- service clients -------------------- |

        self.sc_trajectory = rospy.ServiceProxy('~trajectory_out', TrajectoryReferenceSrv)

        self.sc_land = rospy.ServiceProxy('~land_out', Trigger)

        ## | ------------------------- timers ------------------------- |

        self.timer_main = rospy.Timer(rospy.Duration(1.0/self.timer_main_rate), self.timerMain)

        ## | -------------------- spin till the end ------------------- |

        self.is_initialized = True

        self.called = False
        self.started = False
        self.finished = False

        rospy.spin()

    # #} end of __init__()

    ## | ------------------------- methods ------------------------ |

    # #{ planTrajectory()

    def planTrajectory(self):

        rospy.loginfo('[RoboflyExample]: planning trajectory')

        # https://ctu-mrs.github.io/pairs_msgs/srv/TrajectoryReference.html
        # -> https://ctu-mrs.github.io/pairs_msgs/srv/TrajectoryReferenceSrv.html
        trajectory_srv = TrajectoryReferenceSrvRequest()

        trajectory_srv.trajectory.header.frame_id = self.frame_id
        trajectory_srv.trajectory.header.stamp = rospy.Time.now()

        trajectory_srv.trajectory.fly_now = True

        trajectory_srv.trajectory.use_heading = True

        duration = 6.28 * (1.0 / self.heading_rate)
        n_steps  = int(duration * 5.0) # 5.0 [s] is the default sampling rate of the trajectory
        step     = 6.28 / n_steps

        for i in range(0, n_steps):

            # https://ctu-mrs.github.io/pairs_msgs/msg/Reference.html
            point = Reference()

            point.position.x = 0
            point.position.y = 0
            point.position.z = 0
            point.heading = i*step

            trajectory_srv.trajectory.points.append(point)

        return trajectory_srv

    # #} end of planTrajectory()

    # #{ land()

    def land(self):

        rospy.loginfo('[RoboflyExample]: landing')

        land_srv = TriggerRequest()

        try:
            response = self.sc_land.call(land_srv)
        except:
            rospy.logerr('[RoboflyExample]: land service not callable')
            pass

    # #} end of load()

    ## | ------------------------ callbacks ----------------------- |

    # #{ callbackControlManagerDiagnostics():

    def callbackControlManagerDiagnostics(self, msg):

        if not self.is_initialized:
            return

        rospy.loginfo_once('[RoboflyExample]: getting ControlManager diagnostics')

        self.sub_control_manager_diag = msg

    # #} end of

    ## | ------------------------- timers ------------------------- |

    # #{ timerMain()

    def timerMain(self, event=None):

        if not self.is_initialized:
            return

        rospy.loginfo_once('[RoboflyExample]: main timer spinning')

        if isinstance(self.sub_control_manager_diag, ControlManagerDiagnostics):

            if self.sub_control_manager_diag.flying_normally and not self.started and not self.finished and not self.called:

                trajectory_srv = self.planTrajectory()

                try:
                    response = self.sc_trajectory.call(trajectory_srv)
                except:
                    rospy.logerr('[RoboflyExample]: trajectory service not callable')
                    pass

                if response.success:

                    rospy.loginfo('[RoboflyExample]: trajectory set')

                    self.called = True

                else:
                    rospy.loginfo('[RoboflyExample]: trajectory setting failed, message: {}'.format(response.message))

                return

            if self.called:

                if self.sub_control_manager_diag.tracker_status.have_goal:

                    self.called = False
                    self.started = True

            if self.started and not self.sub_control_manager_diag.tracker_status.have_goal and not self.finished:

                self.land()

                self.finished = True

                return

    # #} end of timerMain()

if __name__ == '__main__':
    try:
        node = Node()
    except rospy.ROSInterruptException:
        pass
