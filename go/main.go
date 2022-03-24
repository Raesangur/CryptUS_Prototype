package main

import (
	"log"
	"os"
	"time"
)

const (
	SERVER_DIR = "./var/cryptus/"
	LOG_DIR    = "./var/log/"
	LOG_FILE   = "cryptus.log"
	MAX_IDLE   = time.Hour * 2
	// TODO: agree on a port
	// TODO: perhaps make port configurable
	PORT = ":8080"
)

var (
	WarnLog  *log.Logger
	InfoLog  *log.Logger
	ErrorLog *log.Logger
)

func init() {
	// Delete all files in the server directory
	// This way, no user data is kept on the server
	// Better to delete at launch than at shutdown since
	// the server is not guaranteed properly shut down after a crash.
	os.RemoveAll(SERVER_DIR)
	// If the server directory doesn't exist, create it
	if _, err := os.Stat(SERVER_DIR); os.IsNotExist(err) {
		os.MkdirAll(SERVER_DIR, 0755)
	}
	// Make sure the server directory is readable and writable
	os.Chmod(SERVER_DIR, 0755)
	// If the log folder doesn't exist, create it
	if _, err := os.Stat(LOG_DIR); os.IsNotExist(err) {
		os.MkdirAll(LOG_DIR, 0755)
	}
	// Set the log file to be readable and writable
	logfile, err := os.OpenFile(LOG_DIR+LOG_FILE, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0655)
	if err != nil {
		log.Fatalf("error opening log file: %v", err)
	}
	// Log levels are coloured with ANSI escape codes
	InfoLog = log.New(logfile, "\x1b[34mINFO:\x1b[0m ", log.Ldate|log.Ltime|log.Lshortfile)
	WarnLog = log.New(logfile, "\x1b[33;4mWARNING:\x1b[0m ", log.Ldate|log.Ltime|log.Lshortfile)
	ErrorLog = log.New(logfile, "\x1b[37;41mERROR:\x1b[0m ", log.Ldate|log.Ltime|log.Lshortfile)
	InfoLog.Println("Cryptus server is starting.")
}

func main() {
	InfoLog.Println("Cryptus server started.")
	client := map[string]Client{}
	for i := 0; i < 10; i++ {
		addClient(&client)
	}
	WarnLog.Println("Cryptus server is shutting down.")
	time.Sleep(900 * time.Second)
}
