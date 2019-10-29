.. _resourcesComputing:

Resources / Computing
=====================

In this section options for ComputingElements can be set


Location for Parameters
-----------------------

Options for computing elements can be set at different levels, from lowest to
highest prority

  /Resources/Computing/OSCompatibility

This section is used to define a compatibility matrix between dirac platforms (:ref:`dirac-platform`) and OS versions.

An example of this session is the following::

    OSCompatibility
    {
      Linux_x86_64_glibc-2.5 = x86_64_CentOS_Carbon_6.6
      Linux_x86_64_glibc-2.5 += x86_64_CentOS_Carbon_6.7
      Linux_x86_64_glibc-2.5 += x86_64_CentOS_Core_7.4
      Linux_x86_64_glibc-2.5 += x86_64_CentOS_Core_7.5
      Linux_x86_64_glibc-2.5 += x86_64_CentOS_Final_6.4
      Linux_x86_64_glibc-2.5 += x86_64_CentOS_Final_6.7
      Linux_x86_64_glibc-2.5 += x86_64_CentOS_Final_6.9
      Linux_x86_64_glibc-2.5 += x86_64_CentOS_Final_7.4
      Linux_x86_64_glibc-2.5 += x86_64_CentOS_Final_7.5
      Linux_x86_64_glibc-2.5 += x86_64_RedHatEnterpriseLinuxServer_6.7_Santiago
      Linux_x86_64_glibc-2.5 += x86_64_RedHatEnterpriseLinuxServer_7.2_Maipo
      Linux_x86_64_glibc-2.5 += x86_64_Scientific_6_6.9
      Linux_x86_64_glibc-2.5 += x86_64_Scientific_Carbon_6.8
      Linux_x86_64_glibc-2.5 += x86_64_Scientific_Carbon_6.9
      Linux_x86_64_glibc-2.5 += x86_64_ScientificCERNSLC_Boron_6.5
      Linux_x86_64_glibc-2.5 += x86_64_ScientificCERNSLC_Carbon_6.3
      Linux_x86_64_glibc-2.5 += x86_64_ScientificCERNSLC_Carbon_6.4
      Linux_x86_64_glibc-2.5 += x86_64_ScientificCERNSLC_Carbon_6.5
      Linux_x86_64_glibc-2.5 += x86_64_ScientificCERNSLC_Carbon_6.6
      Linux_x86_64_glibc-2.5 += x86_64_ScientificCERNSLC_Carbon_6.7
      Linux_x86_64_glibc-2.5 += x86_64_ScientificCERNSLC_Carbon_6.9
      Linux_x86_64_glibc-2.5 += x86_64_ScientificLinux-6.9_0_0
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Boron_6.4
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Carbon_6.10
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Carbon_6.3
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Carbon_6.4
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Carbon_6.5
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Carbon_6.6
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Carbon_6.7
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Carbon_6.8
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Carbon_6.9
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Carbon_6x
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Carbon_6.x
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_Nitrogen_7.4
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_SL_6.4
      Linux_x86_64_glibc-2.5 += x86_64_ScientificSL_SL_6.5
      Linux_x86_64_glibc-2.5 += x86_64_SL_Nitrogen_7.2
    }

What's on the left is an example of a dirac platform as determined the dirac-platform script (:ref:`dirac-platform`). 
This platform is declared to be compatible with a list of "OS" strings.
These strings are identifying the architectures of computing elements.
This list of strings can be constructed from the "Architecture" + "OS" fields
that can be found in the CEs description in the CS (:ref:`cs-sites`).

This compatibility is, by default, used by the SiteDirector when deciding if to send a pilot or not to a certain CE:
the SiteDirector matches "TaskQueues" to Computing Element capabilities.

Other subsections are instead used to describe specific types of computing elements:

  /Resources/Computing/CEDefaults
   For all computing elements
  /Resources/Computing/<CEType>
   For CEs of a given type, e.g., HTCondorCE or ARC
  /Resources/Sites/<grid>/<site>/CEs
   For all CEs at a given site
  /Resources/Sites/<grid>/<site>/CEs/<CEName>
   For the specific CE

Values are overwritten.


General Parameters
------------------

These parameters are valid for all types of computing elements

+---------------------------------+------------------------------------------------+-----------------------------------+
| **Name**                        | **Description**                                | **Example**                       |
+---------------------------------+------------------------------------------------+-----------------------------------+
| GridEnv                         |Default environment file sourced before calling | /opt/dirac/gridenv                |
|                                 |grid commands, without extension '.sh'.         | (when the file is gridenv.sh)     |
+---------------------------------+------------------------------------------------+-----------------------------------+




ARC CE Parameters
-----------------

+---------------------------------+---------------------------------------------------+-------------------------------------------------------------+
| **Name**                        | **Description**                                   | **Example**                                                 |
+---------------------------------+---------------------------------------------------+-------------------------------------------------------------+
| XRSLExtraString                 |  Default additional string for ARC submit files   |                                                             |
+---------------------------------+---------------------------------------------------+-------------------------------------------------------------+
| XRSLMPExtraString               | Default additional string for ARC submit files    |                                                             |
|                                 | for multi-processor jobs.                         |                                                             |
+---------------------------------+---------------------------------------------------+-------------------------------------------------------------+
| Host                            | The host for the ARC CE, used to overwrite the    |                                                             |
|                                 | ce name                                           |                                                             |
+---------------------------------+---------------------------------------------------+-------------------------------------------------------------+
| WorkingDirectory                | Directory where the pilot log files are stored    |   /opt/dirac/pro/runit/WorkloadManagement/SiteDirectorArc   |
|                                 | locally.                                          |                                                             |
+---------------------------------+---------------------------------------------------+-------------------------------------------------------------+


Singularity CE Parameters
-------------------------

+------------------------+--------+----------------------------------------------------------+---------------------------------------------+
| **Name**               | **Description**                                                   |  **Example**                                |
+------------------------+--------+----------------------------------------------------------+---------------------------------------------+
| ContainerRoot          | The root image location for the container to use.                 |  /cvmfs/cernvm-prod.cern.ch/cvm3            |
+------------------------+--------+----------------------------------------------------------+---------------------------------------------+
| ContainerExtraOpts     | Extra options for dirac-install within the container.             |  -u 'http://other.host/instdir' -g 'v13r0'  |
+------------------------+--------+----------------------------------------------------------+---------------------------------------------+
| KeepWorkArea           | If set to True container work area won't be deleted at end of job |  True (Default: False)                      |
+------------------------+--------+----------------------------------------------------------+---------------------------------------------+



.. _res-comp-htcondor:

HTCondorCE Parameters
---------------------

Options for the HTCondorCEs

+---------------------+-----------------------------------------------------+-----------------------------------------------------------+
| **Name**            | **Description**                                     | **Example**                                               |
+---------------------+-----------------------------------------------------+-----------------------------------------------------------+
| ExtraSubmitString   | Additional string for the condor submit             | request_cpus = 8 \\n periodic_remove = ...                |
|                     | file. Separate entries with "\\n".                  |                                                           |
+---------------------+-----------------------------------------------------+-----------------------------------------------------------+
| WorkingDirectory    | Directory where the pilot log files are stored      | /opt/dirac/pro/runit/WorkloadManagement/SiteDirectorHT    |
|                     | locally. Also temproray files like condor submit    |                                                           |
|                     | files are kept here. This option is only read from  |                                                           |
|                     | the global Resources/Computing/HTCondorCE location. |                                                           |
+---------------------+-----------------------------------------------------+-----------------------------------------------------------+
| UseLocalSchedd      | If True use a local condor schedd to submit jobs, if| Default is True                                           |
|                     | False submit to remote condor schedd                |                                                           |
+---------------------+-----------------------------------------------------+-----------------------------------------------------------+
| DaysToKeepLogFiles  | How many days pilot log files are kept on the disk  | 15                                                        |
|                     | before they are removed                             |                                                           |
+---------------------+-----------------------------------------------------+-----------------------------------------------------------+


.. _res-comp-cream:

CREAM CE Parameters
-------------------

+---------------------+-----------------------------------------------------+-----------------------------------------------------------+
| **Name**            | **Description**                                     | **Example**                                               |
+---------------------+-----------------------------------------------------+-----------------------------------------------------------+
| ExtraJDLParameters  | Additional JDL parameters to submit pilot jobs      | ExtraJDLParameters = GPUNumber=1; OneMore="value"         |
|                     | to CREAm CE. Separate entries with ";".             |                                                           |
+---------------------+-----------------------------------------------------+-----------------------------------------------------------+
