package main

import (
	"fmt"
	"net/http"
	"time"
)

func main() {
	fmt.Println("Elephas VPN starting ...")
	url := "http://127.0.0.1:5000/click" 
	
	client := http.Client{
		Timeout: 5 * time.Second, 
	}

	resp, err := client.Get(url)
	
	if err != nil {
		return
	}
	
	defer resp.Body.Close()
}