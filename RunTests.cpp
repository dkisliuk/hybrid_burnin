//ROOT Macro for launching ITSDAQ and running appropriate tests
#include <fcntl.h>
#include <iostream>
#include <sys/stat.h>
#include <unistd.h>
#include <string>

#define MAX_BUF 1024
#define RECV_FIFO "GUI2DAQ.fifo"
#define SEND_FIFO "DAQ2GUI.fifo"

#define O_RDONLY	0x0000
#define O_WRONLY	0x0001
#define O_RDWR		0x0002

#define DEBUG 1

int recvCommand(string fifoName);
int sendCommand(string fifoName, char* buf);

const char* SCTDAQ_ROOT = std::getenv("SCTDAQ_ROOT");
const char* HYBRID_BURN = std::getenv("PWD");

int RunTests()
{
	chdir(SCTDAQ_ROOT);
	gROOT->ProcessLine(".x rootlogon.C");
	gROOT->ProcessLine(".L Stavelet.cpp");
	gROOT->ProcessLine(".L CaptureWhateverABC130.cpp");

	//Open 'read' fifo from GUI
	int fd;
	char recvMsg[MAX_BUF];
	string recvfifo(HYBRID_BURN); recvfifo = recvfifo + '/' + RECV_FIFO;
	string sendfifo(HYBRID_BURN); sendfifo = sendfifo + '/' + SEND_FIFO;
	std::cout << "Opening FIFO '"<< recvfifo << "'. Listening..." << std::endl;

	while(1)
	{
		/*
		fd = open(recvfifo.c_str(), O_RDONLY);
		if(fd < 0)
		{
			std::cout << "Error. Could not open FIFO\n";
			return 1;
		}
		read(fd, buf, MAX_BUF);
		*/

		int check = recvCommand(recvfifo, recvMsg);
		//sendCommand(sendfifo, "ACK\0");
		//if(recvCommand(recvfifo, recvMsg) ) return 1; //If can't recvCommand
		//else sendCommand(sendfifo, "ACK\0");
		//All the different commands
		if(strcmp(recvMsg,"Start") == 0) gROOT->ProcessLine("Stavelet()");
		if(strcmp(recvMsg,"HCC")   == 0) gROOT->ProcessLine("CaptureABC130_HCC_Pattern()");
	}
	return 0;
}

//A function to receive a message through a FIFO
int recvCommand(string fifoName, char* buf)
{
	int fd = open(fifoName.c_str(), O_RDONLY);
	if(fd < 0)
	{
		std::cout << "Error. Could not open FIFO " << fifoName << std::endl;
		return 1;
	}
	read(fd, buf, MAX_BUF);
	if(DEBUG) std::cout << "Received: " << buf << std::endl;

	return 0;
}

int sendCommand(string fifoName, char* buf)
{
	int fd = open(fifoName.c_str(), O_WRONLY);
	if(fd < 0)
	{
		std::cout << "Error. Could not open FIFO " << fifoName << std::endl;
		return 1;
	}
	write(fd, buf, MAX_BUF);
	return 0;
}
