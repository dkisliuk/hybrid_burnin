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
	//Load all the macros into ROOT session
	chdir(SCTDAQ_ROOT);
	gROOT->ProcessLine(".x rootlogon.C");
	gROOT->ProcessLine(".L Stavelet.cpp");
	gROOT->ProcessLine(".L CaptureWhateverABC130.cpp");
	gROOT->ProcessLine(".L ABC130StrobeDelay.cpp");
	gROOT->ProcessLine(".L ABC130StrobeDelay.cpp");
	gROOT->ProcessLine(".L ABC130ThreePointGain.cpp");

	//Open 'read' fifo from GUI
	char recvMsg[MAX_BUF];
	string recvfifo(HYBRID_BURN); recvfifo = recvfifo + '/' + RECV_FIFO;
	string sendfifo(HYBRID_BURN); sendfifo = sendfifo + '/' + SEND_FIFO;
	std::cout << "Opening FIFO '"<< recvfifo << "'. Listening..." << std::endl;

	//Server loop
	int loopflag = 1;
	while(loopflag == 1)
	{
		int check = recvCommand(recvfifo, recvMsg);		
		if(check) return 1;

		//All the commands
		if(strcmp(recvMsg,"Start")   == 0) gROOT->ProcessLine("Stavelet()");
		if(strcmp(recvMsg,"HCC")     == 0) gROOT->ProcessLine("CaptureABC130_HCC_Pattern()");
		if(strcmp(recvMsg,"ChipID")  == 0) gROOT->ProcessLine("CaptureABC130Chips()");
		if(strcmp(recvMsg,"Strobe")  == 0) gROOT->ProcessLine("ABC130StrobeDelay()");
		if(strcmp(recvMsg,"Trim")    == 0) gROOT->ProcessLine("ABC130TrimRange()");
		if(strcmp(recvMsg,"ThreePt") == 0) gROOT->ProcessLine("ABC130ThreePointGain(qCentre=2.0)");
		
		if(strcmp(recvMsg,"Quit")   == 0) break;
		sendCommand(sendfifo, "ACK\0");
	}
	gROOT->ProcessLine(".q");
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
	close(fd);

	return 0;
}

//A function to send a message through a FIFO
int sendCommand(string fifoName, char* buf)
{
	int fd = open(fifoName.c_str(), O_WRONLY);
	if(fd < 0)
	{
		std::cout << "Error. Could not open FIFO " << fifoName << std::endl;
		return 1;
	}
	write(fd, buf, strlen(buf)+1);
	if(DEBUG) std::cout << "Sent: " << buf << std::endl;
	close(fd);

	return 0;
}
