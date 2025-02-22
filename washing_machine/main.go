package main

import (
	"encoding/json"
	"fmt"
	"log"
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
	ID         int
	State      Status
	State_time int
}

var washingMachines = []WashingMachine{}

func main() {

	initWashingMachines()

	loadRoutes()

	log.Print("Server is running on port 8080")
	log.Fatal(http.ListenAndServe(":8080", nil))

	fmt.Println("Server is running on port 8080")
}

func initWashingMachines() {
	for i := 0; i < 10; i++ {
		washingMachines = append(washingMachines, WashingMachine{
			ID:         i,
			State:      Idle,
			State_time: int(time.Now().Unix()),
		})
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
