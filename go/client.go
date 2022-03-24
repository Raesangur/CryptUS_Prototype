package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
	"time"
)

// Client currently interacting with the server
// time is the time at which the client connected to the server
type Client struct {
	Time       time.Time
	LastActive time.Time
}

// This function generates a 16 character long hex token
// it also makes sure that the token is unique
func generateToken(m *map[string]Client) string {
	var token string
	for {
		b := make([]byte, 16)
		rand.Read(b)
		token = hex.EncodeToString(b)
		if _, ok := (*m)[token]; !ok {
			break
		}
	}
	return token
}

// This adds a new client to the map
func addClient(client *map[string]Client) {
	// Use a unique token to identify the client
	name := generateToken(client)
	(*client)[name] = Client{time.Now(), time.Now()}
	// Create a folder in the SERVER_DIR for the client named after the token
	// TODO: make sure file permissions are set correctly
	os.Mkdir(SERVER_DIR+"/"+name, 0777)
	// set a goroutine to remove the client from the map if he's idle
	// also recursively delete the client folder if it is idle for too long
	go func(name string) {
		for {
			time.Sleep(MAX_IDLE)
			if (*client)[name].LastActive.Add(MAX_IDLE).Before(time.Now()) {
				WarnLog.Println("Client ", name, " is idle for too long, deleting")
				// TODO: InfoLog version of this when the client initiates a shutdown
				deleteClient(client, name)
				return
			}
		}
	}(name)
	// Set a goroutine which will watch the client folder for changes
	// and send those files to the blackbox.
	// The LastActive time is updated every time a file is received
}

// Deletes a client
func deleteClient(client *map[string]Client, name string) {
	delete(*client, name)
	os.RemoveAll(SERVER_DIR + "/" + name)
}

// Transfers a file received from the client to the blackbox
func transferFile(name string, file string) {
	fmt.Println("Transferring file ", file, " from ", name, "to Blackbox")
}
