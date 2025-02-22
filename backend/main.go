package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/ucmo_washing_machine ", getWashingMachines)
	//hnalde all other requests
	http.HandleFunc("/", defaultRoute)

	//start server
	log.Fatal(http.ListenAndServe(":8080", nil))
	
	fmt.Println("Server is running on port 8080")
}

func defaultRoute(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Default Route")
	w.Write([]byte("Default Route"))
}

func getWashingMachines(w http.ResponseWriter, r *http.Request) {
	fmt.Println("/getWashingMachines")
	w.Write([]byte(""))
}
