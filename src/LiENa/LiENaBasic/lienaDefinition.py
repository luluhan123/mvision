#  -----------------------------------------------------------------------------------------------------------------------
#  LIENa distributed device ID
#  -----------------------------------------------------------------------------------------------------------------------
SIAT_COCKPIT_VERSION_1 = 0  # hand
SIEMENS_CBCT_ARCADIS_ORBIC_VERSION_1 = 536870912  # eye
MEDSIGHT_INTERVENTIONAL_VASCULAR_ROBOT_VERSION_1 = 1073741824  # brain

#  -----------------------------------------------------------------------------------------------------------------------
#  Real-time session management
#  -----------------------------------------------------------------------------------------------------------------------
LIENA_SESSION_MANAGEMENT_HANDSHAKE_MESSAGE = 0
LIENA_SESSION_MANAGEMENT_HANDSHAKE_COMMIT_MESSAGE = 1
LIENA_SESSION_MANAGEMENT_CHANNEL_OPENED_MESSAGE = 2
LIENA_SESSION_MANAGEMENT_DISENGAGEMENT_MESSAGE = 3
LIENA_SESSION_MANAGEMENT_DISENGAGEMENTCOMMIT_MESSAGE = 4
LIENA_SESSION_MANAGEMENT_CHANNEL_CLOSED_MESSAGE = 5
LIENA_SESSION_MANAGEMENT_REHANDSHAKE_MESSAGE = 6
LIENA_SESSION_MANAGEMENT_REHANDSHAKECOMMIT_MESSAGE = 7
LIENA_SESSION_MANAGEMENT_CHANNEL_REOPENED_MESSAGE = 8

LIENA_SESSION_MANAGEMENT_CLOSE_SYSTEM_MESSAGE = 3145728
LIENA_SESSION_MANAGEMENT_OPEN_SYSTEM_MESSAGE = 3145729
LIENA_SESSION_MANAGEMENT_FREEZE_SYSTEM_MESSAGE = 3145730
LIENA_SESSION_MANAGEMENT_WAKEUP_SYSTEM_MESSAGE = 3145731

LIENA_SESSION_MANAGEMENT_HEARTBEAT_MESSAGE = 2097152
LIENA_SESSION_MANAGEMENT_NTP_CLOCK_SYNCHRONIZATION_MESSAGE = 2097153

#  -----------------------------------------------------------------------------------------------------------------------
#  LIENA Error
#  -----------------------------------------------------------------------------------------------------------------------
LIENA_ERROR_SUCCESS = 0
LIENA_ERROR_LOCAL_CONNEXION_LOST = 1      # Network is unreachable
LIENA_ERROR_PEER_SERVER_NOT_LAUNCHED = 2  # connection refused
LIENA_ERROR_PEER_CONNEXION_LOST = 3       # timed out

#  -----------------------------------------------------------------------------------------------------------------------
#  LIENA static parameter
#  -----------------------------------------------------------------------------------------------------------------------
HEAD_SIZE = 21
DEBUG = 0
