package main

import (
	"encoding/json"
	"fmt"
	
	"math/rand"
	"net/http"
	"strconv"
	"time"
)

type Status string

const (
	Idle     Status = "idle"
	Washing  Status = "washing"
	Finished Status = "finished"
	Reserved Status = "reserved"
	Locked   Status = "locked"
)

type WashingMachine struct {
	ID         string
	State      Status
	State_time int
}

var washingMachines = []WashingMachine{}


func initWashingMachines() {
	rand.Seed(time.Now().UnixNano()) // Seed the random number generator
	for building := 0; building < 10; building++ {
		randomNumber := rand.Intn(101) // Generate a random number between 0 and 100 for the building
		for machine := 0; machine < 10; machine++ {
			washingMachines = append(washingMachines, WashingMachine{
				ID:         strconv.Itoa(randomNumber) +"0" +strconv.Itoa(machine), // Combine building number and machine number
				State:      Idle,
				State_time: int(time.Now().Unix()),
			})
		}
	}
}

func loadRoutes() {
	http.HandleFunc("/machines", getWashingMachines)
	http.HandleFunc("/machine/{id}", getWashingMachine)
	//handle all other requests
	http.HandleFunc("/", defaultRoute)
}

func defaultRoute(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNotFound)
	w.Write([]byte("404 page not found"))
}

func getWashingMachine(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(r.PathValue("id"))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	b, err := json.Marshal(washingMachines[id])
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write(b)
}

func getWashingMachines(w http.ResponseWriter, r *http.Request) {
	fmt.Println("/getWashingMachines")
	b, err := json.Marshal(washingMachines)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write(b)
}
