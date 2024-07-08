# 1. Semestral Project

## Introduction

In this tutorial we will introduce the grading scheme of the course and then discuss the semestral project that students are required to complete to pass the course. The project is selected so that it will enable us to understand the system of security tokens and the User Account Control (UAC) in Windows and to learn how to give-up all unnecessary privileges. Students will also experiment with privilege separation by extracting any high-privileged tasks (e.g. the setting of system time) into a separate process.

## Description

We will be developing a Network Clock (NC) application with the following characteristics:

NC is run as a standard application. It displays the current date and time to the interactive (logged-on) user; the user may specify the exact format of the displayed value by setting a format string interactively. It’s acceptable to only update the display on request.
Additionally, NC listens for communications on a TCP port number defined in a configuration file (or a registry key). A remote user can connect to this port and request the current date and time in a specified format.
The interactive user (but not a remote one) may also set the date/time.
Note that since the application is accessible from the internet, there are many potential attackers waiting to exploit any bug. For this reason, the application should be written with security in mind; particularly, it will use as low privileges as possible.
There is no requirement on the programming language used. It may be beneficial to use a high level language, as a high level language will take care of many of the security issues for you (e.g. most of the buffer overflows, format string abuse etc.). A language with advanced GUI support will also simplify the input validation, because the UI components will handle that. On the other hand, many high-level languages make it difficult to communicate with the operating system’s API, e.g. for the purpose of removing unnecessary privileges.

## Instructions

Any network server code is a prime target for attackers, particularly if the communication protocol is complex and errors can be expected in it. We do not have a protocol specified, that’s up to the developer, but we do have a requirement that the user must be able to supply her own format string. That opens two potential vulnerabilities: Our protocol must be able to handle variable-length strings, which makes it prone to the buffer overflow, and these strings will be used for formatting, which may be used for format string exploitation. Both of these issues need to be addressed properly, otherwise our application won’t be secure. Note that your protocol should be able to deal with split requests (one command is split into multiple TCP packets, e.g. due to the poor quality of the connection used by the user) as well as combined requests (multiple commands got concatenated into a single packet).

It is recommended to use threads to handle the network communication. That would help us in several important aspects: We would be able to run the interactive part of the application simultaneously with the network part, and we would be able to handle multiple simultaneous network connections (otherwise the first connected user would block the application and other users would not be able to connect to it – a denial of service attack). Neither of these two benefits is strictly required, but as they are quite simple to implement, you are encouraged to use them. CreateThread API function can be used to launch a function in its own thread evenin languages which don’t support threads by themselves.

Since any port we define for our server may have been reserved by another application, it is imperative that any server application provides some means for the user to specify the port. We will use either a configuration file or a registry entry for this purpose. Keep in mind that the location of this data must be writable by the user. This could be a registry key under the HKEY_CURRENT_USER/Software branch, or a directory %USERPROFILE%/AppData/Local/Clock/ (you may need to create the Clock directory). To find a path to that directory, you should use the SHGetKnownFolderPathW or SHGetFolderPathW API since the directory name may be localized to another name or rerouted somewhere else than usual. Don’t forget to append the filename (port.txt) in a secure manner!

Setting system time on Windows is a privileged operation, and our application needs to be able to do that. However, because NC is also a server application, we certainly don’t want to run it as Administrator – if we did and overlooked a bug in the server code, it could let the attacker run a remote code of his own within the server process; thanks to the administrative privileges, it would be easy for her to take control over the computer. So we will use the privilege separation method to remove the time-setting functionality from the server; we will create another program (let’s call it Time Setup – TS) that will require administrative privileges and will set the system clock to the specified value. TS shall be run by NC with elevated privileges. That can be achieved through a properly configured manifest and with the requestedPrivilegeLevel attribute set to requireAdministrator. Then you can then use the ShellExecute(Ex) API to launch TS, whereupon UAC automatically requests the user’s permission to run TS and, if the user allows it, TS starts with administrative privileges.

The task can be implemented in almost any operating system. For example, Unix- and Linux-based systems were designed with the possibility of running different applications under different user systems in mind, and support various more-or-less automatic techniques of selecting the right user account (e.g. using the SUID bit or the SU tool). In newer versions, the concept of Capabilities was introduced, which provides the ability to specify the privileges of a process in a great detail.

## Grading system

### Basic solution

In order to be eligible for any points, the application must, at the very least, work locally for the interactive (non-network) user.

- The user physically sitting at the computer must be able to request the time in a format specified by him/her. It’s not sufficient to provide a selection of formats, the user must be able to create their own – even a nonsensical one.
- The user physically sitting at the computer must be able to set the system time.
- A network user may not be able to set the system time.
  - CAUTION! Anybody who uses a network interface to interact with the application is considered a network user, regardless of their actual location or the IP address used (e.g. localhost)!
- The application must be split into at least two parts:
  - The regular part (SH) must run with the privileges of a regular user (or lower).
  - All privileged tasks must be done through a separate application (NC).
  - SH will ensure the privileged start of NC; to simplify matters, it’s OK to just run NC as root or Administrator.
  - NC is only allowed to perform the minimum amount of work and then it must terminate immediately, to minimize the attack vectors. In particular, it is forbidden to leave NC running over prolonged periods of time or to run any other processes from it – functions such as system, fork, exec, ShellExecute and similar are prohibited.
  - NC may not interact with the user in any way.
For completing all of these requirements you will get up to [10 points].

### Full solution

The full solution must satisfy all the requirements of the basic solution, plus these:

- In all applications, give up all privileges you don’t need. If you kept any provileges, explain what do you need them for. [4 points]
- In all applications, subscribe to Data Execution Prevention (in case the operating system is configured in the "OptIn" mode), or provide a reliable documentation that shows that you don’t need to do that. [2 points]
- The SH application will allow remote users to connect and request the current date/time. We assume a "stupid" client, that is, a string containing the formatted date/time will be transferred rather than a binary representation to be formatted by the client. [2 points]
- The remote users may not set the time, but they may specify their own format string for the display of the current time. The creation of the string is up to them, a choice from several options is not sufficient. [2 points]
- Within one session, the user should be able to ask for multiple formattings. [3 points]
- The TCP port used by SH will be configured through a configuration file or a registry key. Explain your choice of location, including the ACLs for it. [2 points]
